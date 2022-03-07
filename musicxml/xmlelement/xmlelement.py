# -----------------------------------------------------
# AUTOMATICALLY GENERATED WITH generate_xml_elements.py
# -----------------------------------------------------
import copy
import xml.etree.ElementTree as ET
from typing import Optional, List, Callable, Union

from musicxml.exceptions import XSDWrongAttribute, XSDAttributeRequiredException, XMLElementChildrenRequired
from musicxml.generate_classes.utils import musicxml_xsd_et_root, ns
from tree.tree import Tree
from musicxml.util.core import cap_first, replace_key_underline_with_hyphen
from musicxml.xmlelement.containers import containers
from musicxml.xmlelement.exceptions import XMLElementCannotHaveChildrenError
from musicxml.xmlelement.xmlchildcontainer import DuplicationXSDSequence
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdtree import XSDTree


class XMLElement(Tree):
    """
    Parent class of all xml elements.
    """
    _PROPERTIES = {'xsd_tree', 'compact_repr', 'is_leaf', 'level', 'attributes', 'child_container_tree', 'possible_children_names',
                   'et_xml_element', 'name', 'type_', 'value_', 'parent_xsd_element', 'xsd_check'}
    TYPE = None
    _SEARCH_FOR_ELEMENT = ''

    def __init__(self, value_=None, xsd_check=True, **kwargs):
        self.xsd_tree = XSDTree(musicxml_xsd_et_root.find(self._SEARCH_FOR_ELEMENT))
        self._type = None
        super().__init__()
        self._xsd_check = None
        self._value_ = None
        self._attributes = {}
        self._et_xml_element = None
        self._child_container_tree = None
        self._unordered_children = []
        self.value_ = value_
        self.xsd_check = xsd_check
        self._set_attributes(kwargs)

        self._create_child_container_tree()

    def _check_attribute(self, name, value):
        attributes = self.TYPE.get_xsd_attributes()
        allowed_attributes = [attribute.name for attribute in attributes]
        if name not in [attribute.name for attribute in self.TYPE.get_xsd_attributes()]:
            raise XSDWrongAttribute(f"{self.__class__.__name__} has no attribute {name}. Allowed attributes are: {allowed_attributes}")
        for attribute in attributes:
            if attribute.name == name:
                return attribute(value)

    def _check_child_to_be_added(self, child):
        if not isinstance(child, XMLElement):
            raise TypeError

    def _check_required_attributes(self):
        if self.TYPE.get_xsd_tree().is_complex_type:
            required_attributes = [attribute for attribute in self.TYPE.get_xsd_attributes() if attribute.is_required]
            for required_attribute in required_attributes:
                if required_attribute.name not in self.attributes:
                    raise XSDAttributeRequiredException(f"{self.__class__.__name__} requires attribute: {required_attribute.name}")

    def _check_required_value(self):
        if self.TYPE.get_xsd_tree().is_simple_type and self.value_ is None:
            raise ValueError(f"{self.__class__.__name__} needs a value.")

    def _convert_attribute_to_child(self, name, value):
        if not name.startswith('xml_'):
            raise NameError
        child_name = name.replace('xml_', '')

        if '-'.join(child_name.split('_')) not in self.possible_children_names:
            raise NameError

        child_class_name = 'XML' + ''.join([cap_first(partial) for partial in child_name.split('_')])
        child_class = eval(child_class_name)

        found_child = self.find_child(child_class_name)
        if isinstance(value, child_class):
            if found_child:
                self.replace_child(found_child, value)
            else:
                self.add_child(value)
        elif value is None:
            if found_child:
                self.remove(found_child)
        else:
            if found_child:
                found_child.value_ = value
            else:
                self.add_child(child_class(value))

    def _create_child_container_tree(self):
        try:
            if self.TYPE.get_xsd_tree().is_complex_type:
                self._child_container_tree = copy.copy(containers[self.TYPE.__name__])
                self._child_container_tree._parent_xml_element = self
        except KeyError:
            pass

    def _create_et_xml_element(self):
        self._et_xml_element = ET.Element(self.name, {k: str(v) for k, v in self.attributes.items()})
        if self.value_ is not None:
            self._et_xml_element.text = str(self.value_)
        for child in self.get_children():
            self._et_xml_element.append(child.et_xml_element)
        ET.indent(self._et_xml_element, space="  ", level=self.level)

    def _final_checks(self, intelligent_choice=False):
        self._check_required_value()
        if self._child_container_tree:
            required_children = self._child_container_tree.get_required_element_names(intelligent_choice=intelligent_choice)
            if required_children:
                raise XMLElementChildrenRequired(f"{self.__class__.__name__} requires at least following children: {required_children}")

        self._check_required_attributes()

        for child in self.get_children():
            child._final_checks(intelligent_choice=intelligent_choice)

    def _get_attributes_error_message(self, wrong_name):
        attributes = self.TYPE.get_xsd_attributes()
        allowed_attributes = [attribute.name for attribute in attributes]
        return f"{self.__class__.__name__} has no attribute {wrong_name}. Allowed attributes are: " \
               f"{sorted(allowed_attributes)} or possible " \
               f"children as attributes: {sorted(['xml_' + '_'.join(ch.split('-')) for ch in self.possible_children_names])}"

    def _set_attributes(self, val):
        if val is None:
            return

        if self.TYPE.get_xsd_tree().is_simple_type:
            if val:
                raise XSDWrongAttribute(f'{self.__class__.__name__} has no attributes.')

        elif not isinstance(val, dict):
            raise TypeError

        new_attributes = replace_key_underline_with_hyphen(dict_=val)
        none_values_dict = {k: v for k, v in new_attributes.items() if v is None}
        for key in none_values_dict:
            new_attributes.pop(key)
            try:
                self.attributes.pop(key)
            except KeyError:
                pass
        for key in new_attributes:
            self._check_attribute(key, new_attributes[key])
        self._attributes = {**self._attributes, **new_attributes}

    @property
    def attributes(self):
        """
        :return: a dictionary of attributes like {'font-family': 'Arial'}

        >>> t = XMLText(value_='hello', font_family = 'Arial')
        >>> t.attributes
        {'font-family': 'Arial'}
        >>> t.to_string()
        <text font-family="Arial">hello</text>
        """

        return self._attributes

    @property
    def child_container_tree(self):
        """
        :return: A ChildContainerTree object which is used to manage and control XMLElements children. The nodes of a ChildContainerTree
                 have a core content property of types XSDSequence, XSDChoice, XSDGroup or XSDElement. XSDElement are the content type of
                 ChildContainerTree leaves where one or more XMLElements of a single type (depending on maxOccur attribute of element)
                 can be added to its xml_elements list. An interaction of xsd indicators (sequence, choice and group) with xsd elements
                 makes it possible to add XMLElement's Children in the right order and control all xsd rules which apply to musicxml. A
                 variety of exceptions help user to control the xml structure of the exported file which they are intending to use as a
                 musicxml format file.
        """
        return self._child_container_tree

    @property
    def et_xml_element(self):
        """
        :return:  A xml.etree.ElementTree.Element which is used to write the musicxml file.
        """
        self._create_et_xml_element()
        return self._et_xml_element

    @property
    def name(self):
        return self.xsd_tree.get_attributes()['name']

    @property
    def possible_children_names(self):
        if not self.child_container_tree:
            return {}
        else:
            return {leaf.content.name for leaf in self.child_container_tree.iterate_leaves()}

    @property
    def value_(self):
        """
        :return: A validated value of XMLElement which will be translated to its text in xml format.
        """
        return self._value

    @value_.setter
    def value_(self, val):
        """
        :param val: Value to be validated and added to XMLElement. This value will be translated to xml element's text in xml format.
        """
        self.TYPE(val, parent=self)
        self._value = val

    @classmethod
    def get_xsd(cls):
        """
        :return: Snippet of musicxml xsd file which is relevant for this XMLElement.
        """
        return cls.xsd_tree.get_xsd()

    @property
    def xsd_check(self) -> bool:
        """
        Set and get xsd_check attribute. Default is ``True``. If set to false methods add_child() and to_string() run no xsd checking.
        :return: bool
        """
        return self._xsd_check

    @xsd_check.setter
    def xsd_check(self, val):
        self._xsd_check = val

    def add_child(self, child: 'XMLElement', forward: Optional[int] = None) -> 'XMLElement':
        """
        :param XMLElement child: XMLElement child to be added to XMLElement's ChildContainerTree and _unordered_children.
        :param int forward: If there are more than one XSDElement leaves in self.child_container_tree, forward can be used to determine
                            manually which of these equivocal xsd elements is going to be used to attach the child.
        :return: Added child.
        """
        if self.xsd_check:
            if not self._child_container_tree:
                raise XMLElementCannotHaveChildrenError()
            self._child_container_tree.add_element(child, forward)
        self._unordered_children.append(child)
        child._parent = self
        return child

    def get_children(self, ordered: bool = True) -> List['XMLElement']:
        """
        :param bool ordered: True or False.
        :return: XMLElement added children. If ordered is False the _unordered_children is returned as a more light weighted way of
                 getting children instead of using the leaves of ChildContainerTree.
        """
        if ordered is False or self.xsd_check is False:
            return self._unordered_children
        if self._child_container_tree:
            return [xml_element for leaf in self._child_container_tree.iterate_leaves() for xml_element in leaf.content.xml_elements if
                    leaf.content.xml_elements]
        else:
            return []

    def find_child(self, name: Union['XMLElement', str], ordered: bool = False) -> 'XMLElement':
        """
        :param XMLElement/String name: Child or it's name as string.
        :param bool ordered: get_children mode to be used to find first appearance of child.
        :return: found child.
        """
        if isinstance(name, type):
            name = name.__name__
        for ch in self.get_children(ordered=ordered):
            if ch.__class__.__name__ == name:
                return ch

    def find_children(self, name: Union['XMLElement', str], ordered: bool = False) -> List['XMLElement']:
        """
        :param XMLElement/String name: Child or it's name as string.
        :param bool ordered: get_children mode to be used to find children.
        :return: found children.
        """
        if isinstance(name, type):
            name = name.__name__
        return [ch for ch in self.get_children(ordered=ordered) if ch.__class__.__name__ == name]

    def remove(self, child: 'XMLElement') -> None:
        """
        :param XMLElement child: child to be removed. This method must be used to remove a child properly from ChildContainerTree and
                                 reset its behaviour.
        :return: None
        """

        def remove_duplictation():
            for node in parent_container.reversed_path_to_root():
                if node.up:
                    if isinstance(node.up.content, DuplicationXSDSequence) and len(node.up.get_children()) > 1:
                        remove_duplicate = False
                        for leaf in node.iterate_leaves():
                            if leaf != parent_container and leaf.content.xml_elements:
                                break
                            remove_duplicate = True
                        if remove_duplicate:
                            node.up.remove(node)

        self._unordered_children.remove(child)

        if self.xsd_check:
            parent_container = child.parent_xsd_element.parent_container.get_parent()
            if parent_container.chosen_child == child.parent_xsd_element.parent_container:
                parent_container.chosen_child = None
                parent_container.requirements_not_fulfilled = True
            child.parent_xsd_element.xml_elements.remove(child)
            child.parent_xsd_element = None
            remove_duplictation()

        child._parent = None
        del child

    def replace_child(self, old: Union['XMLElement', Callable], new: 'XMLElement', index: int = 0) -> 'XMLElement':
        """
        :param XMLElement or function old: A child or function which is used to find a child to be replaced.
        :param XMLElement new: child to be replaced with.
        :param int index: index of old in list of old appearances
        :return: new xml element
        :rtype: XMLElement
        """
        if hasattr(old, '__call__'):
            list_of_olds = [ch for ch in self.get_children(ordered=True) if old(ch)]
        else:
            list_of_olds = [ch for ch in self.get_children(ordered=True) if ch == old]

        if not list_of_olds:
            raise ValueError(f"{old} not in list.")
        self._check_child_to_be_added(new)
        old_index = self._unordered_children.index(list_of_olds[index])
        old_child = self._unordered_children[old_index]
        self._unordered_children.remove(old_child)
        self._unordered_children.insert(old_index, new)

        if self.xsd_check:
            parent_xsd_element = old_child.parent_xsd_element
            new.parent_xsd_element = parent_xsd_element
            parent_xsd_element._xml_elements = [new if el == old_child else el for el in parent_xsd_element.xml_elements]
        new._parent = self
        old._parent = None
        return new

    def to_string(self, intelligent_choice: bool = False) -> str:
        """
        :param bool intelligent_choice: Set to True if you wish to use intelligent choice in final checks to be able to change the
                                         attachment order of XMLElement children in self.child_container_tree if an Exception was thrown
                                         and other choices can still be checked. (No GUARANTEE!)
        :return: String in xml format.
        """
        if self.xsd_check:
            self._final_checks(intelligent_choice=intelligent_choice)
        self._create_et_xml_element()

        return ET.tostring(self.et_xml_element, encoding='unicode') + '\n'

    def __setattr__(self, key, value):
        if key[0] == '_' or key in self._PROPERTIES:
            super().__setattr__(key, value)
        elif key.startswith('xml_'):
            try:
                self._convert_attribute_to_child(name=key, value=value)
            except NameError:
                raise AttributeError(self._get_attributes_error_message(key))
        else:
            try:
                self._set_attributes({key: value})
            except XSDWrongAttribute:
                raise AttributeError(self._get_attributes_error_message(key))

    def __getattr__(self, item):
        try:
            return self.attributes['-'.join(item.split('_'))]
        except KeyError:
            attributes = self.TYPE.get_xsd_attributes()
            allowed_attributes = ['_'.join(attribute.name.split('-')) for attribute in attributes]
            if item in allowed_attributes:
                return None
            else:
                if item.startswith('xml'):
                    child_name = item.replace('xml_', '')
                    for child in self.get_children(ordered=False):
                        if child.name == '-'.join(child_name.split('_')):
                            return child
                    if '-'.join(child_name.split('_')) in self.possible_children_names:
                        return None
                raise AttributeError(self._get_attributes_error_message(item))


class XMLSenzaMisura(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/senza-misura/>`_

A senza-misura element explicitly indicates that no time signature is present. The optional element content indicates the symbol to be used, if any, such as an X. The time element's symbol attribute is not used when a senza-misura element is present.



``Possible parents``::obj:`~XMLTime`
    """

    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='senza-misura'][@type='xs:string']"

    def __init__(self, value_='', *args, **kwargs):
        super().__init__(value_=value_, *args, **kwargs)
        
# -----------------------------------------------------
# AUTOMATICALLY GENERATED WITH generate_xml_elements.py
# -----------------------------------------------------


class XMLAccent(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/accent/>`_
    
    The accent element indicates a regular horizontal accent mark.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='accent'][@type='empty-placement']"


class XMLAccidental(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/accidental/>`_
    
    
    
    ``complexType``: The accidental type represents actual notated accidentals. Editorial and cautionary indications are indicated by attributes. Values for these attributes are "no" if not present. Specific graphic display such as parentheses, brackets, and size are controlled by the level-display attribute group.
    
    ``simpleContent``: The accidental-value type represents notated accidentals supported by MusicXML. In the MusicXML 2.0 DTD this was a string with values that could be included. The XSD strengthens the data typing to an enumerated list. The quarter- and three-quarters- accidentals are Tartini-style quarter-tone accidentals. The -down and -up accidentals are quarter-tone accidentals that include arrows pointing down or up. The slash- accidentals are used in Turkish classical music. The numbered sharp and flat accidentals are superscripted versions of the accidental signs, used in Turkish folk music. The sori and koron accidentals are microtonal sharp and flat accidentals used in Iranian and Persian music. The other accidental covers accidentals other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL accidental. The smufl attribute may be used with any accidental value to help specify the appearance of symbols that share the same MusicXML semantics.
        
        Permitted Values: ``'sharp'``, ``'natural'``, ``'flat'``, ``'double-sharp'``, ``'sharp-sharp'``, ``'flat-flat'``, ``'natural-sharp'``, ``'natural-flat'``, ``'quarter-flat'``, ``'quarter-sharp'``, ``'three-quarters-flat'``, ``'three-quarters-sharp'``, ``'sharp-down'``, ``'sharp-up'``, ``'natural-down'``, ``'natural-up'``, ``'flat-down'``, ``'flat-up'``, ``'double-sharp-down'``, ``'double-sharp-up'``, ``'flat-flat-down'``, ``'flat-flat-up'``, ``'arrow-down'``, ``'arrow-up'``, ``'triple-sharp'``, ``'triple-flat'``, ``'slash-quarter-sharp'``, ``'slash-sharp'``, ``'slash-flat'``, ``'double-slash-flat'``, ``'sharp-1'``, ``'sharp-2'``, ``'sharp-3'``, ``'sharp-5'``, ``'flat-1'``, ``'flat-2'``, ``'flat-3'``, ``'flat-4'``, ``'sori'``, ``'koron'``, ``'other'``
    

    ``Possible attributes``: ``bracket``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``cautionary``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``editorial``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``parentheses``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSymbolSize`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflAccidentalGlyphName`

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeAccidental
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='accidental'][@type='accidental']"


class XMLAccidentalMark(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/accidental-mark/>`_
    
    
    
    ``complexType``: An accidental-mark can be used as a separate notation or as part of an ornament. When used in an ornament, position and placement are relative to the ornament, not relative to the note.
    
    ``simpleContent``: The accidental-value type represents notated accidentals supported by MusicXML. In the MusicXML 2.0 DTD this was a string with values that could be included. The XSD strengthens the data typing to an enumerated list. The quarter- and three-quarters- accidentals are Tartini-style quarter-tone accidentals. The -down and -up accidentals are quarter-tone accidentals that include arrows pointing down or up. The slash- accidentals are used in Turkish classical music. The numbered sharp and flat accidentals are superscripted versions of the accidental signs, used in Turkish folk music. The sori and koron accidentals are microtonal sharp and flat accidentals used in Iranian and Persian music. The other accidental covers accidentals other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL accidental. The smufl attribute may be used with any accidental value to help specify the appearance of symbols that share the same MusicXML semantics.
        
        Permitted Values: ``'sharp'``, ``'natural'``, ``'flat'``, ``'double-sharp'``, ``'sharp-sharp'``, ``'flat-flat'``, ``'natural-sharp'``, ``'natural-flat'``, ``'quarter-flat'``, ``'quarter-sharp'``, ``'three-quarters-flat'``, ``'three-quarters-sharp'``, ``'sharp-down'``, ``'sharp-up'``, ``'natural-down'``, ``'natural-up'``, ``'flat-down'``, ``'flat-up'``, ``'double-sharp-down'``, ``'double-sharp-up'``, ``'flat-flat-down'``, ``'flat-flat-up'``, ``'arrow-down'``, ``'arrow-up'``, ``'triple-sharp'``, ``'triple-flat'``, ``'slash-quarter-sharp'``, ``'slash-sharp'``, ``'slash-flat'``, ``'double-slash-flat'``, ``'sharp-1'``, ``'sharp-2'``, ``'sharp-3'``, ``'sharp-5'``, ``'flat-1'``, ``'flat-2'``, ``'flat-3'``, ``'flat-4'``, ``'sori'``, ``'koron'``, ``'other'``
    

    ``Possible attributes``: ``bracket``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``parentheses``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSymbolSize`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflAccidentalGlyphName`

``Possible parents``::obj:`~XMLNotations`, :obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeAccidentalMark
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='accidental-mark'][@type='accidental-mark']"


class XMLAccidentalText(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/accidental-text/>`_
    
    
    
    ``complexType``: The accidental-text type represents an element with an accidental value and text-formatting attributes.
    
    ``simpleContent``: The accidental-value type represents notated accidentals supported by MusicXML. In the MusicXML 2.0 DTD this was a string with values that could be included. The XSD strengthens the data typing to an enumerated list. The quarter- and three-quarters- accidentals are Tartini-style quarter-tone accidentals. The -down and -up accidentals are quarter-tone accidentals that include arrows pointing down or up. The slash- accidentals are used in Turkish classical music. The numbered sharp and flat accidentals are superscripted versions of the accidental signs, used in Turkish folk music. The sori and koron accidentals are microtonal sharp and flat accidentals used in Iranian and Persian music. The other accidental covers accidentals other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL accidental. The smufl attribute may be used with any accidental value to help specify the appearance of symbols that share the same MusicXML semantics.
        
        Permitted Values: ``'sharp'``, ``'natural'``, ``'flat'``, ``'double-sharp'``, ``'sharp-sharp'``, ``'flat-flat'``, ``'natural-sharp'``, ``'natural-flat'``, ``'quarter-flat'``, ``'quarter-sharp'``, ``'three-quarters-flat'``, ``'three-quarters-sharp'``, ``'sharp-down'``, ``'sharp-up'``, ``'natural-down'``, ``'natural-up'``, ``'flat-down'``, ``'flat-up'``, ``'double-sharp-down'``, ``'double-sharp-up'``, ``'flat-flat-down'``, ``'flat-flat-up'``, ``'arrow-down'``, ``'arrow-up'``, ``'triple-sharp'``, ``'triple-flat'``, ``'slash-quarter-sharp'``, ``'slash-sharp'``, ``'slash-flat'``, ``'double-slash-flat'``, ``'sharp-1'``, ``'sharp-2'``, ``'sharp-3'``, ``'sharp-5'``, ``'flat-1'``, ``'flat-2'``, ``'flat-3'``, ``'flat-4'``, ``'sori'``, ``'koron'``, ``'other'``
    

``Possible parents``::obj:`~XMLGroupAbbreviationDisplay`, :obj:`~XMLGroupNameDisplay`, :obj:`~XMLNoteheadText`, :obj:`~XMLPartAbbreviationDisplay`, :obj:`~XMLPartNameDisplay`
    """
    
    TYPE = XSDComplexTypeAccidentalText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='accidental-text'][@type='accidental-text']"


class XMLAccord(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/accord/>`_
    
    
    
    ``complexType``: The accord type represents the tuning of a single string in the scordatura element. It uses the same group of elements as the staff-tuning element. Strings are numbered from high to low.

    ``Possible attributes``: ``string``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStringNumber`

    ``Possible children``:    :obj:`~XMLTuningAlter`, :obj:`~XMLTuningOctave`, :obj:`~XMLTuningStep`

    ``XSD structure:``

    .. code-block::

       Group@name=tuning@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Element@name=tuning-step@minOccurs=1@maxOccurs=1
               Element@name=tuning-alter@minOccurs=0@maxOccurs=1
               Element@name=tuning-octave@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLScordatura`
    """
    
    TYPE = XSDComplexTypeAccord
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='accord'][@type='accord']"


class XMLAccordionHigh(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/accordion-high/>`_
    
    The accordion-high element indicates the presence of a dot in the high (4') section of the registration symbol. This element is omitted if no dot is present.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLAccordionRegistration`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='accordion-high'][@type='empty']"


class XMLAccordionLow(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/accordion-low/>`_
    
    The accordion-low element indicates the presence of a dot in the low (16') section of the registration symbol. This element is omitted if no dot is present.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLAccordionRegistration`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='accordion-low'][@type='empty']"


class XMLAccordionMiddle(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/accordion-middle/>`_
    
    The accordion-middle element indicates the presence of 1 to 3 dots in the middle (8') section of the registration symbol. This element is omitted if no dots are present.
    
    
    
    ``simpleType``: The accordion-middle type may have values of 1, 2, or 3, corresponding to having 1 to 3 dots in the middle section of the accordion registration symbol. This type is not used if no dots are present.

``Possible parents``::obj:`~XMLAccordionRegistration`
    """
    
    TYPE = XSDSimpleTypeAccordionMiddle
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='accordion-middle'][@type='accordion-middle']"


class XMLAccordionRegistration(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/accordion-registration/>`_
    
    
    
    ``complexType``: The accordion-registration type is used for accordion registration symbols. These are circular symbols divided horizontally into high, middle, and low sections that correspond to 4', 8', and 16' pipes. Each accordion-high, accordion-middle, and accordion-low element represents the presence of one or more dots in the registration diagram. An accordion-registration element needs to have at least one of the child elements present.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

    ``Possible children``:    :obj:`~XMLAccordionHigh`, :obj:`~XMLAccordionLow`, :obj:`~XMLAccordionMiddle`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=accordion-high@minOccurs=0@maxOccurs=1
           Element@name=accordion-middle@minOccurs=0@maxOccurs=1
           Element@name=accordion-low@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeAccordionRegistration
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='accordion-registration'][@type='accordion-registration']"


class XMLActualNotes(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/actual-notes/>`_

The actual-notes element describes how many notes are played in the time usually occupied by the number in the normal-notes element.



``Possible parents``::obj:`~XMLMetronomeTuplet`, :obj:`~XMLTimeModification`
    """
    
    TYPE = XSDSimpleTypeNonNegativeInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='actual-notes'][@type='xs:nonNegativeInteger']"


class XMLAlter(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/alter/>`_
    
    
    
    ``simpleType``: The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.

``Possible parents``::obj:`~XMLPitch`
    """
    
    TYPE = XSDSimpleTypeSemitones
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='alter'][@type='semitones']"


class XMLAppearance(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/appearance/>`_
    
    
    
    ``complexType``: The appearance type controls general graphical settings for the music's final form appearance on a printed page of display. This includes support for line widths, definitions for note sizes, and standard distances between notation elements, plus an extension element for other aspects of appearance.

    ``Possible children``:    :obj:`~XMLDistance`, :obj:`~XMLGlyph`, :obj:`~XMLLineWidth`, :obj:`~XMLNoteSize`, :obj:`~XMLOtherAppearance`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=line-width@minOccurs=0@maxOccurs=unbounded
           Element@name=note-size@minOccurs=0@maxOccurs=unbounded
           Element@name=distance@minOccurs=0@maxOccurs=unbounded
           Element@name=glyph@minOccurs=0@maxOccurs=unbounded
           Element@name=other-appearance@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLDefaults`
    """
    
    TYPE = XSDComplexTypeAppearance
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='appearance'][@type='appearance']"


class XMLArpeggiate(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/arpeggiate/>`_
    
    
    
    ``complexType``: The arpeggiate type indicates that this note is part of an arpeggiated chord. The number attribute can be used to distinguish between two simultaneous chords arpeggiated separately (different numbers) or together (same number). The direction attribute is used if there is an arrow on the arpeggio sign. By default, arpeggios go from the lowest to highest note.  The length of the sign can be determined from the position attributes for the arpeggiate elements used with the top and bottom notes of the arpeggiated chord. If the unbroken attribute is set to yes, it indicates that the arpeggio continues onto another staff within the part. This serves as a hint to applications and is not required for cross-staff arpeggios.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``direction``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeUpDown`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``unbroken``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

``Possible parents``::obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeArpeggiate
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='arpeggiate'][@type='arpeggiate']"


class XMLArrow(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/arrow/>`_
    
    
    
    ``complexType``: The arrow element represents an arrow used for a musical technical indication. It can represent both Unicode and SMuFL arrows. The presence of an arrowhead element indicates that only the arrowhead is displayed, not the arrow stem. The smufl attribute distinguishes different SMuFL glyphs that have an arrow appearance such as arrowBlackUp, guitarStrumUp, or handbellsSwingUp. The specified glyph should match the descriptive representation.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`

    ``Possible children``:    :obj:`~XMLArrowDirection`, :obj:`~XMLArrowStyle`, :obj:`~XMLArrowhead`, :obj:`~XMLCircularArrow`

    ``XSD structure:``

    .. code-block::

       Choice@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Element@name=arrow-direction@minOccurs=1@maxOccurs=1
               Element@name=arrow-style@minOccurs=0@maxOccurs=1
               Element@name=arrowhead@minOccurs=0@maxOccurs=1
           Element@name=circular-arrow@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeArrow
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='arrow'][@type='arrow']"


class XMLArrowDirection(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/arrow-direction/>`_
    
    
    
    ``simpleType``: The arrow-direction type represents the direction in which an arrow points, using Unicode arrow terminology.
        
        Permitted Values: ``'left'``, ``'up'``, ``'right'``, ``'down'``, ``'northwest'``, ``'northeast'``, ``'southeast'``, ``'southwest'``, ``'left right'``, ``'up down'``, ``'northwest southeast'``, ``'northeast southwest'``, ``'other'``
    

``Possible parents``::obj:`~XMLArrow`
    """
    
    TYPE = XSDSimpleTypeArrowDirection
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='arrow-direction'][@type='arrow-direction']"


class XMLArrowStyle(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/arrow-style/>`_
    
    
    
    ``simpleType``: The arrow-style type represents the style of an arrow, using Unicode arrow terminology. Filled and hollow arrows indicate polygonal single arrows. Paired arrows are duplicate single arrows in the same direction. Combined arrows apply to double direction arrows like left right, indicating that an arrow in one direction should be combined with an arrow in the other direction.
        
        Permitted Values: ``'single'``, ``'double'``, ``'filled'``, ``'hollow'``, ``'paired'``, ``'combined'``, ``'other'``
    

``Possible parents``::obj:`~XMLArrow`
    """
    
    TYPE = XSDSimpleTypeArrowStyle
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='arrow-style'][@type='arrow-style']"


class XMLArrowhead(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/arrowhead/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLArrow`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='arrowhead'][@type='empty']"


class XMLArticulations(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/articulations/>`_
    
    
    
    ``complexType``: Articulations and accents are grouped together here.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`

    ``Possible children``:    :obj:`~XMLAccent`, :obj:`~XMLBreathMark`, :obj:`~XMLCaesura`, :obj:`~XMLDetachedLegato`, :obj:`~XMLDoit`, :obj:`~XMLFalloff`, :obj:`~XMLOtherArticulation`, :obj:`~XMLPlop`, :obj:`~XMLScoop`, :obj:`~XMLSoftAccent`, :obj:`~XMLSpiccato`, :obj:`~XMLStaccatissimo`, :obj:`~XMLStaccato`, :obj:`~XMLStress`, :obj:`~XMLStrongAccent`, :obj:`~XMLTenuto`, :obj:`~XMLUnstress`

    ``XSD structure:``

    .. code-block::

       Choice@minOccurs=0@maxOccurs=unbounded
           Element@name=accent@minOccurs=1@maxOccurs=1
           Element@name=strong-accent@minOccurs=1@maxOccurs=1
           Element@name=staccato@minOccurs=1@maxOccurs=1
           Element@name=tenuto@minOccurs=1@maxOccurs=1
           Element@name=detached-legato@minOccurs=1@maxOccurs=1
           Element@name=staccatissimo@minOccurs=1@maxOccurs=1
           Element@name=spiccato@minOccurs=1@maxOccurs=1
           Element@name=scoop@minOccurs=1@maxOccurs=1
           Element@name=plop@minOccurs=1@maxOccurs=1
           Element@name=doit@minOccurs=1@maxOccurs=1
           Element@name=falloff@minOccurs=1@maxOccurs=1
           Element@name=breath-mark@minOccurs=1@maxOccurs=1
           Element@name=caesura@minOccurs=1@maxOccurs=1
           Element@name=stress@minOccurs=1@maxOccurs=1
           Element@name=unstress@minOccurs=1@maxOccurs=1
           Element@name=soft-accent@minOccurs=1@maxOccurs=1
           Element@name=other-articulation@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeArticulations
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='articulations'][@type='articulations']"


class XMLArtificial(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/artificial/>`_
    
    The artificial element indicates that this is an artificial harmonic.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLHarmonic`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='artificial'][@type='empty']"


class XMLAssess(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/assess/>`_
    
    
    
    ``complexType``: By default, an assessment application should assess all notes without a cue child element, and not assess any note with a cue child element. The assess type allows this default assessment to be overridden for individual notes. The optional player and time-only attributes restrict the type to apply to a single player or set of times through a repeated section, respectively. If missing, the type applies to all players or all times through the repeated section, respectively. The player attribute references the id attribute of a player element defined within the matching score-part.

    ``Possible attributes``: ``player``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF`, ``time_only``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeOnly`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`\@required

``Possible parents``::obj:`~XMLListen`
    """
    
    TYPE = XSDComplexTypeAssess
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='assess'][@type='assess']"


class XMLAttributes(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/attributes/>`_
    
    
    
    ``complexType``: The attributes element contains musical information that typically changes on measure boundaries. This includes key and time signatures, clefs, transpositions, and staving. When attributes are changed mid-measure, it affects the music in score order, not in MusicXML document order.

    ``Possible children``:    :obj:`~XMLClef`, :obj:`~XMLDirective`, :obj:`~XMLDivisions`, :obj:`~XMLFootnote`, :obj:`~XMLForPart`, :obj:`~XMLInstruments`, :obj:`~XMLKey`, :obj:`~XMLLevel`, :obj:`~XMLMeasureStyle`, :obj:`~XMLPartSymbol`, :obj:`~XMLStaffDetails`, :obj:`~XMLStaves`, :obj:`~XMLTime`, :obj:`~XMLTranspose`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Group@name=editorial@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=footnote@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=footnote@minOccurs=1@maxOccurs=1
                   Group@name=level@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=level@minOccurs=1@maxOccurs=1
           Element@name=divisions@minOccurs=0@maxOccurs=1
           Element@name=key@minOccurs=0@maxOccurs=unbounded
           Element@name=time@minOccurs=0@maxOccurs=unbounded
           Element@name=staves@minOccurs=0@maxOccurs=1
           Element@name=part-symbol@minOccurs=0@maxOccurs=1
           Element@name=instruments@minOccurs=0@maxOccurs=1
           Element@name=clef@minOccurs=0@maxOccurs=unbounded
           Element@name=staff-details@minOccurs=0@maxOccurs=unbounded
           Choice@minOccurs=1@maxOccurs=1
               Element@name=transpose@minOccurs=0@maxOccurs=unbounded
               Element@name=for-part@minOccurs=0@maxOccurs=unbounded
           Element@name=directive@minOccurs=0@maxOccurs=unbounded
           Element@name=measure-style@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeAttributes
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='attributes'][@type='attributes']"


class XMLBackup(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/backup/>`_
    
    
    
    ``complexType``: The backup and forward elements are required to coordinate multiple voices in one part, including music on multiple staves. The backup type is generally used to move between voices and staves. Thus the backup element does not include voice or staff elements. Duration values should always be positive, and should not cross measure boundaries or mid-measure changes in the divisions value.

    ``Possible children``:    :obj:`~XMLDuration`, :obj:`~XMLFootnote`, :obj:`~XMLLevel`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Group@name=duration@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=duration@minOccurs=1@maxOccurs=1
           Group@name=editorial@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=footnote@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=footnote@minOccurs=1@maxOccurs=1
                   Group@name=level@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=level@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeBackup
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='backup'][@type='backup']"


class XMLBarStyle(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/bar-style/>`_
    
    
    
    ``complexType``: The bar-style-color type contains barline style and color information.
    
    ``simpleContent``: The bar-style type represents barline style information. Choices are regular, dotted, dashed, heavy, light-light, light-heavy, heavy-light, heavy-heavy, tick (a short stroke through the top line), short (a partial barline between the 2nd and 4th lines), and none.
        
        Permitted Values: ``'regular'``, ``'dotted'``, ``'dashed'``, ``'heavy'``, ``'light-light'``, ``'light-heavy'``, ``'heavy-light'``, ``'heavy-heavy'``, ``'tick'``, ``'short'``, ``'none'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`

``Possible parents``::obj:`~XMLBarline`
    """
    
    TYPE = XSDComplexTypeBarStyleColor
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='bar-style'][@type='bar-style-color']"


class XMLBarline(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/barline/>`_
    
    
    
    ``complexType``: If a barline is other than a normal single barline, it should be represented by a barline type that describes it. This includes information about repeats and multiple endings, as well as line style. Barline data is on the same level as the other musical data in a score - a child of a measure in a partwise score, or a part in a timewise score. This allows for barlines within measures, as in dotted barlines that subdivide measures in complex meters. The two fermata elements allow for fermatas on both sides of the barline (the lower one inverted).
    
    Barlines have a location attribute to make it easier to process barlines independently of the other musical data in a score. It is often easier to set up measures separately from entering notes. The location attribute must match where the barline element occurs within the rest of the musical data in the score. If location is left, it should be the first element in the measure, aside from the print, bookmark, and link elements. If location is right, it should be the last element, again with the possible exception of the print, bookmark, and link elements. If no location is specified, the right barline is the default. The segno, coda, and divisions attributes work the same way as in the sound element. They are used for playback when barline elements contain segno or coda child elements.

    ``Possible attributes``: ``coda``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``divisions``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeDivisions`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``location``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeRightLeftMiddle`, ``segno``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

    ``Possible children``:    :obj:`~XMLBarStyle`, :obj:`~XMLCoda`, :obj:`~XMLEnding`, :obj:`~XMLFermata`, :obj:`~XMLFootnote`, :obj:`~XMLLevel`, :obj:`~XMLRepeat`, :obj:`~XMLSegno`, :obj:`~XMLWavyLine`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=bar-style@minOccurs=0@maxOccurs=1
           Group@name=editorial@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=footnote@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=footnote@minOccurs=1@maxOccurs=1
                   Group@name=level@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=level@minOccurs=1@maxOccurs=1
           Element@name=wavy-line@minOccurs=0@maxOccurs=1
           Element@name=segno@minOccurs=0@maxOccurs=1
           Element@name=coda@minOccurs=0@maxOccurs=1
           Element@name=fermata@minOccurs=0@maxOccurs=2
           Element@name=ending@minOccurs=0@maxOccurs=1
           Element@name=repeat@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeBarline
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='barline'][@type='barline']"


class XMLBarre(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/barre/>`_
    
    
    
    ``complexType``: The barre element indicates placing a finger over multiple strings on a single fret. The type is "start" for the lowest pitched string (e.g., the string with the highest MusicXML number) and is "stop" for the highest pitched string.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required

``Possible parents``::obj:`~XMLFrameNote`
    """
    
    TYPE = XSDComplexTypeBarre
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='barre'][@type='barre']"


class XMLBasePitch(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/base-pitch/>`_
    
    The base pitch is the pitch at which the string is played before touching to create the harmonic.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLHarmonic`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='base-pitch'][@type='empty']"


class XMLBass(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/bass/>`_
    
    
    
    ``complexType``: The bass type is used to indicate a bass note in popular music chord symbols, e.g. G/C. It is generally not used in functional harmony, as inversion is generally not used in pop chord symbols. As with root, it is divided into step and alter elements, similar to pitches. The arrangement attribute specifies where the bass is displayed relative to what precedes it.

    ``Possible attributes``: ``arrangement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeHarmonyArrangement`

    ``Possible children``:    :obj:`~XMLBassAlter`, :obj:`~XMLBassSeparator`, :obj:`~XMLBassStep`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=bass-separator@minOccurs=0@maxOccurs=1
           Element@name=bass-step@minOccurs=1@maxOccurs=1
           Element@name=bass-alter@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLHarmony`
    """
    
    TYPE = XSDComplexTypeBass
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='bass'][@type='bass']"


class XMLBassAlter(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/bass-alter/>`_
    
    The bass-alter element represents the chromatic alteration of the bass of the current chord within the harmony element. In some chord styles, the text for the bass-step element may include bass-alter information. In that case, the print-object attribute of the bass-alter element can be set to no. The location attribute indicates whether the alteration should appear to the left or the right of the bass-step; it is right if not specified.
    
    
    
    ``complexType``: The harmony-alter type represents the chromatic alteration of the root, numeral, or bass of the current harmony-chord group within the harmony element. In some chord styles, the text of the preceding element may include alteration information. In that case, the print-object attribute of this type can be set to no. The location attribute indicates whether the alteration should appear to the left or the right of the preceding element. Its default value varies by element.
    
    ``simpleContent``: The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``location``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftRight`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLBass`
    """
    
    TYPE = XSDComplexTypeHarmonyAlter
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='bass-alter'][@type='harmony-alter']"


class XMLBassSeparator(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/bass-separator/>`_
    
    The optional bass-separator element indicates that text, rather than a line or slash, separates the bass from what precedes it.
    
    
    
    ``complexType``: The style-text type represents a text element with a print-style attribute group.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLBass`
    """
    
    TYPE = XSDComplexTypeStyleText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='bass-separator'][@type='style-text']"


class XMLBassStep(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/bass-step/>`_
    
    
    
    ``complexType``: The bass-step type represents the pitch step of the bass of the current chord within the harmony element. The text attribute indicates how the bass should appear in a score if not using the element contents.
    
    ``simpleContent``: The step type represents a step of the diatonic scale, represented using the English letters A through G.
        
        Permitted Values: ``'A'``, ``'B'``, ``'C'``, ``'D'``, ``'E'``, ``'F'``, ``'G'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``text``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLBass`
    """
    
    TYPE = XSDComplexTypeBassStep
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='bass-step'][@type='bass-step']"


class XMLBeam(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/beam/>`_
    
    
    
    ``complexType``: Beam values include begin, continue, end, forward hook, and backward hook. Up to eight concurrent beams are available to cover up to 1024th notes. Each beam in a note is represented with a separate beam element, starting with the eighth note beam using a number attribute of 1.
    
    Note that the beam number does not distinguish sets of beams that overlap, as it does for slur and other elements. Beaming groups are distinguished by being in different voices and/or the presence or absence of grace and cue elements.
    
    Beams that have a begin value can also have a fan attribute to indicate accelerandos and ritardandos using fanned beams. The fan attribute may also be used with a continue value if the fanning direction changes on that note. The value is "none" if not specified.
    
    The repeater attribute has been deprecated in MusicXML 3.0. Formerly used for tremolos, it needs to be specified with a "yes" value for each beam using it.
    
    ``simpleContent``: The beam-value type represents the type of beam associated with each of 8 beam levels (up to 1024th notes) available for each note.
        
        Permitted Values: ``'begin'``, ``'continue'``, ``'end'``, ``'forward hook'``, ``'backward hook'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``fan``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFan`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeBeamLevel`, ``repeater``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeBeam
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='beam'][@type='beam']"


class XMLBeatRepeat(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/beat-repeat/>`_
    
    
    
    ``complexType``: The beat-repeat type is used to indicate that a single beat (but possibly many notes) is repeated. The slashes attribute specifies the number of slashes to use in the symbol. The use-dots attribute indicates whether or not to use dots as well (for instance, with mixed rhythm patterns). The value for slashes is 1 and the value for use-dots is no if not specified.
    
    The stop type indicates the first beat where the repeats are no longer displayed. Both the start and stop of the beat being repeated should be specified unless the repeats are displayed through the end of the part.
    
    The beat-repeat element specifies a notation style for repetitions. The actual music being repeated needs to be repeated within the MusicXML file. This element specifies the notation that indicates the repeat.

    ``Possible attributes``: ``slashes``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePositiveInteger`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required, ``use_dots``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

    ``Possible children``:    :obj:`~XMLExceptVoice`, :obj:`~XMLSlashDot`, :obj:`~XMLSlashType`

    ``XSD structure:``

    .. code-block::

       Group@name=slash@minOccurs=0@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=0@maxOccurs=1
                   Element@name=slash-type@minOccurs=1@maxOccurs=1
                   Element@name=slash-dot@minOccurs=0@maxOccurs=unbounded
               Element@name=except-voice@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLMeasureStyle`
    """
    
    TYPE = XSDComplexTypeBeatRepeat
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='beat-repeat'][@type='beat-repeat']"


class XMLBeatType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/beat-type/>`_

The beat-type element indicates the beat unit, as found in the denominator of a time signature.



``Possible parents``::obj:`~XMLInterchangeable`, :obj:`~XMLTime`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='beat-type'][@type='xs:string']"


class XMLBeatUnit(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/beat-unit/>`_
    
    The beat-unit element indicates the graphical note type to use in a metronome mark.
    
    
    
    ``simpleType``: The note-type-value type is used for the MusicXML type element and represents the graphic note type, from 1024th (shortest) to maxima (longest).
        
        Permitted Values: ``'1024th'``, ``'512th'``, ``'256th'``, ``'128th'``, ``'64th'``, ``'32nd'``, ``'16th'``, ``'eighth'``, ``'quarter'``, ``'half'``, ``'whole'``, ``'breve'``, ``'long'``, ``'maxima'``
    

``Possible parents``::obj:`~XMLBeatUnitTied`, :obj:`~XMLMetronome`
    """
    
    TYPE = XSDSimpleTypeNoteTypeValue
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='beat-unit'][@type='note-type-value']"


class XMLBeatUnitDot(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/beat-unit-dot/>`_
    
    The beat-unit-dot element is used to specify any augmentation dots for a metronome mark note.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLBeatUnitTied`, :obj:`~XMLMetronome`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='beat-unit-dot'][@type='empty']"


class XMLBeatUnitTied(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/beat-unit-tied/>`_
    
    
    
    ``complexType``: The beat-unit-tied type indicates a beat-unit within a metronome mark that is tied to the preceding beat-unit. This allows two or more tied notes to be associated with a per-minute value in a metronome mark, whereas the metronome-tied element is restricted to metric relationship marks.

    ``Possible children``:    :obj:`~XMLBeatUnitDot`, :obj:`~XMLBeatUnit`

    ``XSD structure:``

    .. code-block::

       Group@name=beat-unit@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Element@name=beat-unit@minOccurs=1@maxOccurs=1
               Element@name=beat-unit-dot@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLMetronome`
    """
    
    TYPE = XSDComplexTypeBeatUnitTied
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='beat-unit-tied'][@type='beat-unit-tied']"


class XMLBeater(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/beater/>`_
    
    
    
    ``complexType``: The beater type represents pictograms for beaters, mallets, and sticks that do not have different materials represented in the pictogram.
    
    ``simpleContent``: The beater-value type represents pictograms for beaters, mallets, and sticks that do not have different materials represented in the pictogram. The finger and hammer values are in addition to Stone's list.
        
        Permitted Values: ``'bow'``, ``'chime hammer'``, ``'coin'``, ``'drum stick'``, ``'finger'``, ``'fingernail'``, ``'fist'``, ``'guiro scraper'``, ``'hammer'``, ``'hand'``, ``'jazz stick'``, ``'knitting needle'``, ``'metal hammer'``, ``'slide brush on gong'``, ``'snare stick'``, ``'spoon mallet'``, ``'superball'``, ``'triangle beater'``, ``'triangle beater plain'``, ``'wire brush'``
    

    ``Possible attributes``: ``tip``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTipDirection`

``Possible parents``::obj:`~XMLPercussion`
    """
    
    TYPE = XSDComplexTypeBeater
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='beater'][@type='beater']"


class XMLBeats(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/beats/>`_

The beats element indicates the number of beats, as found in the numerator of a time signature.



``Possible parents``::obj:`~XMLInterchangeable`, :obj:`~XMLTime`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='beats'][@type='xs:string']"


class XMLBend(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/bend/>`_
    
    
    
    ``complexType``: The bend type is used in guitar notation and tablature. A single note with a bend and release will contain two bend elements: the first to represent the bend and the second to represent the release. The shape attribute distinguishes between the angled bend symbols commonly used in standard notation and the curved bend symbols commonly used in both tablature and standard notation.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``first_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``shape``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeBendShape`

    ``Possible children``:    :obj:`~XMLBendAlter`, :obj:`~XMLPreBend`, :obj:`~XMLRelease`, :obj:`~XMLWithBar`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=bend-alter@minOccurs=1@maxOccurs=1
           Choice@minOccurs=0@maxOccurs=1
               Element@name=pre-bend@minOccurs=1@maxOccurs=1
               Element@name=release@minOccurs=1@maxOccurs=1
           Element@name=with-bar@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeBend
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='bend'][@type='bend']"


class XMLBendAlter(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/bend-alter/>`_
    
    The bend-alter element indicates the number of semitones in the bend, similar to the alter element. As with the alter element, numbers like 0.5 can be used to indicate microtones. Negative values indicate pre-bends or releases. The pre-bend and release elements are used to distinguish what is intended. Because the bend-alter element represents the number of steps in the bend, a release after a bend has a negative bend-alter value, not a zero value.
    
    
    
    ``simpleType``: The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.

``Possible parents``::obj:`~XMLBend`
    """
    
    TYPE = XSDSimpleTypeSemitones
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='bend-alter'][@type='semitones']"


class XMLBookmark(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/bookmark/>`_
    
    
    
    ``complexType``: The bookmark type serves as a well-defined target for an incoming simple XLink.

    ``Possible attributes``: ``element``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNMTOKEN`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`\@required, ``name``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``position``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePositiveInteger`

``Possible parents``::obj:`~XMLCredit`, :obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeBookmark
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='bookmark'][@type='bookmark']"


class XMLBottomMargin(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/bottom-margin/>`_
    
    
    
    ``simpleType``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

``Possible parents``::obj:`~XMLPageMargins`
    """
    
    TYPE = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='bottom-margin'][@type='tenths']"


class XMLBracket(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/bracket/>`_
    
    
    
    ``complexType``: Brackets are combined with words in a variety of modern directions. The line-end attribute specifies if there is a jog up or down (or both), an arrow, or nothing at the start or end of the bracket. If the line-end is up or down, the length of the jog can be specified using the end-length attribute. The line-type is solid if not specified.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dash_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``end_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``line_end``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineEnd`\@required, ``line_type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineType`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``space_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStopContinue`\@required

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeBracket
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='bracket'][@type='bracket']"


class XMLBrassBend(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/brass-bend/>`_
    
    The brass-bend element represents the u-shaped bend symbol used in brass notation, distinct from the bend element used in guitar music.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='brass-bend'][@type='empty-placement']"


class XMLBreathMark(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/breath-mark/>`_
    
    
    
    ``complexType``: The breath-mark element indicates a place to take a breath.
    
    ``simpleContent``: The breath-mark-value type represents the symbol used for a breath mark.
        
        Permitted Values: ``''``, ``'comma'``, ``'tick'``, ``'upbow'``, ``'salzedo'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeBreathMark
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='breath-mark'][@type='breath-mark']"


class XMLCaesura(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/caesura/>`_
    
    
    
    ``complexType``: The caesura element indicates a slight pause. It is notated using a "railroad tracks" symbol or other variations specified in the element content.
    
    ``simpleContent``: The caesura-value type represents the shape of the caesura sign.
        
        Permitted Values: ``'normal'``, ``'thick'``, ``'short'``, ``'curved'``, ``'single'``, ``''``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeCaesura
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='caesura'][@type='caesura']"


class XMLCancel(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/cancel/>`_
    
    
    
    ``complexType``: A cancel element indicates that the old key signature should be cancelled before the new one appears. This will always happen when changing to C major or A minor and need not be specified then. The cancel value matches the fifths value of the cancelled key signature (e.g., a cancel of -2 will provide an explicit cancellation for changing from B flat major to F major). The optional location attribute indicates where the cancellation appears relative to the new key signature.
    
    ``simpleContent``: The fifths type represents the number of flats or sharps in a traditional key signature. Negative numbers are used for flats and positive numbers for sharps, reflecting the key's placement within the circle of fifths (hence the type name).

    ``Possible attributes``: ``location``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeCancelLocation`

``Possible parents``::obj:`~XMLKey`
    """
    
    TYPE = XSDComplexTypeCancel
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='cancel'][@type='cancel']"


class XMLCapo(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/capo/>`_

The capo element indicates at which fret a capo should be placed on a fretted instrument. This changes the open tuning of the strings specified by staff-tuning by the specified number of half-steps.



``Possible parents``::obj:`~XMLStaffDetails`
    """
    
    TYPE = XSDSimpleTypeNonNegativeInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='capo'][@type='xs:nonNegativeInteger']"


class XMLChord(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/chord/>`_
    
    The chord element indicates that this note is an additional chord tone with the preceding note.
    
    The duration of a chord note does not move the musical position within a measure. That is done by the duration of the first preceding note without a chord element. Thus the duration of a chord note cannot be longer than the preceding note.
    							
    In most cases the duration will be the same as the preceding note. However it can be shorter in situations such as multiple stops for string instruments.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='chord'][@type='empty']"


class XMLChromatic(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/chromatic/>`_
    
    The chromatic element represents the number of semitones needed to get from written to sounding pitch. This value does not include octave-change values; the values for both elements need to be added to the written pitch to get the correct sounding pitch.
    
    
    
    ``simpleType``: The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.

``Possible parents``::obj:`~XMLPartTranspose`, :obj:`~XMLTranspose`
    """
    
    TYPE = XSDSimpleTypeSemitones
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='chromatic'][@type='semitones']"


class XMLCircularArrow(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/circular-arrow/>`_
    
    
    
    ``simpleType``: The circular-arrow type represents the direction in which a circular arrow points, using Unicode arrow terminology.
        
        Permitted Values: ``'clockwise'``, ``'anticlockwise'``
    

``Possible parents``::obj:`~XMLArrow`
    """
    
    TYPE = XSDSimpleTypeCircularArrow
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='circular-arrow'][@type='circular-arrow']"


class XMLClef(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/clef/>`_
    
    Clefs are represented by a combination of sign, line, and clef-octave-change elements.
    
    
    
    ``complexType``: Clefs are represented by a combination of sign, line, and clef-octave-change elements. The optional number attribute refers to staff numbers within the part. A value of 1 is assumed if not present.
    
    Sometimes clefs are added to the staff in non-standard line positions, either to indicate cue passages, or when there are multiple clefs present simultaneously on one staff. In this situation, the additional attribute is set to "yes" and the line value is ignored. The size attribute is used for clefs where the additional attribute is "yes". It is typically used to indicate cue clefs.
    
    Sometimes clefs at the start of a measure need to appear after the barline rather than before, as for cues or for use after a repeated section. The after-barline attribute is set to "yes" in this situation. The attribute is ignored for mid-measure clefs.
    
    Clefs appear at the start of each system unless the print-object attribute has been set to "no" or the additional attribute has been set to "yes".

    ``Possible attributes``: ``additional``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``after_barline``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffNumber`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSymbolSize`

    ``Possible children``:    :obj:`~XMLClefOctaveChange`, :obj:`~XMLLine`, :obj:`~XMLSign`

    ``XSD structure:``

    .. code-block::

       Group@name=clef@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Element@name=sign@minOccurs=1@maxOccurs=1
               Element@name=line@minOccurs=0@maxOccurs=1
               Element@name=clef-octave-change@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLAttributes`
    """
    
    TYPE = XSDComplexTypeClef
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='clef'][@type='clef']"


class XMLClefOctaveChange(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/clef-octave-change/>`_

The clef-octave-change element is used for transposing clefs. A treble clef for tenors would have a value of -1.



``Possible parents``::obj:`~XMLClef`, :obj:`~XMLPartClef`
    """
    
    TYPE = XSDSimpleTypeInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='clef-octave-change'][@type='xs:integer']"


class XMLCoda(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/coda/>`_
    
    
    
    ``complexType``: The coda type is the visual indicator of a coda sign. The exact glyph can be specified with the smufl attribute. A sound element is also needed to guide playback applications reliably.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflCodaGlyphName`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLBarline`, :obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeCoda
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='coda'][@type='coda']"


class XMLConcertScore(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/concert-score/>`_
    
    The presence of a concert-score element indicates that a score is displayed in concert pitch. It is used for scores that contain parts for transposing instruments.
    
    A document with a concert-score element may not contain any transpose elements that have non-zero values for either the diatonic or chromatic elements. Concert scores may include octave transpositions, so transpose elements with a double element or a non-zero octave-change element value are permitted.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDefaults`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='concert-score'][@type='empty']"


class XMLCreator(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/creator/>`_
    
    The creator element is borrowed from Dublin Core. It is used for the creators of the score. The type attribute is used to distinguish different creative contributions. Thus, there can be multiple creators within an identification. Standard type values are composer, lyricist, and arranger. Other type values may be used for different types of creative roles. The type attribute should usually be used even if there is just a single creator element. The MusicXML format does not use the creator / contributor distinction from Dublin Core.
    
    
    
    ``complexType``: The typed-text type represents a text element with a type attribute.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLIdentification`
    """
    
    TYPE = XSDComplexTypeTypedText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='creator'][@type='typed-text']"


class XMLCredit(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/credit/>`_
    
    
    
    ``complexType``: The credit type represents the appearance of the title, composer, arranger, lyricist, copyright, dedication, and other text, symbols, and graphics that commonly appear on the first page of a score. The credit-words, credit-symbol, and credit-image elements are similar to the words, symbol, and image elements for directions. However, since the credit is not part of a measure, the default-x and default-y attributes adjust the origin relative to the bottom left-hand corner of the page. The enclosure for credit-words and credit-symbol is none by default.
    
    By default, a series of credit-words and credit-symbol elements within a single credit element follow one another in sequence visually. Non-positional formatting attributes are carried over from the previous element by default.
    
    The page attribute for the credit element specifies the page number where the credit should appear. This is an integer value that starts with 1 for the first page. Its value is 1 by default. Since credits occur before the music, these page numbers do not refer to the page numbering specified by the print element's page-number attribute.
    
    The credit-type element indicates the purpose behind a credit. Multiple types of data may be combined in a single credit, so multiple elements may be used. Standard values include page number, title, subtitle, composer, arranger, lyricist, rights, and part name.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``page``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePositiveInteger`

    ``Possible children``:    :obj:`~XMLBookmark`, :obj:`~XMLCreditImage`, :obj:`~XMLCreditSymbol`, :obj:`~XMLCreditType`, :obj:`~XMLCreditWords`, :obj:`~XMLLink`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=credit-type@minOccurs=0@maxOccurs=unbounded
           Element@name=link@minOccurs=0@maxOccurs=unbounded
           Element@name=bookmark@minOccurs=0@maxOccurs=unbounded
           Choice@minOccurs=1@maxOccurs=1
               Element@name=credit-image@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Choice@minOccurs=1@maxOccurs=1
                       Element@name=credit-words@minOccurs=1@maxOccurs=1
                       Element@name=credit-symbol@minOccurs=1@maxOccurs=1
                   Sequence@minOccurs=0@maxOccurs=unbounded
                       Element@name=link@minOccurs=0@maxOccurs=unbounded
                       Element@name=bookmark@minOccurs=0@maxOccurs=unbounded
                       Choice@minOccurs=1@maxOccurs=1
                           Element@name=credit-words@minOccurs=1@maxOccurs=1
                           Element@name=credit-symbol@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLScorePartwise`
    """
    
    TYPE = XSDComplexTypeCredit
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='credit'][@type='credit']"


class XMLCreditImage(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/credit-image/>`_
    
    
    
    ``complexType``: The image type is used to include graphical images in a score.

``Possible parents``::obj:`~XMLCredit`
    """
    
    TYPE = XSDComplexTypeImage
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='credit-image'][@type='image']"


class XMLCreditSymbol(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/credit-symbol/>`_
    
    
    
    ``complexType``: The formatted-symbol-id type represents a SMuFL musical symbol element with formatting and id attributes.
    
    ``simpleContent``: The smufl-glyph-name type is used for attributes that reference a specific Standard Music Font Layout (SMuFL) character. The value is a SMuFL canonical glyph name, not a code point. For instance, the value for a standard piano pedal mark would be keyboardPedalPed, not U+E650.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``dir``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTextDirection`, ``enclosure``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeEnclosureShape`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``justify``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``letter_spacing``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOrNormal`, ``line_height``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOrNormal`, ``line_through``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOfLines`, ``overline``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOfLines`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``rotation``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeRotationDegrees`, ``underline``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOfLines`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLCredit`
    """
    
    TYPE = XSDComplexTypeFormattedSymbolId
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='credit-symbol'][@type='formatted-symbol-id']"


class XMLCreditType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/credit-type/>`_



``Possible parents``::obj:`~XMLCredit`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='credit-type'][@type='xs:string']"


class XMLCreditWords(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/credit-words/>`_
    
    
    
    ``complexType``: The formatted-text-id type represents a text element with text-formatting and id attributes.

``Possible parents``::obj:`~XMLCredit`
    """
    
    TYPE = XSDComplexTypeFormattedTextId
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='credit-words'][@type='formatted-text-id']"


class XMLCue(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/cue/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='cue'][@type='empty']"


class XMLDamp(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/damp/>`_
    
    The damp element specifies a harp damping mark.
    
    
    
    ``complexType``: The empty-print-style-align-id type represents an empty element with print-style-align and optional-unique-id attribute groups.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeEmptyPrintStyleAlignId
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='damp'][@type='empty-print-style-align-id']"


class XMLDampAll(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/damp-all/>`_
    
    The damp-all element specifies a harp damping mark for all strings.
    
    
    
    ``complexType``: The empty-print-style-align-id type represents an empty element with print-style-align and optional-unique-id attribute groups.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeEmptyPrintStyleAlignId
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='damp-all'][@type='empty-print-style-align-id']"


class XMLDashes(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/dashes/>`_
    
    
    
    ``complexType``: The dashes type represents dashes, used for instance with cresc. and dim. marks.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dash_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``space_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStopContinue`\@required

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeDashes
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='dashes'][@type='dashes']"


class XMLDefaults(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/defaults/>`_
    
    
    
    ``complexType``: The defaults type specifies score-wide defaults for scaling; whether or not the file is a concert score; layout; and default values for the music font, word font, lyric font, and lyric language. Except for the concert-score element, if any defaults are missing, the choice of what to use is determined by the application.

    ``Possible children``:    :obj:`~XMLAppearance`, :obj:`~XMLConcertScore`, :obj:`~XMLLyricFont`, :obj:`~XMLLyricLanguage`, :obj:`~XMLMusicFont`, :obj:`~XMLPageLayout`, :obj:`~XMLScaling`, :obj:`~XMLStaffLayout`, :obj:`~XMLSystemLayout`, :obj:`~XMLWordFont`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=scaling@minOccurs=0@maxOccurs=1
           Element@name=concert-score@minOccurs=0@maxOccurs=1
           Group@name=layout@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=page-layout@minOccurs=0@maxOccurs=1
                   Element@name=system-layout@minOccurs=0@maxOccurs=1
                   Element@name=staff-layout@minOccurs=0@maxOccurs=unbounded
           Element@name=appearance@minOccurs=0@maxOccurs=1
           Element@name=music-font@minOccurs=0@maxOccurs=1
           Element@name=word-font@minOccurs=0@maxOccurs=1
           Element@name=lyric-font@minOccurs=0@maxOccurs=unbounded
           Element@name=lyric-language@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLScorePartwise`
    """
    
    TYPE = XSDComplexTypeDefaults
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='defaults'][@type='defaults']"


class XMLDegree(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/degree/>`_
    
    
    
    ``complexType``: The degree type is used to add, alter, or subtract individual notes in the chord. The print-object attribute can be used to keep the degree from printing separately when it has already taken into account in the text attribute of the kind element. The degree-value and degree-type text attributes specify how the value and type of the degree should be displayed.
    
    A harmony of kind "other" can be spelled explicitly by using a series of degree elements together with a root.

    ``Possible attributes``: ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

    ``Possible children``:    :obj:`~XMLDegreeAlter`, :obj:`~XMLDegreeType`, :obj:`~XMLDegreeValue`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=degree-value@minOccurs=1@maxOccurs=1
           Element@name=degree-alter@minOccurs=1@maxOccurs=1
           Element@name=degree-type@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLHarmony`
    """
    
    TYPE = XSDComplexTypeDegree
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='degree'][@type='degree']"


class XMLDegreeAlter(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/degree-alter/>`_
    
    
    
    ``complexType``: The degree-alter type represents the chromatic alteration for the current degree. If the degree-type value is alter or subtract, the degree-alter value is relative to the degree already in the chord based on its kind element. If the degree-type value is add, the degree-alter is relative to a dominant chord (major and perfect intervals except for a minor seventh). The plus-minus attribute is used to indicate if plus and minus symbols should be used instead of sharp and flat symbols to display the degree alteration. It is no if not specified.
    
    ``simpleContent``: The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``plus_minus``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLDegree`
    """
    
    TYPE = XSDComplexTypeDegreeAlter
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='degree-alter'][@type='degree-alter']"


class XMLDegreeType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/degree-type/>`_
    
    
    
    ``complexType``: The degree-type type indicates if this degree is an addition, alteration, or subtraction relative to the kind of the current chord. The value of the degree-type element affects the interpretation of the value of the degree-alter element. The text attribute specifies how the type of the degree should be displayed.
    
    ``simpleContent``: The degree-type-value type indicates whether the current degree element is an addition, alteration, or subtraction to the kind of the current chord in the harmony element.
        
        Permitted Values: ``'add'``, ``'alter'``, ``'subtract'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``text``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLDegree`
    """
    
    TYPE = XSDComplexTypeDegreeType
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='degree-type'][@type='degree-type']"


class XMLDegreeValue(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/degree-value/>`_
    
    
    
    ``complexType``: The content of the degree-value type is a number indicating the degree of the chord (1 for the root, 3 for third, etc). The text attribute specifies how the value of the degree should be displayed. The symbol attribute indicates that a symbol should be used in specifying the degree. If the symbol attribute is present, the value of the text attribute follows the symbol.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``symbol``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeDegreeSymbolValue`, ``text``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLDegree`
    """
    
    TYPE = XSDComplexTypeDegreeValue
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='degree-value'][@type='degree-value']"


class XMLDelayedInvertedTurn(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/delayed-inverted-turn/>`_
    
    The delayed-inverted-turn element indicates an inverted turn that is delayed until the end of the current note.
    
    
    
    ``complexType``: The horizontal-turn type represents turn elements that are horizontal rather than vertical. These are empty elements with print-style, placement, trill-sound, and slash attributes. If the slash attribute is yes, then a vertical line is used to slash the turn. It is no if not specified.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``second_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``slash``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``start_note``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartNote`, ``trill_step``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillStep`, ``two_note_turn``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTwoNoteTurn`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeHorizontalTurn
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='delayed-inverted-turn'][@type='horizontal-turn']"


class XMLDelayedTurn(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/delayed-turn/>`_
    
    The delayed-turn element indicates a normal turn that is delayed until the end of the current note.
    
    
    
    ``complexType``: The horizontal-turn type represents turn elements that are horizontal rather than vertical. These are empty elements with print-style, placement, trill-sound, and slash attributes. If the slash attribute is yes, then a vertical line is used to slash the turn. It is no if not specified.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``second_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``slash``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``start_note``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartNote`, ``trill_step``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillStep`, ``two_note_turn``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTwoNoteTurn`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeHorizontalTurn
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='delayed-turn'][@type='horizontal-turn']"


class XMLDetachedLegato(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/detached-legato/>`_
    
    The detached-legato element indicates the combination of a tenuto line and staccato dot symbol.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='detached-legato'][@type='empty-placement']"


class XMLDiatonic(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/diatonic/>`_

The diatonic element specifies the number of pitch steps needed to go from written to sounding pitch. This allows for correct spelling of enharmonic transpositions. This value does not include octave-change values; the values for both elements need to be added to the written pitch to get the correct sounding pitch.



``Possible parents``::obj:`~XMLPartTranspose`, :obj:`~XMLTranspose`
    """
    
    TYPE = XSDSimpleTypeInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='diatonic'][@type='xs:integer']"


class XMLDirection(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/direction/>`_
    
    
    
    ``complexType``: A direction is a musical indication that is not necessarily attached to a specific note. Two or more may be combined to indicate words followed by the start of a dashed line, the end of a wedge followed by dynamics, etc. For applications where a specific direction is indeed attached to a specific note, the direction element can be associated with the first note element that follows it in score order that is not in a different voice.
    
    By default, a series of direction-type elements and a series of child elements of a direction-type within a single direction element follow one another in sequence visually. For a series of direction-type children, non-positional formatting attributes are carried over from the previous element by default.

    ``Possible attributes``: ``directive``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``system``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSystemRelation`

    ``Possible children``:    :obj:`~XMLDirectionType`, :obj:`~XMLFootnote`, :obj:`~XMLLevel`, :obj:`~XMLListening`, :obj:`~XMLOffset`, :obj:`~XMLSound`, :obj:`~XMLStaff`, :obj:`~XMLVoice`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=direction-type@minOccurs=1@maxOccurs=unbounded
           Element@name=offset@minOccurs=0@maxOccurs=1
           Group@name=editorial-voice-direction@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=footnote@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=footnote@minOccurs=1@maxOccurs=1
                   Group@name=level@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=level@minOccurs=1@maxOccurs=1
                   Group@name=voice@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=voice@minOccurs=1@maxOccurs=1
           Group@name=staff@minOccurs=0@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=staff@minOccurs=1@maxOccurs=1
           Element@name=sound@minOccurs=0@maxOccurs=1
           Element@name=listening@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeDirection
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='direction'][@type='direction']"


class XMLDirectionType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/direction-type/>`_
    
    
    
    ``complexType``: Textual direction types may have more than 1 component due to multiple fonts. The dynamics element may also be used in the notations element. Attribute groups related to print suggestions apply to the individual direction-type, not to the overall direction.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`

    ``Possible children``:    :obj:`~XMLAccordionRegistration`, :obj:`~XMLBracket`, :obj:`~XMLCoda`, :obj:`~XMLDampAll`, :obj:`~XMLDamp`, :obj:`~XMLDashes`, :obj:`~XMLDynamics`, :obj:`~XMLEyeglasses`, :obj:`~XMLHarpPedals`, :obj:`~XMLImage`, :obj:`~XMLMetronome`, :obj:`~XMLOctaveShift`, :obj:`~XMLOtherDirection`, :obj:`~XMLPedal`, :obj:`~XMLPercussion`, :obj:`~XMLPrincipalVoice`, :obj:`~XMLRehearsal`, :obj:`~XMLScordatura`, :obj:`~XMLSegno`, :obj:`~XMLStaffDivide`, :obj:`~XMLStringMute`, :obj:`~XMLSymbol`, :obj:`~XMLWedge`, :obj:`~XMLWords`

    ``XSD structure:``

    .. code-block::

       Choice@minOccurs=1@maxOccurs=1
           Element@name=rehearsal@minOccurs=1@maxOccurs=unbounded
           Element@name=segno@minOccurs=1@maxOccurs=unbounded
           Element@name=coda@minOccurs=1@maxOccurs=unbounded
           Choice@minOccurs=1@maxOccurs=unbounded
               Element@name=words@minOccurs=1@maxOccurs=1
               Element@name=symbol@minOccurs=1@maxOccurs=1
           Element@name=wedge@minOccurs=1@maxOccurs=1
           Element@name=dynamics@minOccurs=1@maxOccurs=unbounded
           Element@name=dashes@minOccurs=1@maxOccurs=1
           Element@name=bracket@minOccurs=1@maxOccurs=1
           Element@name=pedal@minOccurs=1@maxOccurs=1
           Element@name=metronome@minOccurs=1@maxOccurs=1
           Element@name=octave-shift@minOccurs=1@maxOccurs=1
           Element@name=harp-pedals@minOccurs=1@maxOccurs=1
           Element@name=damp@minOccurs=1@maxOccurs=1
           Element@name=damp-all@minOccurs=1@maxOccurs=1
           Element@name=eyeglasses@minOccurs=1@maxOccurs=1
           Element@name=string-mute@minOccurs=1@maxOccurs=1
           Element@name=scordatura@minOccurs=1@maxOccurs=1
           Element@name=image@minOccurs=1@maxOccurs=1
           Element@name=principal-voice@minOccurs=1@maxOccurs=1
           Element@name=percussion@minOccurs=1@maxOccurs=unbounded
           Element@name=accordion-registration@minOccurs=1@maxOccurs=1
           Element@name=staff-divide@minOccurs=1@maxOccurs=1
           Element@name=other-direction@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLDirection`
    """
    
    TYPE = XSDComplexTypeDirectionType
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='direction-type'][@type='direction-type']"


class XMLDirective(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/directive/>`_

Directives are like directions, but can be grouped together with attributes for convenience. This is typically used for tempo markings at the beginning of a piece of music. This element was deprecated in Version 2.0 in favor of the direction element's directive attribute. Language names come from ISO 639, with optional country subcodes from ISO 3166.



    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``lang``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLanguage`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLAttributes`
    """
    
    TYPE = XSDComplexTypeDirective
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='attributes']//{*}element[@name='directive']"


class XMLDisplayOctave(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/display-octave/>`_
    
    
    
    ``simpleType``: Octaves are represented by the numbers 0 to 9, where 4 indicates the octave started by middle C.

``Possible parents``::obj:`~XMLRest`, :obj:`~XMLUnpitched`
    """
    
    TYPE = XSDSimpleTypeOctave
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='display-octave'][@type='octave']"


class XMLDisplayStep(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/display-step/>`_
    
    
    
    ``simpleType``: The step type represents a step of the diatonic scale, represented using the English letters A through G.
        
        Permitted Values: ``'A'``, ``'B'``, ``'C'``, ``'D'``, ``'E'``, ``'F'``, ``'G'``
    

``Possible parents``::obj:`~XMLRest`, :obj:`~XMLUnpitched`
    """
    
    TYPE = XSDSimpleTypeStep
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='display-step'][@type='step']"


class XMLDisplayText(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/display-text/>`_
    
    
    
    ``complexType``: The formatted-text type represents a text element with text-formatting attributes.

``Possible parents``::obj:`~XMLGroupAbbreviationDisplay`, :obj:`~XMLGroupNameDisplay`, :obj:`~XMLNoteheadText`, :obj:`~XMLPartAbbreviationDisplay`, :obj:`~XMLPartNameDisplay`
    """
    
    TYPE = XSDComplexTypeFormattedText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='display-text'][@type='formatted-text']"


class XMLDistance(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/distance/>`_
    
    
    
    ``complexType``: The distance element represents standard distances between notation elements in tenths. The type attribute defines what type of distance is being defined. Valid values include hyphen (for hyphens in lyrics) and beam.
    
    ``simpleContent``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeDistanceType`\@required

``Possible parents``::obj:`~XMLAppearance`
    """
    
    TYPE = XSDComplexTypeDistance
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='distance'][@type='distance']"


class XMLDivisions(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/divisions/>`_
    
    Musical notation duration is commonly represented as fractions. The divisions element indicates how many divisions per quarter note are used to indicate a note's duration. For example, if duration = 1 and divisions = 2, this is an eighth note duration. Duration and divisions are used directly for generating sound output, so they must be chosen to take tuplets into account. Using a divisions element lets us use just one number to represent a duration for each note in the score, while retaining the full power of a fractional representation. If maximum compatibility with Standard MIDI 1.0 files is important, do not have the divisions value exceed 16383.
    
    
    
    ``simpleType``: The positive-divisions type restricts divisions values to positive numbers.

``Possible parents``::obj:`~XMLAttributes`
    """
    
    TYPE = XSDSimpleTypePositiveDivisions
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='divisions'][@type='positive-divisions']"


class XMLDoit(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/doit/>`_
    
    The doit element is an indeterminate slide attached to a single note. The doit appears after the main note and goes above the main pitch.
    
    
    
    ``complexType``: The empty-line type represents an empty element with line-shape, line-type, line-length, dashed-formatting, print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dash_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``line_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineLength`, ``line_shape``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineShape`, ``line_type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineType`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``space_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyLine
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='doit'][@type='empty-line']"


class XMLDot(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/dot/>`_
    
    One dot element is used for each dot of prolongation. The placement attribute is used to specify whether the dot should appear above or below the staff line. It is ignored for notes that appear on a staff space.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='dot'][@type='empty-placement']"


class XMLDouble(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/double/>`_
    
    If the double element is present, it indicates that the music is doubled one octave from what is currently written.
    
    
    
    ``complexType``: The double type indicates that the music is doubled one octave from what is currently written. If the above attribute is set to yes, the doubling is one octave above what is written, as for mixed flute / piccolo parts in band literature. Otherwise the doubling is one octave below what is written, as for mixed cello / bass parts in orchestral literature.

    ``Possible attributes``: ``above``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

``Possible parents``::obj:`~XMLPartTranspose`, :obj:`~XMLTranspose`
    """
    
    TYPE = XSDComplexTypeDouble
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='double'][@type='double']"


class XMLDoubleTongue(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/double-tongue/>`_
    
    The double-tongue element represents the double tongue symbol (two dots arranged horizontally).
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='double-tongue'][@type='empty-placement']"


class XMLDownBow(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/down-bow/>`_
    
    The down-bow element represents the symbol that is used both for down-bowing on bowed instruments, and down-stroke on plucked instruments.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='down-bow'][@type='empty-placement']"


class XMLDuration(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/duration/>`_
    
    Duration is a positive number specified in division units. This is the intended duration vs. notated duration (for instance, differences in dotted notes in Baroque-era music). Differences in duration specific to an interpretation or performance should be represented using the note element's attack and release attributes.
    
    The duration element moves the musical position when used in backup elements, forward elements, and note elements that do not contain a chord child element.
    
    
    
    ``simpleType``: The positive-divisions type restricts divisions values to positive numbers.

``Possible parents``::obj:`~XMLBackup`, :obj:`~XMLFiguredBass`, :obj:`~XMLForward`, :obj:`~XMLNote`
    """
    
    TYPE = XSDSimpleTypePositiveDivisions
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='duration'][@type='positive-divisions']"


class XMLDynamics(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/dynamics/>`_
    
    
    
    ``complexType``: Dynamics can be associated either with a note or a general musical direction. To avoid inconsistencies between and amongst the letter abbreviations for dynamics (what is sf vs. sfz, standing alone or with a trailing dynamic that is not always piano), we use the actual letters as the names of these dynamic elements. The other-dynamics element allows other dynamic marks that are not covered here. Dynamics elements may also be combined to create marks not covered by a single element, such as sfmp.
    
    These letter dynamic symbols are separated from crescendo, decrescendo, and wedge indications. Dynamic representation is inconsistent in scores. Many things are assumed by the composer and left out, such as returns to original dynamics. The MusicXML format captures what is in the score, but does not try to be optimal for analysis or synthesis of dynamics.
    
    The placement attribute is used when the dynamics are associated with a note. It is ignored when the dynamics are associated with a direction. In that case the direction element's placement attribute is used instead.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``enclosure``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeEnclosureShape`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``line_through``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOfLines`, ``overline``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOfLines`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``underline``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOfLines`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

    ``Possible children``:    :obj:`~XMLF`, :obj:`~XMLFf`, :obj:`~XMLFff`, :obj:`~XMLFfff`, :obj:`~XMLFffff`, :obj:`~XMLFfffff`, :obj:`~XMLFp`, :obj:`~XMLFz`, :obj:`~XMLMf`, :obj:`~XMLMp`, :obj:`~XMLN`, :obj:`~XMLOtherDynamics`, :obj:`~XMLP`, :obj:`~XMLPf`, :obj:`~XMLPp`, :obj:`~XMLPpp`, :obj:`~XMLPppp`, :obj:`~XMLPpppp`, :obj:`~XMLPppppp`, :obj:`~XMLRf`, :obj:`~XMLRfz`, :obj:`~XMLSf`, :obj:`~XMLSffz`, :obj:`~XMLSfp`, :obj:`~XMLSfpp`, :obj:`~XMLSfz`, :obj:`~XMLSfzp`

    ``XSD structure:``

    .. code-block::

       Choice@minOccurs=0@maxOccurs=unbounded
           Element@name=p@minOccurs=1@maxOccurs=1
           Element@name=pp@minOccurs=1@maxOccurs=1
           Element@name=ppp@minOccurs=1@maxOccurs=1
           Element@name=pppp@minOccurs=1@maxOccurs=1
           Element@name=ppppp@minOccurs=1@maxOccurs=1
           Element@name=pppppp@minOccurs=1@maxOccurs=1
           Element@name=f@minOccurs=1@maxOccurs=1
           Element@name=ff@minOccurs=1@maxOccurs=1
           Element@name=fff@minOccurs=1@maxOccurs=1
           Element@name=ffff@minOccurs=1@maxOccurs=1
           Element@name=fffff@minOccurs=1@maxOccurs=1
           Element@name=ffffff@minOccurs=1@maxOccurs=1
           Element@name=mp@minOccurs=1@maxOccurs=1
           Element@name=mf@minOccurs=1@maxOccurs=1
           Element@name=sf@minOccurs=1@maxOccurs=1
           Element@name=sfp@minOccurs=1@maxOccurs=1
           Element@name=sfpp@minOccurs=1@maxOccurs=1
           Element@name=fp@minOccurs=1@maxOccurs=1
           Element@name=rf@minOccurs=1@maxOccurs=1
           Element@name=rfz@minOccurs=1@maxOccurs=1
           Element@name=sfz@minOccurs=1@maxOccurs=1
           Element@name=sffz@minOccurs=1@maxOccurs=1
           Element@name=fz@minOccurs=1@maxOccurs=1
           Element@name=n@minOccurs=1@maxOccurs=1
           Element@name=pf@minOccurs=1@maxOccurs=1
           Element@name=sfzp@minOccurs=1@maxOccurs=1
           Element@name=other-dynamics@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLDirectionType`, :obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeDynamics
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='dynamics'][@type='dynamics']"


class XMLEffect(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/effect/>`_
    
    
    
    ``complexType``: The effect type represents pictograms for sound effect percussion instruments. The smufl attribute is used to distinguish different SMuFL stylistic alternates.
    
    ``simpleContent``: The effect-value type represents pictograms for sound effect percussion instruments. The cannon, lotus flute, and megaphone values are in addition to Stone's list.
        
        Permitted Values: ``'anvil'``, ``'auto horn'``, ``'bird whistle'``, ``'cannon'``, ``'duck call'``, ``'gun shot'``, ``'klaxon horn'``, ``'lions roar'``, ``'lotus flute'``, ``'megaphone'``, ``'police whistle'``, ``'siren'``, ``'slide whistle'``, ``'thunder sheet'``, ``'wind machine'``, ``'wind whistle'``
    

    ``Possible attributes``: ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflPictogramGlyphName`

``Possible parents``::obj:`~XMLPercussion`
    """
    
    TYPE = XSDComplexTypeEffect
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='effect'][@type='effect']"


class XMLElevation(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/elevation/>`_
    
    The elevation and pan elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For elevation, 0 is level with the listener, 90 is directly above, and -90 is directly below.
    
    
    
    ``simpleType``: The rotation-degrees type specifies rotation, pan, and elevation values in degrees. Values range from -180 to 180.

``Possible parents``::obj:`~XMLMidiInstrument`
    """
    
    TYPE = XSDSimpleTypeRotationDegrees
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='elevation'][@type='rotation-degrees']"


class XMLElision(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/elision/>`_
    
    
    
    ``complexType``: The elision type represents an elision between lyric syllables. The text content specifies the symbol used to display the elision. Common values are a no-break space (Unicode 00A0), an underscore (Unicode 005F), or an undertie (Unicode 203F). If the text content is empty, the smufl attribute is used to specify the symbol to use. Its value is a SMuFL canonical glyph name that starts with lyrics. The SMuFL attribute is ignored if the elision glyph is already specified by the text content. If neither text content nor a smufl attribute are present, the elision glyph is application-specific.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflLyricsGlyphName`

``Possible parents``::obj:`~XMLLyric`
    """
    
    TYPE = XSDComplexTypeElision
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='elision'][@type='elision']"


class XMLEncoder(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/encoder/>`_
    
    
    
    ``complexType``: The typed-text type represents a text element with a type attribute.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLEncoding`
    """
    
    TYPE = XSDComplexTypeTypedText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='encoder'][@type='typed-text']"


class XMLEncoding(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/encoding/>`_
    
    
    
    ``complexType``: The encoding element contains information about who did the digital encoding, when, with what software, and in what aspects. Standard type values for the encoder element are music, words, and arrangement, but other types may be used. The type attribute is only needed when there are multiple encoder elements.

    ``Possible children``:    :obj:`~XMLEncoder`, :obj:`~XMLEncodingDate`, :obj:`~XMLEncodingDescription`, :obj:`~XMLSoftware`, :obj:`~XMLSupports`

    ``XSD structure:``

    .. code-block::

       Choice@minOccurs=0@maxOccurs=unbounded
           Element@name=encoding-date@minOccurs=1@maxOccurs=1
           Element@name=encoder@minOccurs=1@maxOccurs=1
           Element@name=software@minOccurs=1@maxOccurs=1
           Element@name=encoding-description@minOccurs=1@maxOccurs=1
           Element@name=supports@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLIdentification`
    """
    
    TYPE = XSDComplexTypeEncoding
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='encoding'][@type='encoding']"


class XMLEncodingDate(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/encoding-date/>`_
    
    
    
    ``simpleType``: Calendar dates are represented yyyy-mm-dd format, following ISO 8601. This is a W3C XML Schema date type, but without the optional timezone data.
        
            
    Pattern: [^:Z]*
    

``Possible parents``::obj:`~XMLEncoding`
    """
    
    TYPE = XSDSimpleTypeYyyyMmDd
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='encoding-date'][@type='yyyy-mm-dd']"


class XMLEncodingDescription(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/encoding-description/>`_



``Possible parents``::obj:`~XMLEncoding`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='encoding-description'][@type='xs:string']"


class XMLEndLine(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/end-line/>`_
    
    The end-line element comes from RP-017 for Standard MIDI File Lyric meta-events. It facilitates lyric display for Karaoke and similar applications.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLLyric`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='end-line'][@type='empty']"


class XMLEndParagraph(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/end-paragraph/>`_
    
    The end-paragraph element comes from RP-017 for Standard MIDI File Lyric meta-events. It facilitates lyric display for Karaoke and similar applications.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLLyric`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='end-paragraph'][@type='empty']"


class XMLEnding(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/ending/>`_
    
    
    
    ``complexType``: The ending type represents multiple (e.g. first and second) endings. Typically, the start type is associated with the left barline of the first measure in an ending. The stop and discontinue types are associated with the right barline of the last measure in an ending. Stop is used when the ending mark concludes with a downward jog, as is typical for first endings. Discontinue is used when there is no downward jog, as is typical for second endings that do not conclude a piece. The length of the jog can be specified using the end-length attribute. The text-x and text-y attributes are offsets that specify where the baseline of the start of the ending text appears, relative to the start of the ending line.
    
    The number attribute indicates which times the ending is played, similar to the time-only attribute used by other elements. While this often represents the numeric values for what is under the ending line, it can also indicate whether an ending is played during a larger dal segno or da capo repeat. Single endings such as "1" or comma-separated multiple endings such as "1,2" may be used. The ending element text is used when the text displayed in the ending is different than what appears in the number attribute. The print-object attribute is used to indicate when an ending is present but not printed, as is often the case for many parts in a full score.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``end_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeEndingNumber`\@required, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``system``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSystemRelation`, ``text_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``text_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStopDiscontinue`\@required

``Possible parents``::obj:`~XMLBarline`
    """
    
    TYPE = XSDComplexTypeEnding
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='ending'][@type='ending']"


class XMLEnsemble(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/ensemble/>`_
    
    The ensemble element is present if performance is intended by an ensemble such as an orchestral section. The text of the ensemble element contains the size of the section, or is empty if the ensemble size is not specified.
    
    
    
    ``simpleType``: The positive-integer-or-empty values can be either a positive integer or an empty string.
    
        .. todo::
           Better documentation.
        

``Possible parents``::obj:`~XMLInstrumentChange`, :obj:`~XMLScoreInstrument`
    """
    
    TYPE = XSDSimpleTypePositiveIntegerOrEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='ensemble'][@type='positive-integer-or-empty']"


class XMLExceptVoice(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/except-voice/>`_

The except-voice element is used to specify a combination of slash notation and regular notation. Any note elements that are in voices specified by the except-voice elements are displayed in normal notation, in addition to the slash notation that is always displayed.



``Possible parents``::obj:`~XMLBeatRepeat`, :obj:`~XMLSlash`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='except-voice'][@type='xs:string']"


class XMLExtend(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/extend/>`_
    
    
    
    ``complexType``: The extend type represents lyric word extension / melisma lines as well as figured bass extensions. The optional type and position attributes are added in Version 3.0 to provide better formatting control.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStopContinue`

``Possible parents``::obj:`~XMLFigure`, :obj:`~XMLLyric`
    """
    
    TYPE = XSDComplexTypeExtend
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='extend'][@type='extend']"


class XMLEyeglasses(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/eyeglasses/>`_
    
    The eyeglasses element represents the eyeglasses symbol, common in commercial music.
    
    
    
    ``complexType``: The empty-print-style-align-id type represents an empty element with print-style-align and optional-unique-id attribute groups.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeEmptyPrintStyleAlignId
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='eyeglasses'][@type='empty-print-style-align-id']"


class XMLF(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/f/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='f'][@type='empty']"


class XMLFalloff(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/falloff/>`_
    
    The falloff element is an indeterminate slide attached to a single note. The falloff appears after the main note and goes below the main pitch.
    
    
    
    ``complexType``: The empty-line type represents an empty element with line-shape, line-type, line-length, dashed-formatting, print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dash_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``line_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineLength`, ``line_shape``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineShape`, ``line_type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineType`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``space_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyLine
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='falloff'][@type='empty-line']"


class XMLFeature(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/feature/>`_
    
    
    
    ``complexType``: The feature type is a part of the grouping element used for musical analysis. The type attribute represents the type of the feature and the element content represents its value. This type is flexible to allow for different analyses.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLGrouping`
    """
    
    TYPE = XSDComplexTypeFeature
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='feature'][@type='feature']"


class XMLFermata(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/fermata/>`_
    
    
    
    ``complexType``: The fermata text content represents the shape of the fermata sign. An empty fermata element represents a normal fermata. The fermata type is upright if not specified.
    
    ``simpleContent``: The fermata-shape type represents the shape of the fermata sign. The empty value is equivalent to the normal value.
        
        Permitted Values: ``'normal'``, ``'angled'``, ``'square'``, ``'double-angled'``, ``'double-square'``, ``'double-dot'``, ``'half-curve'``, ``'curlew'``, ``''``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeUprightInverted`

``Possible parents``::obj:`~XMLBarline`, :obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeFermata
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='fermata'][@type='fermata']"


class XMLFf(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/ff/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='ff'][@type='empty']"


class XMLFff(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/fff/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='fff'][@type='empty']"


class XMLFfff(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/ffff/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='ffff'][@type='empty']"


class XMLFffff(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/fffff/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='fffff'][@type='empty']"


class XMLFfffff(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/ffffff/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='ffffff'][@type='empty']"


class XMLFifths(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/fifths/>`_
    
    
    
    ``simpleType``: The fifths type represents the number of flats or sharps in a traditional key signature. Negative numbers are used for flats and positive numbers for sharps, reflecting the key's placement within the circle of fifths (hence the type name).

``Possible parents``::obj:`~XMLKey`
    """
    
    TYPE = XSDSimpleTypeFifths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='fifths'][@type='fifths']"


class XMLFigure(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/figure/>`_
    
    
    
    ``complexType``: The figure type represents a single figure within a figured-bass element.

    ``Possible children``:    :obj:`~XMLExtend`, :obj:`~XMLFigureNumber`, :obj:`~XMLFootnote`, :obj:`~XMLLevel`, :obj:`~XMLPrefix`, :obj:`~XMLSuffix`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=prefix@minOccurs=0@maxOccurs=1
           Element@name=figure-number@minOccurs=0@maxOccurs=1
           Element@name=suffix@minOccurs=0@maxOccurs=1
           Element@name=extend@minOccurs=0@maxOccurs=1
           Group@name=editorial@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=footnote@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=footnote@minOccurs=1@maxOccurs=1
                   Group@name=level@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=level@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLFiguredBass`
    """
    
    TYPE = XSDComplexTypeFigure
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='figure'][@type='figure']"


class XMLFigureNumber(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/figure-number/>`_
    
    A figure-number is a number. Overstrikes of the figure number are represented in the suffix element.
    
    
    
    ``complexType``: The style-text type represents a text element with a print-style attribute group.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLFigure`
    """
    
    TYPE = XSDComplexTypeStyleText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='figure-number'][@type='style-text']"


class XMLFiguredBass(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/figured-bass/>`_
    
    
    
    ``complexType``: The figured-bass element represents figured bass notation. Figured bass elements take their position from the first regular note (not a grace note or chord note) that follows in score order. The optional duration element is used to indicate changes of figures under a note.
    
    Figures are ordered from top to bottom. The value of parentheses is "no" if not present.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``parentheses``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``print_dot``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``print_lyric``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``print_spacing``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

    ``Possible children``:    :obj:`~XMLDuration`, :obj:`~XMLFigure`, :obj:`~XMLFootnote`, :obj:`~XMLLevel`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=figure@minOccurs=1@maxOccurs=unbounded
           Group@name=duration@minOccurs=0@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=duration@minOccurs=1@maxOccurs=1
           Group@name=editorial@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=footnote@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=footnote@minOccurs=1@maxOccurs=1
                   Group@name=level@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=level@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeFiguredBass
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='figured-bass'][@type='figured-bass']"


class XMLFingering(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/fingering/>`_
    
    
    
    ``complexType``: Fingering is typically indicated 1,2,3,4,5. Multiple fingerings may be given, typically to substitute fingerings in the middle of a note. The substitution and alternate values are "no" if the attribute is not present. For guitar and other fretted instruments, the fingering element represents the fretting finger; the pluck element represents the plucking finger.

    ``Possible attributes``: ``alternate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``substitution``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

``Possible parents``::obj:`~XMLFrameNote`, :obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeFingering
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='fingering'][@type='fingering']"


class XMLFingernails(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/fingernails/>`_
    
    The fingernails element is used in notation for harp and other plucked string instruments.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='fingernails'][@type='empty-placement']"


class XMLFirst(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/first/>`_



``Possible parents``::obj:`~XMLSwing`
    """
    
    TYPE = XSDSimpleTypePositiveInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='first'][@type='xs:positiveInteger']"


class XMLFirstFret(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/first-fret/>`_
    
    
    
    ``complexType``: The first-fret type indicates which fret is shown in the top space of the frame; it is fret 1 if the element is not present. The optional text attribute indicates how this is represented in the fret diagram, while the location attribute indicates whether the text appears to the left or right of the frame.

    ``Possible attributes``: ``location``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftRight`, ``text``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLFrame`
    """
    
    TYPE = XSDComplexTypeFirstFret
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='first-fret'][@type='first-fret']"


class XMLFlip(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/flip/>`_
    
    The flip element represents the flip symbol used in brass notation.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='flip'][@type='empty-placement']"


class XMLFootnote(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/footnote/>`_
    
    
    
    ``complexType``: The formatted-text type represents a text element with text-formatting attributes.

``Possible parents``::obj:`~XMLAttributes`, :obj:`~XMLBackup`, :obj:`~XMLBarline`, :obj:`~XMLDirection`, :obj:`~XMLFigure`, :obj:`~XMLFiguredBass`, :obj:`~XMLForward`, :obj:`~XMLHarmony`, :obj:`~XMLLyric`, :obj:`~XMLNotations`, :obj:`~XMLNote`, :obj:`~XMLPartGroup`
    """
    
    TYPE = XSDComplexTypeFormattedText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='footnote'][@type='formatted-text']"


class XMLForPart(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/for-part/>`_
    
    The for-part element is used in a concert score to indicate the transposition for a transposed part created from that score. It is only used in score files that contain a concert-score element in the defaults. This allows concert scores with transposed parts to be represented in a single uncompressed MusicXML file.
    
    
    
    ``complexType``: The for-part type is used in a concert score to indicate the transposition for a transposed part created from that score. It is only used in score files that contain a concert-score element in the defaults. This allows concert scores with transposed parts to be represented in a single uncompressed MusicXML file.
    
    The optional number attribute refers to staff numbers, from top to bottom on the system. If absent, the child elements apply to all staves in the created part.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffNumber`

    ``Possible children``:    :obj:`~XMLPartClef`, :obj:`~XMLPartTranspose`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=part-clef@minOccurs=0@maxOccurs=1
           Element@name=part-transpose@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLAttributes`
    """
    
    TYPE = XSDComplexTypeForPart
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='for-part'][@type='for-part']"


class XMLForward(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/forward/>`_
    
    
    
    ``complexType``: The backup and forward elements are required to coordinate multiple voices in one part, including music on multiple staves. The forward element is generally used within voices and staves. Duration values should always be positive, and should not cross measure boundaries or mid-measure changes in the divisions value.

    ``Possible children``:    :obj:`~XMLDuration`, :obj:`~XMLFootnote`, :obj:`~XMLLevel`, :obj:`~XMLStaff`, :obj:`~XMLVoice`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Group@name=duration@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=duration@minOccurs=1@maxOccurs=1
           Group@name=editorial-voice@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=footnote@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=footnote@minOccurs=1@maxOccurs=1
                   Group@name=level@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=level@minOccurs=1@maxOccurs=1
                   Group@name=voice@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=voice@minOccurs=1@maxOccurs=1
           Group@name=staff@minOccurs=0@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=staff@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeForward
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='forward'][@type='forward']"


class XMLFp(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/fp/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='fp'][@type='empty']"


class XMLFrame(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/frame/>`_
    
    
    
    ``complexType``: The frame type represents a frame or fretboard diagram used together with a chord symbol. The representation is based on the NIFF guitar grid with additional information. The frame type's unplayed attribute indicates what to display above a string that has no associated frame-note element. Typical values are x and the empty string. If the attribute is not present, the display of the unplayed string is application-defined.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``height``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``unplayed``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValignImage`, ``width``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

    ``Possible children``:    :obj:`~XMLFirstFret`, :obj:`~XMLFrameFrets`, :obj:`~XMLFrameNote`, :obj:`~XMLFrameStrings`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=frame-strings@minOccurs=1@maxOccurs=1
           Element@name=frame-frets@minOccurs=1@maxOccurs=1
           Element@name=first-fret@minOccurs=0@maxOccurs=1
           Element@name=frame-note@minOccurs=1@maxOccurs=unbounded

``Possible parents``::obj:`~XMLHarmony`
    """
    
    TYPE = XSDComplexTypeFrame
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='frame'][@type='frame']"


class XMLFrameFrets(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/frame-frets/>`_

The frame-frets element gives the overall size of the frame in horizontal spaces (frets).



``Possible parents``::obj:`~XMLFrame`
    """
    
    TYPE = XSDSimpleTypePositiveInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='frame-frets'][@type='xs:positiveInteger']"


class XMLFrameNote(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/frame-note/>`_
    
    
    
    ``complexType``: The frame-note type represents each note included in the frame. An open string will have a fret value of 0, while a muted string will not be associated with a frame-note element.

    ``Possible children``:    :obj:`~XMLBarre`, :obj:`~XMLFingering`, :obj:`~XMLFret`, :obj:`~XMLString`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=string@minOccurs=1@maxOccurs=1
           Element@name=fret@minOccurs=1@maxOccurs=1
           Element@name=fingering@minOccurs=0@maxOccurs=1
           Element@name=barre@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLFrame`
    """
    
    TYPE = XSDComplexTypeFrameNote
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='frame-note'][@type='frame-note']"


class XMLFrameStrings(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/frame-strings/>`_

The frame-strings element gives the overall size of the frame in vertical lines (strings).



``Possible parents``::obj:`~XMLFrame`
    """
    
    TYPE = XSDSimpleTypePositiveInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='frame-strings'][@type='xs:positiveInteger']"


class XMLFret(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/fret/>`_
    
    
    
    ``complexType``: The fret element is used with tablature notation and chord diagrams. Fret numbers start with 0 for an open string and 1 for the first fret.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`

``Possible parents``::obj:`~XMLFrameNote`, :obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeFret
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='fret'][@type='fret']"


class XMLFunction(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/function/>`_
    
    The function element represents classical functional harmony with an indication like I, II, III rather than C, D, E. It represents the Roman numeral part of a functional harmony rather than the complete function itself. It has been deprecated as of MusicXML 4.0 in favor of the numeral element.
    
    
    
    ``complexType``: The style-text type represents a text element with a print-style attribute group.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLHarmony`
    """
    
    TYPE = XSDComplexTypeStyleText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='function'][@type='style-text']"


class XMLFz(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/fz/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='fz'][@type='empty']"


class XMLGlass(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/glass/>`_
    
    
    
    ``complexType``: The glass type represents pictograms for glass percussion instruments. The smufl attribute is used to distinguish different SMuFL glyphs for wind chimes in the Chimes pictograms range, including those made of materials other than glass.
    
    ``simpleContent``: The glass-value type represents pictograms for glass percussion instruments.
        
        Permitted Values: ``'glass harmonica'``, ``'glass harp'``, ``'wind chimes'``
    

    ``Possible attributes``: ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflPictogramGlyphName`

``Possible parents``::obj:`~XMLPercussion`
    """
    
    TYPE = XSDComplexTypeGlass
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='glass'][@type='glass']"


class XMLGlissando(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/glissando/>`_
    
    
    
    ``complexType``: Glissando and slide types both indicate rapidly moving from one pitch to the other so that individual notes are not discerned. A glissando sounds the distinct notes in between the two pitches and defaults to a wavy line. The optional text is printed alongside the line.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dash_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``line_type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineType`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``space_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required

``Possible parents``::obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeGlissando
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='glissando'][@type='glissando']"


class XMLGlyph(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/glyph/>`_
    
    
    
    ``complexType``: The glyph element represents what SMuFL glyph should be used for different variations of symbols that are semantically identical. The type attribute specifies what type of glyph is being defined. The element value specifies what SMuFL glyph to use, including recommended stylistic alternates. The SMuFL glyph name should match the type. For instance, a type of quarter-rest would use values restQuarter, restQuarterOld, or restQuarterZ. A type of g-clef-ottava-bassa would use values gClef8vb, gClef8vbOld, or gClef8vbCClef. A type of octave-shift-up-8 would use values ottava, ottavaBassa, ottavaBassaBa, ottavaBassaVb, or octaveBassa.
    
    ``simpleContent``: The smufl-glyph-name type is used for attributes that reference a specific Standard Music Font Layout (SMuFL) character. The value is a SMuFL canonical glyph name, not a code point. For instance, the value for a standard piano pedal mark would be keyboardPedalPed, not U+E650.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeGlyphType`\@required

``Possible parents``::obj:`~XMLAppearance`
    """
    
    TYPE = XSDComplexTypeGlyph
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='glyph'][@type='glyph']"


class XMLGolpe(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/golpe/>`_
    
    The golpe element represents the golpe symbol that is used for tapping the pick guard in guitar music.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='golpe'][@type='empty-placement']"


class XMLGrace(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/grace/>`_
    
    
    
    ``complexType``: The grace type indicates the presence of a grace note. The slash attribute for a grace note is yes for slashed grace notes. The steal-time-previous attribute indicates the percentage of time to steal from the previous note for the grace note. The steal-time-following attribute indicates the percentage of time to steal from the following note for the grace note, as for appoggiaturas. The make-time attribute indicates to make time, not steal time; the units are in real-time divisions for the grace note.

    ``Possible attributes``: ``make_time``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeDivisions`, ``slash``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``steal_time_following``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``steal_time_previous``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeGrace
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='grace'][@type='grace']"


class XMLGroup(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/group/>`_

The group element allows the use of different versions of the part for different purposes. Typical values include score, parts, sound, and data. Ordering information can be derived from the ordering within a MusicXML score or opus.



``Possible parents``::obj:`~XMLScorePart`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='group'][@type='xs:string']"


class XMLGroupAbbreviation(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/group-abbreviation/>`_
    
    
    
    ``complexType``: The group-name type describes the name or abbreviation of a part-group element. Formatting attributes in the group-name type are deprecated in Version 2.0 in favor of the new group-name-display and group-abbreviation-display elements.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``justify``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLPartGroup`
    """
    
    TYPE = XSDComplexTypeGroupName
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='group-abbreviation'][@type='group-name']"


class XMLGroupAbbreviationDisplay(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/group-abbreviation-display/>`_
    
    Formatting specified in the group-abbreviation-display element overrides formatting specified in the group-abbreviation element.
    
    
    
    ``complexType``: The name-display type is used for exact formatting of multi-font text in part and group names to the left of the system. The print-object attribute can be used to determine what, if anything, is printed at the start of each system. Enclosure for the display-text element is none by default. Language for the display-text element is Italian ("it") by default.

    ``Possible attributes``: ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

    ``Possible children``:    :obj:`~XMLAccidentalText`, :obj:`~XMLDisplayText`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Choice@minOccurs=0@maxOccurs=unbounded
               Element@name=display-text@minOccurs=1@maxOccurs=1
               Element@name=accidental-text@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLPartGroup`
    """
    
    TYPE = XSDComplexTypeNameDisplay
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='group-abbreviation-display'][@type='name-display']"


class XMLGroupBarline(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/group-barline/>`_
    
    
    
    ``complexType``: The group-barline type indicates if the group should have common barlines.
    
    ``simpleContent``: The group-barline-value type indicates if the group should have common barlines.
        
        Permitted Values: ``'yes'``, ``'no'``, ``'Mensurstrich'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`

``Possible parents``::obj:`~XMLPartGroup`
    """
    
    TYPE = XSDComplexTypeGroupBarline
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='group-barline'][@type='group-barline']"


class XMLGroupLink(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/group-link/>`_

Multiple part-link elements can reference different types of linked documents, such as parts and condensed score. The optional group-link elements identify the groups used in the linked document. The content of a group-link element should match the content of a group element in the linked document.



``Possible parents``::obj:`~XMLPartLink`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='group-link'][@type='xs:string']"


class XMLGroupName(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/group-name/>`_
    
    
    
    ``complexType``: The group-name type describes the name or abbreviation of a part-group element. Formatting attributes in the group-name type are deprecated in Version 2.0 in favor of the new group-name-display and group-abbreviation-display elements.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``justify``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLPartGroup`
    """
    
    TYPE = XSDComplexTypeGroupName
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='group-name'][@type='group-name']"


class XMLGroupNameDisplay(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/group-name-display/>`_
    
    Formatting specified in the group-name-display element overrides formatting specified in the group-name element.
    
    
    
    ``complexType``: The name-display type is used for exact formatting of multi-font text in part and group names to the left of the system. The print-object attribute can be used to determine what, if anything, is printed at the start of each system. Enclosure for the display-text element is none by default. Language for the display-text element is Italian ("it") by default.

    ``Possible attributes``: ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

    ``Possible children``:    :obj:`~XMLAccidentalText`, :obj:`~XMLDisplayText`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Choice@minOccurs=0@maxOccurs=unbounded
               Element@name=display-text@minOccurs=1@maxOccurs=1
               Element@name=accidental-text@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLPartGroup`
    """
    
    TYPE = XSDComplexTypeNameDisplay
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='group-name-display'][@type='name-display']"


class XMLGroupSymbol(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/group-symbol/>`_
    
    
    
    ``complexType``: The group-symbol type indicates how the symbol for a group is indicated in the score. It is none if not specified.
    
    ``simpleContent``: The group-symbol-value type indicates how the symbol for a group or multi-staff part is indicated in the score.
        
        Permitted Values: ``'none'``, ``'brace'``, ``'line'``, ``'bracket'``, ``'square'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLPartGroup`
    """
    
    TYPE = XSDComplexTypeGroupSymbol
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='group-symbol'][@type='group-symbol']"


class XMLGroupTime(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/group-time/>`_
    
    The group-time element indicates that the displayed time signatures should stretch across all parts and staves in the group.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLPartGroup`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='group-time'][@type='empty']"


class XMLGrouping(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/grouping/>`_
    
    
    
    ``complexType``: The grouping type is used for musical analysis. When the type attribute is "start" or "single", it usually contains one or more feature elements. The number attribute is used for distinguishing between overlapping and hierarchical groupings. The member-of attribute allows for easy distinguishing of what grouping elements are in what hierarchy. Feature elements contained within a "stop" type of grouping may be ignored.
    
    This element is flexible to allow for different types of analyses. Future versions of the MusicXML format may add elements that can represent more standardized categories of analysis data, allowing for easier data sharing.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``member_of``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStopSingle`\@required

    ``Possible children``:    :obj:`~XMLFeature`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=feature@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeGrouping
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='grouping'][@type='grouping']"


class XMLHalfMuted(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/half-muted/>`_
    
    The half-muted element represents the half-muted symbol, which looks like a circle with a plus sign inside. The smufl attribute can be used to distinguish different SMuFL glyphs that have a similar appearance such as brassMuteHalfClosed and guitarHalfOpenPedal. If not present, the default glyph is brassMuteHalfClosed.
    
    
    
    ``complexType``: The empty-placement-smufl type represents an empty element with print-style, placement, and smufl attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacementSmufl
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='half-muted'][@type='empty-placement-smufl']"


class XMLHammerOn(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/hammer-on/>`_
    
    
    
    ``complexType``: The hammer-on and pull-off elements are used in guitar and fretted instrument notation. Since a single slur can be marked over many notes, the hammer-on and pull-off elements are separate so the individual pair of notes can be specified. The element content can be used to specify how the hammer-on or pull-off should be notated. An empty element leaves this choice up to the application.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeHammerOnPullOff
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='hammer-on'][@type='hammer-on-pull-off']"


class XMLHandbell(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/handbell/>`_
    
    
    
    ``complexType``: The handbell element represents notation for various techniques used in handbell and handchime music.
    
    ``simpleContent``: The handbell-value type represents the type of handbell technique being notated.
        
        Permitted Values: ``'belltree'``, ``'damp'``, ``'echo'``, ``'gyro'``, ``'hand martellato'``, ``'mallet lift'``, ``'mallet table'``, ``'martellato'``, ``'martellato lift'``, ``'muted martellato'``, ``'pluck lift'``, ``'swing'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeHandbell
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='handbell'][@type='handbell']"


class XMLHarmonClosed(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/harmon-closed/>`_
    
    
    
    ``complexType``: The harmon-closed type represents whether the harmon mute is closed, open, or half-open. The optional location attribute indicates which portion of the symbol is filled in when the element value is half.
    
    ``simpleContent``: The harmon-closed-value type represents whether the harmon mute is closed, open, or half-open.
        
        Permitted Values: ``'yes'``, ``'no'``, ``'half'``
    

    ``Possible attributes``: ``location``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeHarmonClosedLocation`

``Possible parents``::obj:`~XMLHarmonMute`
    """
    
    TYPE = XSDComplexTypeHarmonClosed
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='harmon-closed'][@type='harmon-closed']"


class XMLHarmonMute(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/harmon-mute/>`_
    
    
    
    ``complexType``: The harmon-mute type represents the symbols used for harmon mutes in brass notation.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

    ``Possible children``:    :obj:`~XMLHarmonClosed`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=harmon-closed@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeHarmonMute
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='harmon-mute'][@type='harmon-mute']"


class XMLHarmonic(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/harmonic/>`_
    
    
    
    ``complexType``: The harmonic type indicates natural and artificial harmonics. Allowing the type of pitch to be specified, combined with controls for appearance/playback differences, allows both the notation and the sound to be represented. Artificial harmonics can add a notated touching pitch; artificial pinch harmonics will usually not notate a touching pitch. The attributes for the harmonic element refer to the use of the circular harmonic symbol, typically but not always used with natural harmonics.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

    ``Possible children``:    :obj:`~XMLArtificial`, :obj:`~XMLBasePitch`, :obj:`~XMLNatural`, :obj:`~XMLSoundingPitch`, :obj:`~XMLTouchingPitch`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Choice@minOccurs=0@maxOccurs=1
               Element@name=natural@minOccurs=1@maxOccurs=1
               Element@name=artificial@minOccurs=1@maxOccurs=1
           Choice@minOccurs=0@maxOccurs=1
               Element@name=base-pitch@minOccurs=1@maxOccurs=1
               Element@name=touching-pitch@minOccurs=1@maxOccurs=1
               Element@name=sounding-pitch@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeHarmonic
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='harmonic'][@type='harmonic']"


class XMLHarmony(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/harmony/>`_
    
    
    
    ``complexType``: The harmony type represents harmony analysis, including chord symbols in popular music as well as functional harmony analysis in classical music.
    
    If there are alternate harmonies possible, this can be specified using multiple harmony elements differentiated by type. Explicit harmonies have all note present in the music; implied have some notes missing but implied; alternate represents alternate analyses.
    
    The print-object attribute controls whether or not anything is printed due to the harmony element. The print-frame attribute controls printing of a frame or fretboard diagram. The print-style attribute group sets the default for the harmony, but individual elements can override this with their own print-style values. The arrangement attribute specifies how multiple harmony-chord groups are arranged relative to each other. Harmony-chords with vertical arrangement are separated by horizontal lines. Harmony-chords with diagonal or horizontal arrangement are separated by diagonal lines or slashes.

    ``Possible attributes``: ``arrangement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeHarmonyArrangement`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``print_frame``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``system``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSystemRelation`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeHarmonyType`

    ``Possible children``:    :obj:`~XMLBass`, :obj:`~XMLDegree`, :obj:`~XMLFootnote`, :obj:`~XMLFrame`, :obj:`~XMLFunction`, :obj:`~XMLInversion`, :obj:`~XMLKind`, :obj:`~XMLLevel`, :obj:`~XMLNumeral`, :obj:`~XMLOffset`, :obj:`~XMLRoot`, :obj:`~XMLStaff`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Group@name=harmony-chord@minOccurs=1@maxOccurs=unbounded
               Sequence@minOccurs=1@maxOccurs=1
                   Choice@minOccurs=1@maxOccurs=1
                       Element@name=root@minOccurs=1@maxOccurs=1
                       Element@name=numeral@minOccurs=1@maxOccurs=1
                       Element@name=function@minOccurs=1@maxOccurs=1
                   Element@name=kind@minOccurs=1@maxOccurs=1
                   Element@name=inversion@minOccurs=0@maxOccurs=1
                   Element@name=bass@minOccurs=0@maxOccurs=1
                   Element@name=degree@minOccurs=0@maxOccurs=unbounded
           Element@name=frame@minOccurs=0@maxOccurs=1
           Element@name=offset@minOccurs=0@maxOccurs=1
           Group@name=editorial@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=footnote@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=footnote@minOccurs=1@maxOccurs=1
                   Group@name=level@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=level@minOccurs=1@maxOccurs=1
           Group@name=staff@minOccurs=0@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=staff@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeHarmony
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='harmony'][@type='harmony']"


class XMLHarpPedals(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/harp-pedals/>`_
    
    
    
    ``complexType``: The harp-pedals type is used to create harp pedal diagrams. The pedal-step and pedal-alter elements use the same values as the step and alter elements. For easiest reading, the pedal-tuning elements should follow standard harp pedal order, with pedal-step values of D, C, B, E, F, G, and A.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

    ``Possible children``:    :obj:`~XMLPedalTuning`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=pedal-tuning@minOccurs=1@maxOccurs=unbounded

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeHarpPedals
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='harp-pedals'][@type='harp-pedals']"


class XMLHaydn(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/haydn/>`_
    
    The haydn element represents the Haydn ornament. This is defined in SMuFL as ornamentHaydn.
    
    
    
    ``complexType``: The empty-trill-sound type represents an empty element with print-style, placement, and trill-sound attributes.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``second_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``start_note``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartNote`, ``trill_step``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillStep`, ``two_note_turn``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTwoNoteTurn`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeEmptyTrillSound
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='haydn'][@type='empty-trill-sound']"


class XMLHeel(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/heel/>`_
    
    
    
    ``complexType``: The heel and toe elements are used with organ pedals. The substitution value is "no" if the attribute is not present.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``substitution``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeHeelToe
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='heel'][@type='heel-toe']"


class XMLHole(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/hole/>`_
    
    
    
    ``complexType``: The hole type represents the symbols used for woodwind and brass fingerings as well as other notations.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

    ``Possible children``:    :obj:`~XMLHoleClosed`, :obj:`~XMLHoleShape`, :obj:`~XMLHoleType`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=hole-type@minOccurs=0@maxOccurs=1
           Element@name=hole-closed@minOccurs=1@maxOccurs=1
           Element@name=hole-shape@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeHole
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='hole'][@type='hole']"


class XMLHoleClosed(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/hole-closed/>`_
    
    
    
    ``complexType``: The hole-closed type represents whether the hole is closed, open, or half-open. The optional location attribute indicates which portion of the hole is filled in when the element value is half.
    
    ``simpleContent``: The hole-closed-value type represents whether the hole is closed, open, or half-open.
        
        Permitted Values: ``'yes'``, ``'no'``, ``'half'``
    

    ``Possible attributes``: ``location``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeHoleClosedLocation`

``Possible parents``::obj:`~XMLHole`
    """
    
    TYPE = XSDComplexTypeHoleClosed
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='hole-closed'][@type='hole-closed']"


class XMLHoleShape(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/hole-shape/>`_

The optional hole-shape element indicates the shape of the hole symbol; the default is a circle.



``Possible parents``::obj:`~XMLHole`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='hole-shape'][@type='xs:string']"


class XMLHoleType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/hole-type/>`_

The content of the optional hole-type element indicates what the hole symbol represents in terms of instrument fingering or other techniques.



``Possible parents``::obj:`~XMLHole`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='hole-type'][@type='xs:string']"


class XMLHumming(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/humming/>`_
    
    The humming element represents a humming voice.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLLyric`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='humming'][@type='empty']"


class XMLIdentification(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/identification/>`_
    
    
    
    ``complexType``: Identification contains basic metadata about the score. It includes information that may apply at a score-wide, movement-wide, or part-wide level. The creator, rights, source, and relation elements are based on Dublin Core.

    ``Possible children``:    :obj:`~XMLCreator`, :obj:`~XMLEncoding`, :obj:`~XMLMiscellaneous`, :obj:`~XMLRelation`, :obj:`~XMLRights`, :obj:`~XMLSource`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=creator@minOccurs=0@maxOccurs=unbounded
           Element@name=rights@minOccurs=0@maxOccurs=unbounded
           Element@name=encoding@minOccurs=0@maxOccurs=1
           Element@name=source@minOccurs=0@maxOccurs=1
           Element@name=relation@minOccurs=0@maxOccurs=unbounded
           Element@name=miscellaneous@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLScorePart`, :obj:`~XMLScorePartwise`
    """
    
    TYPE = XSDComplexTypeIdentification
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='identification'][@type='identification']"


class XMLImage(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/image/>`_
    
    
    
    ``complexType``: The image type is used to include graphical images in a score.

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeImage
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='image'][@type='image']"


class XMLInstrument(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/instrument/>`_
    
    
    
    ``complexType``: The instrument type distinguishes between score-instrument elements in a score-part. The id attribute is an IDREF back to the score-instrument ID. If multiple score-instruments are specified in a score-part, there should be an instrument element for each note in the part. Notes that are shared between multiple score-instruments can have more than one instrument element.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF`\@required

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeInstrument
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='instrument'][@type='instrument']"


class XMLInstrumentAbbreviation(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/instrument-abbreviation/>`_

The optional instrument-abbreviation element is typically used within a software application, rather than appearing on the printed page of a score.



``Possible parents``::obj:`~XMLScoreInstrument`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='instrument-abbreviation'][@type='xs:string']"


class XMLInstrumentChange(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/instrument-change/>`_
    
    
    
    ``complexType``: The instrument-change element type represents a change to the virtual instrument sound for a given score-instrument. The id attribute refers to the score-instrument affected by the change. All instrument-change child elements can also be initially specified within the score-instrument element.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF`\@required

    ``Possible children``:    :obj:`~XMLEnsemble`, :obj:`~XMLInstrumentSound`, :obj:`~XMLSolo`, :obj:`~XMLVirtualInstrument`

    ``XSD structure:``

    .. code-block::

       Group@name=virtual-instrument-data@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Element@name=instrument-sound@minOccurs=0@maxOccurs=1
               Choice@minOccurs=0@maxOccurs=1
                   Element@name=solo@minOccurs=1@maxOccurs=1
                   Element@name=ensemble@minOccurs=1@maxOccurs=1
               Element@name=virtual-instrument@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLSound`
    """
    
    TYPE = XSDComplexTypeInstrumentChange
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='instrument-change'][@type='instrument-change']"


class XMLInstrumentLink(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/instrument-link/>`_
    
    
    
    ``complexType``: Multiple part-link elements can link a condensed part within a score file to multiple MusicXML parts files. For example, a "Clarinet 1 and 2" part in a score file could link to separate "Clarinet 1" and "Clarinet 2" part files. The instrument-link type distinguish which of the score-instruments within a score-part are in which part file. The instrument-link id attribute refers to a score-instrument id attribute.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF`\@required

``Possible parents``::obj:`~XMLPartLink`
    """
    
    TYPE = XSDComplexTypeInstrumentLink
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='instrument-link'][@type='instrument-link']"


class XMLInstrumentName(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/instrument-name/>`_

The instrument-name element is typically used within a software application, rather than appearing on the printed page of a score.



``Possible parents``::obj:`~XMLScoreInstrument`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='instrument-name'][@type='xs:string']"


class XMLInstrumentSound(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/instrument-sound/>`_

The instrument-sound element describes the default timbre of the score-instrument. This description is independent of a particular virtual or MIDI instrument specification and allows playback to be shared more easily between applications and libraries.



``Possible parents``::obj:`~XMLInstrumentChange`, :obj:`~XMLScoreInstrument`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='instrument-sound'][@type='xs:string']"


class XMLInstruments(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/instruments/>`_

The instruments element is only used if more than one instrument is represented in the part (e.g., oboe I and II where they play together most of the time). If absent, a value of 1 is assumed.



``Possible parents``::obj:`~XMLAttributes`
    """
    
    TYPE = XSDSimpleTypeNonNegativeInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='instruments'][@type='xs:nonNegativeInteger']"


class XMLInterchangeable(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/interchangeable/>`_
    
    
    
    ``complexType``: The interchangeable type is used to represent the second in a pair of interchangeable dual time signatures, such as the 6/8 in 3/4 (6/8). A separate symbol attribute value is available compared to the time element's symbol attribute, which applies to the first of the dual time signatures.

    ``Possible attributes``: ``separator``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeSeparator`, ``symbol``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeSymbol`

    ``Possible children``:    :obj:`~XMLBeatType`, :obj:`~XMLBeats`, :obj:`~XMLTimeRelation`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=time-relation@minOccurs=0@maxOccurs=1
           Group@name=time-signature@minOccurs=1@maxOccurs=unbounded
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=beats@minOccurs=1@maxOccurs=1
                   Element@name=beat-type@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLTime`
    """
    
    TYPE = XSDComplexTypeInterchangeable
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='interchangeable'][@type='interchangeable']"


class XMLInversion(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/inversion/>`_
    
    
    
    ``complexType``: The inversion type represents harmony inversions. The value is a number indicating which inversion is used: 0 for root position, 1 for first inversion, etc.  The text attribute indicates how the inversion should be displayed in a score.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``text``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLHarmony`
    """
    
    TYPE = XSDComplexTypeInversion
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='inversion'][@type='inversion']"


class XMLInvertedMordent(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/inverted-mordent/>`_
    
    The inverted-mordent element represents the sign without the vertical line. The choice of which mordent is inverted differs between MusicXML and SMuFL. The long attribute is "no" by default.
    
    
    
    ``complexType``: The mordent type is used for both represents the mordent sign with the vertical line and the inverted-mordent sign without the line. The long attribute is "no" by default. The approach and departure attributes are used for compound ornaments, indicating how the beginning and ending of the ornament look relative to the main part of the mordent.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``approach``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``departure``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``long``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``second_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``start_note``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartNote`, ``trill_step``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillStep`, ``two_note_turn``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTwoNoteTurn`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeMordent
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='inverted-mordent'][@type='mordent']"


class XMLInvertedTurn(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/inverted-turn/>`_
    
    The inverted-turn element has the shape which goes down and then up.
    
    
    
    ``complexType``: The horizontal-turn type represents turn elements that are horizontal rather than vertical. These are empty elements with print-style, placement, trill-sound, and slash attributes. If the slash attribute is yes, then a vertical line is used to slash the turn. It is no if not specified.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``second_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``slash``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``start_note``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartNote`, ``trill_step``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillStep`, ``two_note_turn``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTwoNoteTurn`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeHorizontalTurn
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='inverted-turn'][@type='horizontal-turn']"


class XMLInvertedVerticalTurn(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/inverted-vertical-turn/>`_
    
    The inverted-vertical-turn element has the turn symbol shape arranged vertically going from upper right to lower left.
    
    
    
    ``complexType``: The empty-trill-sound type represents an empty element with print-style, placement, and trill-sound attributes.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``second_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``start_note``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartNote`, ``trill_step``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillStep`, ``two_note_turn``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTwoNoteTurn`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeEmptyTrillSound
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='inverted-vertical-turn'][@type='empty-trill-sound']"


class XMLIpa(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/ipa/>`_

The ipa element represents International Phonetic Alphabet (IPA) sounds for vocal music. String content is limited to IPA 2015 symbols represented in Unicode 13.0.



``Possible parents``::obj:`~XMLPlay`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='ipa'][@type='xs:string']"


class XMLKey(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/key/>`_
    
    The key element represents a key signature. Both traditional and non-traditional key signatures are supported. The optional number attribute refers to staff numbers. If absent, the key signature applies to all staves in the part.
    
    
    
    ``complexType``: The key type represents a key signature. Both traditional and non-traditional key signatures are supported. The optional number attribute refers to staff numbers. If absent, the key signature applies to all staves in the part. Key signatures appear at the start of each system unless the print-object attribute has been set to "no".

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffNumber`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

    ``Possible children``:    :obj:`~XMLCancel`, :obj:`~XMLFifths`, :obj:`~XMLKeyAccidental`, :obj:`~XMLKeyAlter`, :obj:`~XMLKeyOctave`, :obj:`~XMLKeyStep`, :obj:`~XMLMode`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Choice@minOccurs=1@maxOccurs=1
               Group@name=traditional-key@minOccurs=1@maxOccurs=1
                   Sequence@minOccurs=1@maxOccurs=1
                       Element@name=cancel@minOccurs=0@maxOccurs=1
                       Element@name=fifths@minOccurs=1@maxOccurs=1
                       Element@name=mode@minOccurs=0@maxOccurs=1
               Group@name=non-traditional-key@minOccurs=0@maxOccurs=unbounded
                   Sequence@minOccurs=1@maxOccurs=1
                       Element@name=key-step@minOccurs=1@maxOccurs=1
                       Element@name=key-alter@minOccurs=1@maxOccurs=1
                       Element@name=key-accidental@minOccurs=0@maxOccurs=1
           Element@name=key-octave@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLAttributes`
    """
    
    TYPE = XSDComplexTypeKey
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='key'][@type='key']"


class XMLKeyAccidental(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/key-accidental/>`_
    
    Non-traditional key signatures are represented using a list of altered tones. The key-accidental element indicates the accidental to be displayed in the key signature, represented in the same manner as the accidental element. It is used for disambiguating microtonal accidentals.
    
    
    
    ``complexType``: The key-accidental type indicates the accidental to be displayed in a non-traditional key signature, represented in the same manner as the accidental type without the formatting attributes.
    
    ``simpleContent``: The accidental-value type represents notated accidentals supported by MusicXML. In the MusicXML 2.0 DTD this was a string with values that could be included. The XSD strengthens the data typing to an enumerated list. The quarter- and three-quarters- accidentals are Tartini-style quarter-tone accidentals. The -down and -up accidentals are quarter-tone accidentals that include arrows pointing down or up. The slash- accidentals are used in Turkish classical music. The numbered sharp and flat accidentals are superscripted versions of the accidental signs, used in Turkish folk music. The sori and koron accidentals are microtonal sharp and flat accidentals used in Iranian and Persian music. The other accidental covers accidentals other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL accidental. The smufl attribute may be used with any accidental value to help specify the appearance of symbols that share the same MusicXML semantics.
        
        Permitted Values: ``'sharp'``, ``'natural'``, ``'flat'``, ``'double-sharp'``, ``'sharp-sharp'``, ``'flat-flat'``, ``'natural-sharp'``, ``'natural-flat'``, ``'quarter-flat'``, ``'quarter-sharp'``, ``'three-quarters-flat'``, ``'three-quarters-sharp'``, ``'sharp-down'``, ``'sharp-up'``, ``'natural-down'``, ``'natural-up'``, ``'flat-down'``, ``'flat-up'``, ``'double-sharp-down'``, ``'double-sharp-up'``, ``'flat-flat-down'``, ``'flat-flat-up'``, ``'arrow-down'``, ``'arrow-up'``, ``'triple-sharp'``, ``'triple-flat'``, ``'slash-quarter-sharp'``, ``'slash-sharp'``, ``'slash-flat'``, ``'double-slash-flat'``, ``'sharp-1'``, ``'sharp-2'``, ``'sharp-3'``, ``'sharp-5'``, ``'flat-1'``, ``'flat-2'``, ``'flat-3'``, ``'flat-4'``, ``'sori'``, ``'koron'``, ``'other'``
    

    ``Possible attributes``: ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflAccidentalGlyphName`

``Possible parents``::obj:`~XMLKey`
    """
    
    TYPE = XSDComplexTypeKeyAccidental
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='key-accidental'][@type='key-accidental']"


class XMLKeyAlter(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/key-alter/>`_
    
    Non-traditional key signatures are represented using a list of altered tones. The key-alter element represents the alteration for a given pitch step, represented with semitones in the same manner as the alter element.
    
    
    
    ``simpleType``: The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.

``Possible parents``::obj:`~XMLKey`
    """
    
    TYPE = XSDSimpleTypeSemitones
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='key-alter'][@type='semitones']"


class XMLKeyOctave(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/key-octave/>`_
    
    The optional list of key-octave elements is used to specify in which octave each element of the key signature appears.
    
    
    
    ``complexType``: The key-octave type specifies in which octave an element of a key signature appears. The content specifies the octave value using the same values as the display-octave element. The number attribute is a positive integer that refers to the key signature element in left-to-right order. If the cancel attribute is set to yes, then this number refers to the canceling key signature specified by the cancel element in the parent key element. The cancel attribute cannot be set to yes if there is no corresponding cancel element within the parent key element. It is no by default.
    
    ``simpleContent``: Octaves are represented by the numbers 0 to 9, where 4 indicates the octave started by middle C.

    ``Possible attributes``: ``cancel``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePositiveInteger`\@required

``Possible parents``::obj:`~XMLKey`
    """
    
    TYPE = XSDComplexTypeKeyOctave
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='key-octave'][@type='key-octave']"


class XMLKeyStep(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/key-step/>`_
    
    Non-traditional key signatures are represented using a list of altered tones. The key-step element indicates the pitch step to be altered, represented using the same names as in the step element.
    
    
    
    ``simpleType``: The step type represents a step of the diatonic scale, represented using the English letters A through G.
        
        Permitted Values: ``'A'``, ``'B'``, ``'C'``, ``'D'``, ``'E'``, ``'F'``, ``'G'``
    

``Possible parents``::obj:`~XMLKey`
    """
    
    TYPE = XSDSimpleTypeStep
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='key-step'][@type='step']"


class XMLKind(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/kind/>`_
    
    
    
    ``complexType``: Kind indicates the type of chord. Degree elements can then add, subtract, or alter from these starting points
    
    The attributes are used to indicate the formatting of the symbol. Since the kind element is the constant in all the harmony-chord groups that can make up a polychord, many formatting attributes are here.
    
    The use-symbols attribute is yes if the kind should be represented when possible with harmony symbols rather than letters and numbers. These symbols include:
    
    	major: a triangle, like Unicode 25B3
    	minor: -, like Unicode 002D
    	augmented: +, like Unicode 002B
    	diminished: °, like Unicode 00B0
    	half-diminished: ø, like Unicode 00F8
    
    For the major-minor kind, only the minor symbol is used when use-symbols is yes. The major symbol is set using the symbol attribute in the degree-value element. The corresponding degree-alter value will usually be 0 in this case.
    
    The text attribute describes how the kind should be spelled in a score. If use-symbols is yes, the value of the text attribute follows the symbol. The stack-degrees attribute is yes if the degree elements should be stacked above each other. The parentheses-degrees attribute is yes if all the degrees should be in parentheses. The bracket-degrees attribute is yes if all the degrees should be in a bracket. If not specified, these values are implementation-specific. The alignment attributes are for the entire harmony-chord group of which this kind element is a part.
    
    The text attribute may use strings such as "13sus" that refer to both the kind and one or more degree elements. In this case, the corresponding degree elements should have the print-object attribute set to "no" to keep redundant alterations from being displayed.
    
    ``simpleContent``: A kind-value indicates the type of chord. Degree elements can then add, subtract, or alter from these starting points. Values include:
    
    Triads:
        major (major third, perfect fifth)
        minor (minor third, perfect fifth)
        augmented (major third, augmented fifth)
        diminished (minor third, diminished fifth)
    Sevenths:
        dominant (major triad, minor seventh)
        major-seventh (major triad, major seventh)
        minor-seventh (minor triad, minor seventh)
        diminished-seventh (diminished triad, diminished seventh)
        augmented-seventh (augmented triad, minor seventh)
        half-diminished (diminished triad, minor seventh)
        major-minor (minor triad, major seventh)
    Sixths:
        major-sixth (major triad, added sixth)
        minor-sixth (minor triad, added sixth)
    Ninths:
        dominant-ninth (dominant-seventh, major ninth)
        major-ninth (major-seventh, major ninth)
        minor-ninth (minor-seventh, major ninth)
    11ths (usually as the basis for alteration):
        dominant-11th (dominant-ninth, perfect 11th)
        major-11th (major-ninth, perfect 11th)
        minor-11th (minor-ninth, perfect 11th)
    13ths (usually as the basis for alteration):
        dominant-13th (dominant-11th, major 13th)
        major-13th (major-11th, major 13th)
        minor-13th (minor-11th, major 13th)
    Suspended:
        suspended-second (major second, perfect fifth)
        suspended-fourth (perfect fourth, perfect fifth)
    Functional sixths:
        Neapolitan
        Italian
        French
        German
    Other:
        pedal (pedal-point bass)
        power (perfect fifth)
        Tristan
    
    The "other" kind is used when the harmony is entirely composed of add elements.
    
    The "none" kind is used to explicitly encode absence of chords or functional harmony. In this case, the root, numeral, or function element has no meaning. When using the root or numeral element, the root-step or numeral-step text attribute should be set to the empty string to keep the root or numeral from being displayed.
        
        Permitted Values: ``'major'``, ``'minor'``, ``'augmented'``, ``'diminished'``, ``'dominant'``, ``'major-seventh'``, ``'minor-seventh'``, ``'diminished-seventh'``, ``'augmented-seventh'``, ``'half-diminished'``, ``'major-minor'``, ``'major-sixth'``, ``'minor-sixth'``, ``'dominant-ninth'``, ``'major-ninth'``, ``'minor-ninth'``, ``'dominant-11th'``, ``'major-11th'``, ``'minor-11th'``, ``'dominant-13th'``, ``'major-13th'``, ``'minor-13th'``, ``'suspended-second'``, ``'suspended-fourth'``, ``'Neapolitan'``, ``'Italian'``, ``'French'``, ``'German'``, ``'pedal'``, ``'power'``, ``'Tristan'``, ``'other'``, ``'none'``
    

    ``Possible attributes``: ``bracket_degrees``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``parentheses_degrees``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``stack_degrees``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``text``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``use_symbols``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLHarmony`
    """
    
    TYPE = XSDComplexTypeKind
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='kind'][@type='kind']"


class XMLLaughing(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/laughing/>`_
    
    The laughing element represents a laughing voice.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLLyric`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='laughing'][@type='empty']"


class XMLLeftDivider(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/left-divider/>`_
    
    
    
    ``complexType``: The empty-print-style-align-object type represents an empty element with print-object and print-style-align attribute groups.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLSystemDividers`
    """
    
    TYPE = XSDComplexTypeEmptyPrintObjectStyleAlign
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='left-divider'][@type='empty-print-object-style-align']"


class XMLLeftMargin(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/left-margin/>`_
    
    
    
    ``simpleType``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

``Possible parents``::obj:`~XMLPageMargins`, :obj:`~XMLSystemMargins`
    """
    
    TYPE = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='left-margin'][@type='tenths']"


class XMLLevel(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/level/>`_
    
    
    
    ``complexType``: The level type is used to specify editorial information for different MusicXML elements. The content contains identifying and/or descriptive text about the editorial status of the parent element.
    
    If the reference attribute is yes, this indicates editorial information that is for display only and should not affect playback. For instance, a modern edition of older music may set reference="yes" on the attributes containing the music's original clef, key, and time signature. It is no if not specified.
    
    The type attribute indicates whether the editorial information applies to the start of a series of symbols, the end of a series of symbols, or a single symbol. It is single if not specified for compatibility with earlier MusicXML versions.

    ``Possible attributes``: ``bracket``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``parentheses``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``reference``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSymbolSize`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStopSingle`

``Possible parents``::obj:`~XMLAttributes`, :obj:`~XMLBackup`, :obj:`~XMLBarline`, :obj:`~XMLDirection`, :obj:`~XMLFigure`, :obj:`~XMLFiguredBass`, :obj:`~XMLForward`, :obj:`~XMLHarmony`, :obj:`~XMLLyric`, :obj:`~XMLNotations`, :obj:`~XMLNote`, :obj:`~XMLPartGroup`
    """
    
    TYPE = XSDComplexTypeLevel
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='level'][@type='level']"


class XMLLine(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/line/>`_
    
    Line numbers are counted from the bottom of the staff. They are only needed with the G, F, and C signs in order to position a pitch correctly on the staff. Standard values are 2 for the G sign (treble clef), 4 for the F sign (bass clef), and 3 for the C sign (alto clef). Line values can be used to specify positions outside the staff, such as a C clef positioned in the middle of a grand staff.
    
    
    
    ``simpleType``: The staff-line-position type indicates the line position on a given staff. Staff lines are numbered from bottom to top, with 1 being the bottom line on a staff. A staff-line-position value can extend beyond the range of the lines on the current staff.

``Possible parents``::obj:`~XMLClef`, :obj:`~XMLPartClef`
    """
    
    TYPE = XSDSimpleTypeStaffLinePosition
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='line'][@type='staff-line-position']"


class XMLLineDetail(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/line-detail/>`_
    
    
    
    ``complexType``: If the staff-lines element is present, the appearance of each line may be individually specified with a line-detail type. Staff lines are numbered from bottom to top. The print-object attribute allows lines to be hidden within a staff. This is used in special situations such as a widely-spaced percussion staff where a note placed below the higher line is distinct from a note placed above the lower line. Hidden staff lines are included when specifying clef lines and determining display-step / display-octave values, but are not counted as lines for the purposes of the system-layout and staff-layout elements.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``line_type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineType`, ``line``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffLine`\@required, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``width``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLStaffDetails`
    """
    
    TYPE = XSDComplexTypeLineDetail
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='line-detail'][@type='line-detail']"


class XMLLineWidth(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/line-width/>`_
    
    
    
    ``complexType``: The line-width type indicates the width of a line type in tenths. The type attribute defines what type of line is being defined. Values include beam, bracket, dashes, enclosure, ending, extend, heavy barline, leger, light barline, octave shift, pedal, slur middle, slur tip, staff, stem, tie middle, tie tip, tuplet bracket, and wedge. The text content is expressed in tenths.
    
    ``simpleContent``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineWidthType`\@required

``Possible parents``::obj:`~XMLAppearance`
    """
    
    TYPE = XSDComplexTypeLineWidth
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='line-width'][@type='line-width']"


class XMLLink(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/link/>`_
    
    
    
    ``complexType``: The link type serves as an outgoing simple XLink. If a relative link is used within a document that is part of a compressed MusicXML file, the link is relative to the root folder of the zip file.

``Possible parents``::obj:`~XMLCredit`, :obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeLink
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='link'][@type='link']"


class XMLListen(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/listen/>`_
    
    
    
    ``complexType``: The listen and listening types, new in Version 4.0, specify different ways that a score following or machine listening application can interact with a performer. The listen type handles interactions that are specific to a note. If multiple child elements of the same type are present, they should have distinct player and/or time-only attributes.

    ``Possible children``:    :obj:`~XMLAssess`, :obj:`~XMLOtherListen`, :obj:`~XMLWait`

    ``XSD structure:``

    .. code-block::

       Choice@minOccurs=1@maxOccurs=unbounded
           Element@name=assess@minOccurs=1@maxOccurs=1
           Element@name=wait@minOccurs=1@maxOccurs=1
           Element@name=other-listen@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeListen
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='listen'][@type='listen']"


class XMLListening(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/listening/>`_
    
    
    
    ``complexType``: The listen and listening types, new in Version 4.0, specify different ways that a score following or machine listening application can interact with a performer. The listening type handles interactions that change the state of the listening application from the specified point in the performance onward. If multiple child elements of the same type are present, they should have distinct player and/or time-only attributes.
    
    The offset element is used to indicate that the listening change takes place offset from the current score position. If the listening element is a child of a direction element, the listening offset element overrides the direction offset element if both elements are present. Note that the offset reflects the intended musical position for the change in state. It should not be used to compensate for latency issues in particular hardware configurations.

    ``Possible children``:    :obj:`~XMLOffset`, :obj:`~XMLOtherListening`, :obj:`~XMLSync`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Choice@minOccurs=1@maxOccurs=unbounded
               Element@name=sync@minOccurs=1@maxOccurs=1
               Element@name=other-listening@minOccurs=1@maxOccurs=1
           Element@name=offset@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLDirection`, :obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeListening
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='listening'][@type='listening']"


class XMLLyric(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/lyric/>`_
    
    
    
    ``complexType``: The lyric type represents text underlays for lyrics. Two text elements that are not separated by an elision element are part of the same syllable, but may have different text formatting. The MusicXML XSD is more strict than the DTD in enforcing this by disallowing a second syllabic element unless preceded by an elision element. The lyric number indicates multiple lines, though a name can be used as well. Common name examples are verse and chorus.
    
    Justification is center by default; placement is below by default. Vertical alignment is to the baseline of the text and horizontal alignment matches justification. The print-object attribute can override a note's print-lyric attribute in cases where only some lyrics on a note are printed, as when lyrics for later verses are printed in a block of text rather than with each note. The time-only attribute precisely specifies which lyrics are to be sung which time through a repeated section.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``justify``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``name``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNMTOKEN`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``time_only``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeOnly`

    ``Possible children``:    :obj:`~XMLElision`, :obj:`~XMLEndLine`, :obj:`~XMLEndParagraph`, :obj:`~XMLExtend`, :obj:`~XMLFootnote`, :obj:`~XMLHumming`, :obj:`~XMLLaughing`, :obj:`~XMLLevel`, :obj:`~XMLSyllabic`, :obj:`~XMLText`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Choice@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=syllabic@minOccurs=0@maxOccurs=1
                   Element@name=text@minOccurs=1@maxOccurs=1
                   Sequence@minOccurs=0@maxOccurs=unbounded
                       Sequence@minOccurs=0@maxOccurs=1
                           Element@name=elision@minOccurs=1@maxOccurs=1
                           Element@name=syllabic@minOccurs=0@maxOccurs=1
                       Element@name=text@minOccurs=1@maxOccurs=1
                   Element@name=extend@minOccurs=0@maxOccurs=1
               Element@name=extend@minOccurs=1@maxOccurs=1
               Element@name=laughing@minOccurs=1@maxOccurs=1
               Element@name=humming@minOccurs=1@maxOccurs=1
           Element@name=end-line@minOccurs=0@maxOccurs=1
           Element@name=end-paragraph@minOccurs=0@maxOccurs=1
           Group@name=editorial@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=footnote@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=footnote@minOccurs=1@maxOccurs=1
                   Group@name=level@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=level@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeLyric
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='lyric'][@type='lyric']"


class XMLLyricFont(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/lyric-font/>`_
    
    
    
    ``complexType``: The lyric-font type specifies the default font for a particular name and number of lyric.

    ``Possible attributes``: ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``name``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNMTOKEN`

``Possible parents``::obj:`~XMLDefaults`
    """
    
    TYPE = XSDComplexTypeLyricFont
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='lyric-font'][@type='lyric-font']"


class XMLLyricLanguage(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/lyric-language/>`_
    
    
    
    ``complexType``: The lyric-language type specifies the default language for a particular name and number of lyric.

    ``Possible attributes``: ``lang``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLanguage`, ``name``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNMTOKEN`

``Possible parents``::obj:`~XMLDefaults`
    """
    
    TYPE = XSDComplexTypeLyricLanguage
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='lyric-language'][@type='lyric-language']"


class XMLMeasure(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/measure/>`_



    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``implicit``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``non_controlling``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`\@required, ``text``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeMeasureText`, ``width``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

    ``Possible children``:    :obj:`~XMLAttributes`, :obj:`~XMLBackup`, :obj:`~XMLBarline`, :obj:`~XMLBookmark`, :obj:`~XMLDirection`, :obj:`~XMLFiguredBass`, :obj:`~XMLForward`, :obj:`~XMLGrouping`, :obj:`~XMLHarmony`, :obj:`~XMLLink`, :obj:`~XMLListening`, :obj:`~XMLNote`, :obj:`~XMLPrint`, :obj:`~XMLSound`

    ``XSD structure:``

    .. code-block::

       Group@name=music-data@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Choice@minOccurs=0@maxOccurs=unbounded
                   Element@name=note@minOccurs=1@maxOccurs=1
                   Element@name=backup@minOccurs=1@maxOccurs=1
                   Element@name=forward@minOccurs=1@maxOccurs=1
                   Element@name=direction@minOccurs=1@maxOccurs=1
                   Element@name=attributes@minOccurs=1@maxOccurs=1
                   Element@name=harmony@minOccurs=1@maxOccurs=1
                   Element@name=figured-bass@minOccurs=1@maxOccurs=1
                   Element@name=print@minOccurs=1@maxOccurs=1
                   Element@name=sound@minOccurs=1@maxOccurs=1
                   Element@name=listening@minOccurs=1@maxOccurs=1
                   Element@name=barline@minOccurs=1@maxOccurs=1
                   Element@name=grouping@minOccurs=1@maxOccurs=1
                   Element@name=link@minOccurs=1@maxOccurs=1
                   Element@name=bookmark@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLPart`
    """
    
    TYPE = XSDComplexTypeMeasure
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='score-partwise']//{*}element[@name='measure']"


class XMLMeasureDistance(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/measure-distance/>`_
    
    The measure-distance element specifies the horizontal distance from the previous measure. This value is only used for systems where there is horizontal whitespace in the middle of a system, as in systems with codas. To specify the measure width, use the width attribute of the measure element.
    
    
    
    ``simpleType``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

``Possible parents``::obj:`~XMLMeasureLayout`
    """
    
    TYPE = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='measure-distance'][@type='tenths']"


class XMLMeasureLayout(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/measure-layout/>`_
    
    
    
    ``complexType``: The measure-layout type includes the horizontal distance from the previous measure. It applies to the current measure only.

    ``Possible children``:    :obj:`~XMLMeasureDistance`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=measure-distance@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLPrint`
    """
    
    TYPE = XSDComplexTypeMeasureLayout
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='measure-layout'][@type='measure-layout']"


class XMLMeasureNumbering(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/measure-numbering/>`_
    
    
    
    ``complexType``: The measure-numbering type describes how frequently measure numbers are displayed on this part. The text attribute from the measure element is used for display, or the number attribute if the text attribute is not present. Measures with an implicit attribute set to "yes" never display a measure number, regardless of the measure-numbering setting.
    
    The optional staff attribute refers to staff numbers within the part, from top to bottom on the system. It indicates which staff is used as the reference point for vertical positioning. A value of 1 is assumed if not present.
    
    The optional multiple-rest-always and multiple-rest-range attributes describe how measure numbers are shown on multiple rests when the measure-numbering value is not set to none. The multiple-rest-always attribute is set to yes when the measure number should always be shown, even if the multiple rest starts midway through a system when measure numbering is set to system level. The multiple-rest-range attribute is set to yes when measure numbers on multiple rests display the range of numbers for the first and last measure, rather than just the number of the first measure.
    
    ``simpleContent``: The measure-numbering-value type describes how measure numbers are displayed on this part: no numbers, numbers every measure, or numbers every system.
        
        Permitted Values: ``'none'``, ``'measure'``, ``'system'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``multiple_rest_always``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``multiple_rest_range``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``staff``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffNumber`, ``system``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSystemRelationNumber`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLPrint`
    """
    
    TYPE = XSDComplexTypeMeasureNumbering
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='measure-numbering'][@type='measure-numbering']"


class XMLMeasureRepeat(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/measure-repeat/>`_
    
    
    
    ``complexType``: The measure-repeat type is used for both single and multiple measure repeats. The text of the element indicates the number of measures to be repeated in a single pattern. The slashes attribute specifies the number of slashes to use in the repeat sign. It is 1 if not specified. The text of the element is ignored when the type is stop.
    
    The stop type indicates the first measure where the repeats are no longer displayed. Both the start and the stop of the measure-repeat should be specified unless the repeats are displayed through the end of the part.
    
    The measure-repeat element specifies a notation style for repetitions. The actual music being repeated needs to be repeated within each measure of the MusicXML file. This element specifies the notation that indicates the repeat.

    ``Possible attributes``: ``slashes``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePositiveInteger`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required

``Possible parents``::obj:`~XMLMeasureStyle`
    """
    
    TYPE = XSDComplexTypeMeasureRepeat
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='measure-repeat'][@type='measure-repeat']"


class XMLMeasureStyle(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/measure-style/>`_
    
    A measure-style indicates a special way to print partial to multiple measures within a part. This includes multiple rests over several measures, repeats of beats, single, or multiple measures, and use of slash notation.
    
    
    
    ``complexType``: A measure-style indicates a special way to print partial to multiple measures within a part. This includes multiple rests over several measures, repeats of beats, single, or multiple measures, and use of slash notation.
    
    The multiple-rest and measure-repeat elements indicate the number of measures covered in the element content. The beat-repeat and slash elements can cover partial measures. All but the multiple-rest element use a type attribute to indicate starting and stopping the use of the style. The optional number attribute specifies the staff number from top to bottom on the system, as with clef.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffNumber`

    ``Possible children``:    :obj:`~XMLBeatRepeat`, :obj:`~XMLMeasureRepeat`, :obj:`~XMLMultipleRest`, :obj:`~XMLSlash`

    ``XSD structure:``

    .. code-block::

       Choice@minOccurs=1@maxOccurs=1
           Element@name=multiple-rest@minOccurs=1@maxOccurs=1
           Element@name=measure-repeat@minOccurs=1@maxOccurs=1
           Element@name=beat-repeat@minOccurs=1@maxOccurs=1
           Element@name=slash@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLAttributes`
    """
    
    TYPE = XSDComplexTypeMeasureStyle
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='measure-style'][@type='measure-style']"


class XMLMembrane(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/membrane/>`_
    
    
    
    ``complexType``: The membrane type represents pictograms for membrane percussion instruments. The smufl attribute is used to distinguish different SMuFL stylistic alternates.
    
    ``simpleContent``: The membrane-value type represents pictograms for membrane percussion instruments.
        
        Permitted Values: ``'bass drum'``, ``'bass drum on side'``, ``'bongos'``, ``'Chinese tomtom'``, ``'conga drum'``, ``'cuica'``, ``'goblet drum'``, ``'Indo-American tomtom'``, ``'Japanese tomtom'``, ``'military drum'``, ``'snare drum'``, ``'snare drum snares off'``, ``'tabla'``, ``'tambourine'``, ``'tenor drum'``, ``'timbales'``, ``'tomtom'``
    

    ``Possible attributes``: ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflPictogramGlyphName`

``Possible parents``::obj:`~XMLPercussion`
    """
    
    TYPE = XSDComplexTypeMembrane
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='membrane'][@type='membrane']"


class XMLMetal(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/metal/>`_
    
    
    
    ``complexType``: The metal type represents pictograms for metal percussion instruments. The smufl attribute is used to distinguish different SMuFL stylistic alternates.
    
    ``simpleContent``: The metal-value type represents pictograms for metal percussion instruments. The hi-hat value refers to a pictogram like Stone's high-hat cymbals but without the long vertical line at the bottom.
        
        Permitted Values: ``'agogo'``, ``'almglocken'``, ``'bell'``, ``'bell plate'``, ``'bell tree'``, ``'brake drum'``, ``'cencerro'``, ``'chain rattle'``, ``'Chinese cymbal'``, ``'cowbell'``, ``'crash cymbals'``, ``'crotale'``, ``'cymbal tongs'``, ``'domed gong'``, ``'finger cymbals'``, ``'flexatone'``, ``'gong'``, ``'hi-hat'``, ``'high-hat cymbals'``, ``'handbell'``, ``'jaw harp'``, ``'jingle bells'``, ``'musical saw'``, ``'shell bells'``, ``'sistrum'``, ``'sizzle cymbal'``, ``'sleigh bells'``, ``'suspended cymbal'``, ``'tam tam'``, ``'tam tam with beater'``, ``'triangle'``, ``'Vietnamese hat'``
    

    ``Possible attributes``: ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflPictogramGlyphName`

``Possible parents``::obj:`~XMLPercussion`
    """
    
    TYPE = XSDComplexTypeMetal
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='metal'][@type='metal']"


class XMLMetronome(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/metronome/>`_
    
    
    
    ``complexType``: The metronome type represents metronome marks and other metric relationships. The beat-unit group and per-minute element specify regular metronome marks. The metronome-note and metronome-relation elements allow for the specification of metric modulations and other metric relationships, such as swing tempo marks where two eighths are equated to a quarter note / eighth note triplet. Tied notes can be represented in both types of metronome marks by using the beat-unit-tied and metronome-tied elements. The parentheses attribute indicates whether or not to put the metronome mark in parentheses; its value is no if not specified. The print-object attribute is set to no in cases where the metronome element represents a relationship or range that is not displayed in the music notation.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``justify``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``parentheses``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

    ``Possible children``:    :obj:`~XMLBeatUnitDot`, :obj:`~XMLBeatUnitTied`, :obj:`~XMLBeatUnit`, :obj:`~XMLMetronomeArrows`, :obj:`~XMLMetronomeNote`, :obj:`~XMLMetronomeRelation`, :obj:`~XMLPerMinute`

    ``XSD structure:``

    .. code-block::

       Choice@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Group@name=beat-unit@minOccurs=1@maxOccurs=1
                   Sequence@minOccurs=1@maxOccurs=1
                       Element@name=beat-unit@minOccurs=1@maxOccurs=1
                       Element@name=beat-unit-dot@minOccurs=0@maxOccurs=unbounded
               Element@name=beat-unit-tied@minOccurs=0@maxOccurs=unbounded
               Choice@minOccurs=1@maxOccurs=1
                   Element@name=per-minute@minOccurs=1@maxOccurs=1
                   Sequence@minOccurs=1@maxOccurs=1
                       Group@name=beat-unit@minOccurs=1@maxOccurs=1
                           Sequence@minOccurs=1@maxOccurs=1
                               Element@name=beat-unit@minOccurs=1@maxOccurs=1
                               Element@name=beat-unit-dot@minOccurs=0@maxOccurs=unbounded
                       Element@name=beat-unit-tied@minOccurs=0@maxOccurs=unbounded
           Sequence@minOccurs=1@maxOccurs=1
               Element@name=metronome-arrows@minOccurs=0@maxOccurs=1
               Element@name=metronome-note@minOccurs=1@maxOccurs=unbounded
               Sequence@minOccurs=0@maxOccurs=1
                   Element@name=metronome-relation@minOccurs=1@maxOccurs=1
                   Element@name=metronome-note@minOccurs=1@maxOccurs=unbounded

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeMetronome
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='metronome'][@type='metronome']"


class XMLMetronomeArrows(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/metronome-arrows/>`_
    
    If the metronome-arrows element is present, it indicates that metric modulation arrows are displayed on both sides of the metronome mark.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLMetronome`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='metronome-arrows'][@type='empty']"


class XMLMetronomeBeam(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/metronome-beam/>`_
    
    
    
    ``complexType``: The metronome-beam type works like the beam type in defining metric relationships, but does not include all the attributes available in the beam type.
    
    ``simpleContent``: The beam-value type represents the type of beam associated with each of 8 beam levels (up to 1024th notes) available for each note.
        
        Permitted Values: ``'begin'``, ``'continue'``, ``'end'``, ``'forward hook'``, ``'backward hook'``
    

    ``Possible attributes``: ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeBeamLevel`

``Possible parents``::obj:`~XMLMetronomeNote`
    """
    
    TYPE = XSDComplexTypeMetronomeBeam
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='metronome-beam'][@type='metronome-beam']"


class XMLMetronomeDot(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/metronome-dot/>`_
    
    The metronome-dot element works like the dot element in defining metric relationships.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLMetronomeNote`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='metronome-dot'][@type='empty']"


class XMLMetronomeNote(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/metronome-note/>`_
    
    
    
    ``complexType``: The metronome-note type defines the appearance of a note within a metric relationship mark.

    ``Possible children``:    :obj:`~XMLMetronomeBeam`, :obj:`~XMLMetronomeDot`, :obj:`~XMLMetronomeTied`, :obj:`~XMLMetronomeTuplet`, :obj:`~XMLMetronomeType`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=metronome-type@minOccurs=1@maxOccurs=1
           Element@name=metronome-dot@minOccurs=0@maxOccurs=unbounded
           Element@name=metronome-beam@minOccurs=0@maxOccurs=unbounded
           Element@name=metronome-tied@minOccurs=0@maxOccurs=1
           Element@name=metronome-tuplet@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLMetronome`
    """
    
    TYPE = XSDComplexTypeMetronomeNote
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='metronome-note'][@type='metronome-note']"


class XMLMetronomeRelation(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/metronome-relation/>`_

The metronome-relation element describes the relationship symbol that goes between the two sets of metronome-note elements. The currently allowed value is equals, but this may expand in future versions. If the element is empty, the equals value is used.



``Possible parents``::obj:`~XMLMetronome`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='metronome-relation'][@type='xs:string']"


class XMLMetronomeTied(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/metronome-tied/>`_
    
    
    
    ``complexType``: The metronome-tied indicates the presence of a tie within a metric relationship mark. As with the tied element, both the start and stop of the tie should be specified, in this case within separate metronome-note elements.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required

``Possible parents``::obj:`~XMLMetronomeNote`
    """
    
    TYPE = XSDComplexTypeMetronomeTied
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='metronome-tied'][@type='metronome-tied']"


class XMLMetronomeTuplet(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/metronome-tuplet/>`_
    
    
    
    ``complexType``: The metronome-tuplet type uses the same element structure as the time-modification element along with some attributes from the tuplet element.

    ``Possible attributes``: ``bracket``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``show_number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeShowTuplet`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required

    ``Possible children``:    :obj:`~XMLActualNotes`, :obj:`~XMLNormalDot`, :obj:`~XMLNormalNotes`, :obj:`~XMLNormalType`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=actual-notes@minOccurs=1@maxOccurs=1
           Element@name=normal-notes@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=0@maxOccurs=1
               Element@name=normal-type@minOccurs=1@maxOccurs=1
               Element@name=normal-dot@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLMetronomeNote`
    """
    
    TYPE = XSDComplexTypeMetronomeTuplet
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='metronome-tuplet'][@type='metronome-tuplet']"


class XMLMetronomeType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/metronome-type/>`_
    
    The metronome-type element works like the type element in defining metric relationships.
    
    
    
    ``simpleType``: The note-type-value type is used for the MusicXML type element and represents the graphic note type, from 1024th (shortest) to maxima (longest).
        
        Permitted Values: ``'1024th'``, ``'512th'``, ``'256th'``, ``'128th'``, ``'64th'``, ``'32nd'``, ``'16th'``, ``'eighth'``, ``'quarter'``, ``'half'``, ``'whole'``, ``'breve'``, ``'long'``, ``'maxima'``
    

``Possible parents``::obj:`~XMLMetronomeNote`
    """
    
    TYPE = XSDSimpleTypeNoteTypeValue
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='metronome-type'][@type='note-type-value']"


class XMLMf(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/mf/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='mf'][@type='empty']"


class XMLMidiBank(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/midi-bank/>`_
    
    The midi-bank element specifies a MIDI 1.0 bank number ranging from 1 to 16,384.
    
    
    
    ``simpleType``: The midi-16384 type is used to express MIDI 1.0 values that range from 1 to 16,384.

``Possible parents``::obj:`~XMLMidiInstrument`
    """
    
    TYPE = XSDSimpleTypeMidi16384
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='midi-bank'][@type='midi-16384']"


class XMLMidiChannel(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/midi-channel/>`_
    
    The midi-channel element specifies a MIDI 1.0 channel numbers ranging from 1 to 16.
    
    
    
    ``simpleType``: The midi-16 type is used to express MIDI 1.0 values that range from 1 to 16.

``Possible parents``::obj:`~XMLMidiInstrument`
    """
    
    TYPE = XSDSimpleTypeMidi16
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='midi-channel'][@type='midi-16']"


class XMLMidiDevice(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/midi-device/>`_
    
    
    
    ``complexType``: The midi-device type corresponds to the DeviceName meta event in Standard MIDI Files. The optional port attribute is a number from 1 to 16 that can be used with the unofficial MIDI 1.0 port (or cable) meta event. Unlike the DeviceName meta event, there can be multiple midi-device elements per MusicXML part. The optional id attribute refers to the score-instrument assigned to this device. If missing, the device assignment affects all score-instrument elements in the score-part.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF`, ``port``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeMidi16`

``Possible parents``::obj:`~XMLScorePart`, :obj:`~XMLSound`
    """
    
    TYPE = XSDComplexTypeMidiDevice
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='midi-device'][@type='midi-device']"


class XMLMidiInstrument(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/midi-instrument/>`_
    
    
    
    ``complexType``: The midi-instrument type defines MIDI 1.0 instrument playback. The midi-instrument element can be a part of either the score-instrument element at the start of a part, or the sound element within a part. The id attribute refers to the score-instrument affected by the change.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF`\@required

    ``Possible children``:    :obj:`~XMLElevation`, :obj:`~XMLMidiBank`, :obj:`~XMLMidiChannel`, :obj:`~XMLMidiName`, :obj:`~XMLMidiProgram`, :obj:`~XMLMidiUnpitched`, :obj:`~XMLPan`, :obj:`~XMLVolume`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=midi-channel@minOccurs=0@maxOccurs=1
           Element@name=midi-name@minOccurs=0@maxOccurs=1
           Element@name=midi-bank@minOccurs=0@maxOccurs=1
           Element@name=midi-program@minOccurs=0@maxOccurs=1
           Element@name=midi-unpitched@minOccurs=0@maxOccurs=1
           Element@name=volume@minOccurs=0@maxOccurs=1
           Element@name=pan@minOccurs=0@maxOccurs=1
           Element@name=elevation@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLScorePart`, :obj:`~XMLSound`
    """
    
    TYPE = XSDComplexTypeMidiInstrument
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='midi-instrument'][@type='midi-instrument']"


class XMLMidiName(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/midi-name/>`_

The midi-name element corresponds to a ProgramName meta-event within a Standard MIDI File.



``Possible parents``::obj:`~XMLMidiInstrument`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='midi-name'][@type='xs:string']"


class XMLMidiProgram(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/midi-program/>`_
    
    The midi-program element specifies a MIDI 1.0 program number ranging from 1 to 128.
    
    
    
    ``simpleType``: The midi-128 type is used to express MIDI 1.0 values that range from 1 to 128.

``Possible parents``::obj:`~XMLMidiInstrument`
    """
    
    TYPE = XSDSimpleTypeMidi128
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='midi-program'][@type='midi-128']"


class XMLMidiUnpitched(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/midi-unpitched/>`_
    
    For unpitched instruments, the midi-unpitched element specifies a MIDI 1.0 note number ranging from 1 to 128. It is usually used with MIDI banks for percussion. Note that MIDI 1.0 note numbers are generally specified from 0 to 127 rather than the 1 to 128 numbering used in this element.
    
    
    
    ``simpleType``: The midi-128 type is used to express MIDI 1.0 values that range from 1 to 128.

``Possible parents``::obj:`~XMLMidiInstrument`
    """
    
    TYPE = XSDSimpleTypeMidi128
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='midi-unpitched'][@type='midi-128']"


class XMLMillimeters(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/millimeters/>`_
    
    
    
    ``simpleType``: The millimeters type is a number representing millimeters. This is used in the scaling element to provide a default scaling from tenths to physical units.

``Possible parents``::obj:`~XMLScaling`
    """
    
    TYPE = XSDSimpleTypeMillimeters
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='millimeters'][@type='millimeters']"


class XMLMiscellaneous(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/miscellaneous/>`_
    
    
    
    ``complexType``: If a program has other metadata not yet supported in the MusicXML format, it can go in the miscellaneous element. The miscellaneous type puts each separate part of metadata into its own miscellaneous-field type.

    ``Possible children``:    :obj:`~XMLMiscellaneousField`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=miscellaneous-field@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLIdentification`
    """
    
    TYPE = XSDComplexTypeMiscellaneous
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='miscellaneous'][@type='miscellaneous']"


class XMLMiscellaneousField(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/miscellaneous-field/>`_
    
    
    
    ``complexType``: If a program has other metadata not yet supported in the MusicXML format, each type of metadata can go in a miscellaneous-field element. The required name attribute indicates the type of metadata the element content represents.

    ``Possible attributes``: ``name``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`\@required

``Possible parents``::obj:`~XMLMiscellaneous`
    """
    
    TYPE = XSDComplexTypeMiscellaneousField
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='miscellaneous-field'][@type='miscellaneous-field']"


class XMLMode(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/mode/>`_
    
    
    
    ``simpleType``: The mode type is used to specify major/minor and other mode distinctions. Valid mode values include major, minor, dorian, phrygian, lydian, mixolydian, aeolian, ionian, locrian, and none.

``Possible parents``::obj:`~XMLKey`
    """
    
    TYPE = XSDSimpleTypeMode
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='mode'][@type='mode']"


class XMLMordent(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/mordent/>`_
    
    The mordent element represents the sign with the vertical line. The choice of which mordent sign is inverted differs between MusicXML and SMuFL. The long attribute is "no" by default.
    
    
    
    ``complexType``: The mordent type is used for both represents the mordent sign with the vertical line and the inverted-mordent sign without the line. The long attribute is "no" by default. The approach and departure attributes are used for compound ornaments, indicating how the beginning and ending of the ornament look relative to the main part of the mordent.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``approach``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``departure``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``long``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``second_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``start_note``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartNote`, ``trill_step``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillStep`, ``two_note_turn``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTwoNoteTurn`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeMordent
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='mordent'][@type='mordent']"


class XMLMovementNumber(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/movement-number/>`_

The movement-number element specifies the number of a movement.



``Possible parents``::obj:`~XMLScorePartwise`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='movement-number'][@type='xs:string']"


class XMLMovementTitle(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/movement-title/>`_

The movement-title element specifies the title of a movement, not including its number.



``Possible parents``::obj:`~XMLScorePartwise`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='movement-title'][@type='xs:string']"


class XMLMp(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/mp/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='mp'][@type='empty']"


class XMLMultipleRest(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/multiple-rest/>`_
    
    
    
    ``complexType``: The text of the multiple-rest type indicates the number of measures in the multiple rest. Multiple rests may use the 1-bar / 2-bar / 4-bar rest symbols, or a single shape. The use-symbols attribute indicates which to use; it is no if not specified.

    ``Possible attributes``: ``use_symbols``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

``Possible parents``::obj:`~XMLMeasureStyle`
    """
    
    TYPE = XSDComplexTypeMultipleRest
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='multiple-rest'][@type='multiple-rest']"


class XMLMusicFont(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/music-font/>`_
    
    
    
    ``complexType``: The empty-font type represents an empty element with font attributes.

    ``Possible attributes``: ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`

``Possible parents``::obj:`~XMLDefaults`
    """
    
    TYPE = XSDComplexTypeEmptyFont
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='music-font'][@type='empty-font']"


class XMLMute(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/mute/>`_
    
    
    
    ``simpleType``: The mute type represents muting for different instruments, including brass, winds, and strings. The on and off values are used for undifferentiated mutes. The remaining values represent specific mutes.
        
        Permitted Values: ``'on'``, ``'off'``, ``'straight'``, ``'cup'``, ``'harmon-no-stem'``, ``'harmon-stem'``, ``'bucket'``, ``'plunger'``, ``'hat'``, ``'solotone'``, ``'practice'``, ``'stop-mute'``, ``'stop-hand'``, ``'echo'``, ``'palm'``
    

``Possible parents``::obj:`~XMLPlay`
    """
    
    TYPE = XSDSimpleTypeMute
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='mute'][@type='mute']"


class XMLN(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/n/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='n'][@type='empty']"


class XMLNatural(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/natural/>`_
    
    The natural element indicates that this is a natural harmonic. These are usually notated at base pitch rather than sounding pitch.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLHarmonic`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='natural'][@type='empty']"


class XMLNonArpeggiate(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/non-arpeggiate/>`_
    
    
    
    ``complexType``: The non-arpeggiate type indicates that this note is at the top or bottom of a bracket indicating to not arpeggiate these notes. Since this does not involve playback, it is only used on the top or bottom notes, not on each note as for the arpeggiate type.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTopBottom`\@required

``Possible parents``::obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeNonArpeggiate
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='non-arpeggiate'][@type='non-arpeggiate']"


class XMLNormalDot(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/normal-dot/>`_
    
    The normal-dot element is used to specify dotted normal tuplet types.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLMetronomeTuplet`, :obj:`~XMLTimeModification`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='normal-dot'][@type='empty']"


class XMLNormalNotes(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/normal-notes/>`_

The normal-notes element describes how many notes are usually played in the time occupied by the number in the actual-notes element.



``Possible parents``::obj:`~XMLMetronomeTuplet`, :obj:`~XMLTimeModification`
    """
    
    TYPE = XSDSimpleTypeNonNegativeInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='normal-notes'][@type='xs:nonNegativeInteger']"


class XMLNormalType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/normal-type/>`_
    
    If the type associated with the number in the normal-notes element is different than the current note type (e.g., a quarter note within an eighth note triplet), then the normal-notes type (e.g. eighth) is specified in the normal-type and normal-dot elements.
    
    
    
    ``simpleType``: The note-type-value type is used for the MusicXML type element and represents the graphic note type, from 1024th (shortest) to maxima (longest).
        
        Permitted Values: ``'1024th'``, ``'512th'``, ``'256th'``, ``'128th'``, ``'64th'``, ``'32nd'``, ``'16th'``, ``'eighth'``, ``'quarter'``, ``'half'``, ``'whole'``, ``'breve'``, ``'long'``, ``'maxima'``
    

``Possible parents``::obj:`~XMLMetronomeTuplet`, :obj:`~XMLTimeModification`
    """
    
    TYPE = XSDSimpleTypeNoteTypeValue
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='normal-type'][@type='note-type-value']"


class XMLNotations(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/notations/>`_
    
    
    
    ``complexType``: Notations refer to musical notations, not XML notations. Multiple notations are allowed in order to represent multiple editorial levels. The print-object attribute, added in Version 3.0, allows notations to represent details of performance technique, such as fingerings, without having them appear in the score.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

    ``Possible children``:    :obj:`~XMLAccidentalMark`, :obj:`~XMLArpeggiate`, :obj:`~XMLArticulations`, :obj:`~XMLDynamics`, :obj:`~XMLFermata`, :obj:`~XMLFootnote`, :obj:`~XMLGlissando`, :obj:`~XMLLevel`, :obj:`~XMLNonArpeggiate`, :obj:`~XMLOrnaments`, :obj:`~XMLOtherNotation`, :obj:`~XMLSlide`, :obj:`~XMLSlur`, :obj:`~XMLTechnical`, :obj:`~XMLTied`, :obj:`~XMLTuplet`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Group@name=editorial@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=footnote@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=footnote@minOccurs=1@maxOccurs=1
                   Group@name=level@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=level@minOccurs=1@maxOccurs=1
           Choice@minOccurs=0@maxOccurs=unbounded
               Element@name=tied@minOccurs=1@maxOccurs=1
               Element@name=slur@minOccurs=1@maxOccurs=1
               Element@name=tuplet@minOccurs=1@maxOccurs=1
               Element@name=glissando@minOccurs=1@maxOccurs=1
               Element@name=slide@minOccurs=1@maxOccurs=1
               Element@name=ornaments@minOccurs=1@maxOccurs=1
               Element@name=technical@minOccurs=1@maxOccurs=1
               Element@name=articulations@minOccurs=1@maxOccurs=1
               Element@name=dynamics@minOccurs=1@maxOccurs=1
               Element@name=fermata@minOccurs=1@maxOccurs=1
               Element@name=arpeggiate@minOccurs=1@maxOccurs=1
               Element@name=non-arpeggiate@minOccurs=1@maxOccurs=1
               Element@name=accidental-mark@minOccurs=1@maxOccurs=1
               Element@name=other-notation@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeNotations
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='notations'][@type='notations']"


class XMLNote(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/note/>`_
    
    
    
    ``complexType``: Notes are the most common type of MusicXML data. The MusicXML format distinguishes between elements used for sound information and elements used for notation information (e.g., tie is used for sound, tied for notation). Thus grace notes do not have a duration element. Cue notes have a duration element, as do forward elements, but no tie elements. Having these two types of information available can make interchange easier, as some programs handle one type of information more readily than the other.
    
    The print-leger attribute is used to indicate whether leger lines are printed. Notes without leger lines are used to indicate indeterminate high and low notes. By default, it is set to yes. If print-object is set to no, print-leger is interpreted to also be set to no if not present. This attribute is ignored for rests.
    
    The dynamics and end-dynamics attributes correspond to MIDI 1.0's Note On and Note Off velocities, respectively. They are expressed in terms of percentages of the default forte value (90 for MIDI 1.0).
    
    The attack and release attributes are used to alter the starting and stopping time of the note from when it would otherwise occur based on the flow of durations - information that is specific to a performance. They are expressed in terms of divisions, either positive or negative. A note that starts a tie should not have a release attribute, and a note that stops a tie should not have an attack attribute. The attack and release attributes are independent of each other. The attack attribute only changes the starting time of a note, and the release attribute only changes the stopping time of a note.
    
    If a note is played only particular times through a repeat, the time-only attribute shows which times to play the note.
    
    The pizzicato attribute is used when just this note is sounded pizzicato, vs. the pizzicato element which changes overall playback between pizzicato and arco.
    

    ``Possible attributes``: ``attack``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeDivisions`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``dynamics``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNonNegativeDecimal`, ``end_dynamics``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNonNegativeDecimal`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``pizzicato``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``print_dot``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``print_leger``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``print_lyric``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``print_spacing``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``release``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeDivisions`, ``time_only``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeOnly`

    ``Possible children``:    :obj:`~XMLAccidental`, :obj:`~XMLBeam`, :obj:`~XMLChord`, :obj:`~XMLCue`, :obj:`~XMLDot`, :obj:`~XMLDuration`, :obj:`~XMLFootnote`, :obj:`~XMLGrace`, :obj:`~XMLInstrument`, :obj:`~XMLLevel`, :obj:`~XMLListen`, :obj:`~XMLLyric`, :obj:`~XMLNotations`, :obj:`~XMLNoteheadText`, :obj:`~XMLNotehead`, :obj:`~XMLPitch`, :obj:`~XMLPlay`, :obj:`~XMLRest`, :obj:`~XMLStaff`, :obj:`~XMLStem`, :obj:`~XMLTie`, :obj:`~XMLTimeModification`, :obj:`~XMLType`, :obj:`~XMLUnpitched`, :obj:`~XMLVoice`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Choice@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=full-note@minOccurs=1@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=chord@minOccurs=0@maxOccurs=1
                           Choice@minOccurs=1@maxOccurs=1
                               Element@name=pitch@minOccurs=1@maxOccurs=1
                               Element@name=unpitched@minOccurs=1@maxOccurs=1
                               Element@name=rest@minOccurs=1@maxOccurs=1
                   Group@name=duration@minOccurs=1@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=duration@minOccurs=1@maxOccurs=1
                   Element@name=tie@minOccurs=0@maxOccurs=2
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=cue@minOccurs=1@maxOccurs=1
                   Group@name=full-note@minOccurs=1@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=chord@minOccurs=0@maxOccurs=1
                           Choice@minOccurs=1@maxOccurs=1
                               Element@name=pitch@minOccurs=1@maxOccurs=1
                               Element@name=unpitched@minOccurs=1@maxOccurs=1
                               Element@name=rest@minOccurs=1@maxOccurs=1
                   Group@name=duration@minOccurs=1@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=duration@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=grace@minOccurs=1@maxOccurs=1
                   Choice@minOccurs=1@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Group@name=full-note@minOccurs=1@maxOccurs=1
                               Sequence@minOccurs=1@maxOccurs=1
                                   Element@name=chord@minOccurs=0@maxOccurs=1
                                   Choice@minOccurs=1@maxOccurs=1
                                       Element@name=pitch@minOccurs=1@maxOccurs=1
                                       Element@name=unpitched@minOccurs=1@maxOccurs=1
                                       Element@name=rest@minOccurs=1@maxOccurs=1
                           Element@name=tie@minOccurs=0@maxOccurs=2
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=cue@minOccurs=1@maxOccurs=1
                           Group@name=full-note@minOccurs=1@maxOccurs=1
                               Sequence@minOccurs=1@maxOccurs=1
                                   Element@name=chord@minOccurs=0@maxOccurs=1
                                   Choice@minOccurs=1@maxOccurs=1
                                       Element@name=pitch@minOccurs=1@maxOccurs=1
                                       Element@name=unpitched@minOccurs=1@maxOccurs=1
                                       Element@name=rest@minOccurs=1@maxOccurs=1
           Element@name=instrument@minOccurs=0@maxOccurs=unbounded
           Group@name=editorial-voice@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=footnote@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=footnote@minOccurs=1@maxOccurs=1
                   Group@name=level@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=level@minOccurs=1@maxOccurs=1
                   Group@name=voice@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=voice@minOccurs=1@maxOccurs=1
           Element@name=type@minOccurs=0@maxOccurs=1
           Element@name=dot@minOccurs=0@maxOccurs=unbounded
           Element@name=accidental@minOccurs=0@maxOccurs=1
           Element@name=time-modification@minOccurs=0@maxOccurs=1
           Element@name=stem@minOccurs=0@maxOccurs=1
           Element@name=notehead@minOccurs=0@maxOccurs=1
           Element@name=notehead-text@minOccurs=0@maxOccurs=1
           Group@name=staff@minOccurs=0@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=staff@minOccurs=1@maxOccurs=1
           Element@name=beam@minOccurs=0@maxOccurs=8
           Element@name=notations@minOccurs=0@maxOccurs=unbounded
           Element@name=lyric@minOccurs=0@maxOccurs=unbounded
           Element@name=play@minOccurs=0@maxOccurs=1
           Element@name=listen@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeNote
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='note'][@type='note']"


class XMLNoteSize(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/note-size/>`_
    
    
    
    ``complexType``: The note-size type indicates the percentage of the regular note size to use for notes with a cue and large size as defined in the type element. The grace type is used for notes of cue size that that include a grace element. The cue type is used for all other notes with cue size, whether defined explicitly or implicitly via a cue element. The large type is used for notes of large size. The text content represent the numeric percentage. A value of 100 would be identical to the size of a regular note as defined by the music font.
    
    ``simpleContent``: The non-negative-decimal type specifies a non-negative decimal value.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNoteSizeType`\@required

``Possible parents``::obj:`~XMLAppearance`
    """
    
    TYPE = XSDComplexTypeNoteSize
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='note-size'][@type='note-size']"


class XMLNotehead(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/notehead/>`_
    
    
    
    ``complexType``: The notehead type indicates shapes other than the open and closed ovals associated with note durations. 
    
    The smufl attribute can be used to specify a particular notehead, allowing application interoperability without requiring every SMuFL glyph to have a MusicXML element equivalent. This attribute can be used either with the "other" value, or to refine a specific notehead value such as "cluster". Noteheads in the SMuFL Note name noteheads and Note name noteheads supplement ranges (U+E150–U+E1AF and U+EEE0–U+EEFF) should not use the smufl attribute or the "other" value, but instead use the notehead-text element.
    
    For the enclosed shapes, the default is to be hollow for half notes and longer, and filled otherwise. The filled attribute can be set to change this if needed.
    
    If the parentheses attribute is set to yes, the notehead is parenthesized. It is no by default.
    
    ``simpleContent``: The notehead-value type indicates shapes other than the open and closed ovals associated with note durations. 
    
    The values do, re, mi, fa, fa up, so, la, and ti correspond to Aikin's 7-shape system.  The fa up shape is typically used with upstems; the fa shape is typically used with downstems or no stems.
    
    The arrow shapes differ from triangle and inverted triangle by being centered on the stem. Slashed and back slashed notes include both the normal notehead and a slash. The triangle shape has the tip of the triangle pointing up; the inverted triangle shape has the tip of the triangle pointing down. The left triangle shape is a right triangle with the hypotenuse facing up and to the left.
    
    The other notehead covers noteheads other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL notehead. The smufl attribute may be used with any notehead value to help specify the appearance of symbols that share the same MusicXML semantics. Noteheads in the SMuFL Note name noteheads and Note name noteheads supplement ranges (U+E150–U+E1AF and U+EEE0–U+EEFF) should not use the smufl attribute or the "other" value, but instead use the notehead-text element.
        
        Permitted Values: ``'slash'``, ``'triangle'``, ``'diamond'``, ``'square'``, ``'cross'``, ``'x'``, ``'circle-x'``, ``'inverted triangle'``, ``'arrow down'``, ``'arrow up'``, ``'circled'``, ``'slashed'``, ``'back slashed'``, ``'normal'``, ``'cluster'``, ``'circle dot'``, ``'left triangle'``, ``'rectangle'``, ``'none'``, ``'do'``, ``'re'``, ``'mi'``, ``'fa'``, ``'fa up'``, ``'so'``, ``'la'``, ``'ti'``, ``'other'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``filled``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``parentheses``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeNotehead
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='notehead'][@type='notehead']"


class XMLNoteheadText(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/notehead-text/>`_
    
    
    
    ``complexType``: The notehead-text type represents text that is displayed inside a notehead, as is done in some educational music. It is not needed for the numbers used in tablature or jianpu notation. The presence of a TAB or jianpu clefs is sufficient to indicate that numbers are used. The display-text and accidental-text elements allow display of fully formatted text and accidentals.

    ``Possible children``:    :obj:`~XMLAccidentalText`, :obj:`~XMLDisplayText`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Choice@minOccurs=1@maxOccurs=unbounded
               Element@name=display-text@minOccurs=1@maxOccurs=1
               Element@name=accidental-text@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeNoteheadText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='notehead-text'][@type='notehead-text']"


class XMLNumeral(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/numeral/>`_
    
    
    
    ``complexType``: The numeral type represents the Roman numeral or Nashville number part of a harmony. It requires that the key be specified in the encoding, either with a key or numeral-key element.

    ``Possible children``:    :obj:`~XMLNumeralAlter`, :obj:`~XMLNumeralKey`, :obj:`~XMLNumeralRoot`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=numeral-root@minOccurs=1@maxOccurs=1
           Element@name=numeral-alter@minOccurs=0@maxOccurs=1
           Element@name=numeral-key@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLHarmony`
    """
    
    TYPE = XSDComplexTypeNumeral
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='numeral'][@type='numeral']"


class XMLNumeralAlter(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/numeral-alter/>`_
    
    The numeral-alter element represents an alteration to the numeral-root, similar to the alter element for a pitch. The print-object attribute can be used to hide an alteration in cases such as when the MusicXML encoding of a 6 or 7 numeral-root in a minor key requires an alteration that is not displayed. The location attribute indicates whether the alteration should appear to the left or the right of the numeral-root. It is left by default.
    
    
    
    ``complexType``: The harmony-alter type represents the chromatic alteration of the root, numeral, or bass of the current harmony-chord group within the harmony element. In some chord styles, the text of the preceding element may include alteration information. In that case, the print-object attribute of this type can be set to no. The location attribute indicates whether the alteration should appear to the left or the right of the preceding element. Its default value varies by element.
    
    ``simpleContent``: The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``location``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftRight`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLNumeral`
    """
    
    TYPE = XSDComplexTypeHarmonyAlter
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='numeral-alter'][@type='harmony-alter']"


class XMLNumeralFifths(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/numeral-fifths/>`_
    
    
    
    ``simpleType``: The fifths type represents the number of flats or sharps in a traditional key signature. Negative numbers are used for flats and positive numbers for sharps, reflecting the key's placement within the circle of fifths (hence the type name).

``Possible parents``::obj:`~XMLNumeralKey`
    """
    
    TYPE = XSDSimpleTypeFifths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='numeral-fifths'][@type='fifths']"


class XMLNumeralKey(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/numeral-key/>`_
    
    
    
    ``complexType``: The numeral-key type is used when the key for the numeral is different than the key specified by the key signature. The numeral-fifths element specifies the key in the same way as the fifths element. The numeral-mode element specifies the mode similar to the mode element, but with a restricted set of values

    ``Possible attributes``: ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

    ``Possible children``:    :obj:`~XMLNumeralFifths`, :obj:`~XMLNumeralMode`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=numeral-fifths@minOccurs=1@maxOccurs=1
           Element@name=numeral-mode@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLNumeral`
    """
    
    TYPE = XSDComplexTypeNumeralKey
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='numeral-key'][@type='numeral-key']"


class XMLNumeralMode(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/numeral-mode/>`_
    
    
    
    ``simpleType``: The numeral-mode type specifies the mode similar to the mode type, but with a restricted set of values. The different minor values are used to interpret numeral-root values of 6 and 7 when present in a minor key. The harmonic minor value sharpens the 7 and the melodic minor value sharpens both 6 and 7. If a minor mode is used without qualification, either in the mode or numeral-mode elements, natural minor is used.
        
        Permitted Values: ``'major'``, ``'minor'``, ``'natural minor'``, ``'melodic minor'``, ``'harmonic minor'``
    

``Possible parents``::obj:`~XMLNumeralKey`
    """
    
    TYPE = XSDSimpleTypeNumeralMode
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='numeral-mode'][@type='numeral-mode']"


class XMLNumeralRoot(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/numeral-root/>`_
    
    
    
    ``complexType``: The numeral-root type represents the Roman numeral or Nashville number as a positive integer from 1 to 7. The text attribute indicates how the numeral should appear in the score. A numeral-root value of 5 with a kind of major would have a text attribute of "V" if displayed as a Roman numeral, and "5" if displayed as a Nashville number. If the text attribute is not specified, the display is application-dependent.
    
    ``simpleContent``: The numeral-value type represents a Roman numeral or Nashville number value as a positive integer from 1 to 7.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``text``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLNumeral`
    """
    
    TYPE = XSDComplexTypeNumeralRoot
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='numeral-root'][@type='numeral-root']"


class XMLOctave(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/octave/>`_
    
    
    
    ``simpleType``: Octaves are represented by the numbers 0 to 9, where 4 indicates the octave started by middle C.

``Possible parents``::obj:`~XMLPitch`
    """
    
    TYPE = XSDSimpleTypeOctave
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='octave'][@type='octave']"


class XMLOctaveChange(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/octave-change/>`_

The octave-change element indicates how many octaves to add to get from written pitch to sounding pitch. The octave-change element should be included when using transposition intervals of an octave or more, and should not be present for intervals of less than an octave.



``Possible parents``::obj:`~XMLPartTranspose`, :obj:`~XMLTranspose`
    """
    
    TYPE = XSDSimpleTypeInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='octave-change'][@type='xs:integer']"


class XMLOctaveShift(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/octave-shift/>`_
    
    
    
    ``complexType``: The octave shift type indicates where notes are shifted up or down from their true pitched values because of printing difficulty. Thus a treble clef line noted with 8va will be indicated with an octave-shift down from the pitch data indicated in the notes. A size of 8 indicates one octave; a size of 15 indicates two octaves.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dash_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePositiveInteger`, ``space_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeUpDownStopContinue`\@required

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeOctaveShift
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='octave-shift'][@type='octave-shift']"


class XMLOffset(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/offset/>`_
    
    
    
    ``complexType``: An offset is represented in terms of divisions, and indicates where the direction will appear relative to the current musical location. The current musical location is always within the current measure, even at the end of a measure.
    
    The offset affects the visual appearance of the direction. If the sound attribute is "yes", then the offset affects playback and listening too. If the sound attribute is "no", then any sound or listening associated with the direction takes effect at the current location. The sound attribute is "no" by default for compatibility with earlier versions of the MusicXML format. If an element within a direction includes a default-x attribute, the offset value will be ignored when determining the appearance of that element.
    
    ``simpleContent``: The divisions type is used to express values in terms of the musical divisions defined by the divisions element. It is preferred that these be integer values both for MIDI interoperability and to avoid roundoff errors.

    ``Possible attributes``: ``sound``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

``Possible parents``::obj:`~XMLDirection`, :obj:`~XMLHarmony`, :obj:`~XMLListening`, :obj:`~XMLSound`
    """
    
    TYPE = XSDComplexTypeOffset
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='offset'][@type='offset']"


class XMLOpen(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/open/>`_
    
    The open element represents the open symbol, which looks like a circle. The smufl attribute can be used to distinguish different SMuFL glyphs that have a similar appearance such as brassMuteOpen and guitarOpenPedal. If not present, the default glyph is brassMuteOpen.
    
    
    
    ``complexType``: The empty-placement-smufl type represents an empty element with print-style, placement, and smufl attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacementSmufl
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='open'][@type='empty-placement-smufl']"


class XMLOpenString(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/open-string/>`_
    
    The open-string element represents the zero-shaped open string symbol.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='open-string'][@type='empty-placement']"


class XMLOpus(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/opus/>`_
    
    
    
    ``complexType``: The opus type represents a link to a MusicXML opus document that composes multiple MusicXML scores into a collection.

``Possible parents``::obj:`~XMLWork`
    """
    
    TYPE = XSDComplexTypeOpus
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='opus'][@type='opus']"


class XMLOrnaments(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/ornaments/>`_
    
    
    
    ``complexType``: Ornaments can be any of several types, followed optionally by accidentals. The accidental-mark element's content is represented the same as an accidental element, but with a different name to reflect the different musical meaning.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`

    ``Possible children``:    :obj:`~XMLAccidentalMark`, :obj:`~XMLDelayedInvertedTurn`, :obj:`~XMLDelayedTurn`, :obj:`~XMLHaydn`, :obj:`~XMLInvertedMordent`, :obj:`~XMLInvertedTurn`, :obj:`~XMLInvertedVerticalTurn`, :obj:`~XMLMordent`, :obj:`~XMLOtherOrnament`, :obj:`~XMLSchleifer`, :obj:`~XMLShake`, :obj:`~XMLTremolo`, :obj:`~XMLTrillMark`, :obj:`~XMLTurn`, :obj:`~XMLVerticalTurn`, :obj:`~XMLWavyLine`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=0@maxOccurs=unbounded
           Choice@minOccurs=1@maxOccurs=1
               Element@name=trill-mark@minOccurs=1@maxOccurs=1
               Element@name=turn@minOccurs=1@maxOccurs=1
               Element@name=delayed-turn@minOccurs=1@maxOccurs=1
               Element@name=inverted-turn@minOccurs=1@maxOccurs=1
               Element@name=delayed-inverted-turn@minOccurs=1@maxOccurs=1
               Element@name=vertical-turn@minOccurs=1@maxOccurs=1
               Element@name=inverted-vertical-turn@minOccurs=1@maxOccurs=1
               Element@name=shake@minOccurs=1@maxOccurs=1
               Element@name=wavy-line@minOccurs=1@maxOccurs=1
               Element@name=mordent@minOccurs=1@maxOccurs=1
               Element@name=inverted-mordent@minOccurs=1@maxOccurs=1
               Element@name=schleifer@minOccurs=1@maxOccurs=1
               Element@name=tremolo@minOccurs=1@maxOccurs=1
               Element@name=haydn@minOccurs=1@maxOccurs=1
               Element@name=other-ornament@minOccurs=1@maxOccurs=1
           Element@name=accidental-mark@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeOrnaments
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='ornaments'][@type='ornaments']"


class XMLOtherAppearance(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/other-appearance/>`_
    
    
    
    ``complexType``: The other-appearance type is used to define any graphical settings not yet in the current version of the MusicXML format. This allows extended representation, though without application interoperability.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`\@required

``Possible parents``::obj:`~XMLAppearance`
    """
    
    TYPE = XSDComplexTypeOtherAppearance
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='other-appearance'][@type='other-appearance']"


class XMLOtherArticulation(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/other-articulation/>`_
    
    The other-articulation element is used to define any articulations not yet in the MusicXML format. The smufl attribute can be used to specify a particular articulation, allowing application interoperability without requiring every SMuFL articulation to have a MusicXML element equivalent. Using the other-articulation element without the smufl attribute allows for extended representation, though without application interoperability.
    
    
    
    ``complexType``: The other-placement-text type represents a text element with print-style, placement, and smufl attribute groups. This type is used by MusicXML notation extension elements to allow specification of specific SMuFL glyphs without needed to add every glyph as a MusicXML element.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeOtherPlacementText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='other-articulation'][@type='other-placement-text']"


class XMLOtherDirection(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/other-direction/>`_
    
    
    
    ``complexType``: The other-direction type is used to define any direction symbols not yet in the MusicXML format. The smufl attribute can be used to specify a particular direction symbol, allowing application interoperability without requiring every SMuFL glyph to have a MusicXML element equivalent. Using the other-direction type without the smufl attribute allows for extended representation, though without application interoperability.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeOtherDirection
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='other-direction'][@type='other-direction']"


class XMLOtherDynamics(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/other-dynamics/>`_
    
    
    
    ``complexType``: The other-text type represents a text element with a smufl attribute group. This type is used by MusicXML direction extension elements to allow specification of specific SMuFL glyphs without needed to add every glyph as a MusicXML element.

    ``Possible attributes``: ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeOtherText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='other-dynamics'][@type='other-text']"


class XMLOtherListen(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/other-listen/>`_
    
    
    
    ``complexType``: The other-listening type represents other types of listening control and interaction. The required type attribute indicates the type of listening to which the element content applies. The optional player and time-only attributes restrict the element to apply to a single player or set of times through a repeated section, respectively.

    ``Possible attributes``: ``player``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF`, ``time_only``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeOnly`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`\@required

``Possible parents``::obj:`~XMLListen`
    """
    
    TYPE = XSDComplexTypeOtherListening
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='other-listen'][@type='other-listening']"


class XMLOtherListening(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/other-listening/>`_
    
    
    
    ``complexType``: The other-listening type represents other types of listening control and interaction. The required type attribute indicates the type of listening to which the element content applies. The optional player and time-only attributes restrict the element to apply to a single player or set of times through a repeated section, respectively.

    ``Possible attributes``: ``player``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF`, ``time_only``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeOnly`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`\@required

``Possible parents``::obj:`~XMLListening`
    """
    
    TYPE = XSDComplexTypeOtherListening
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='other-listening'][@type='other-listening']"


class XMLOtherNotation(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/other-notation/>`_
    
    
    
    ``complexType``: The other-notation type is used to define any notations not yet in the MusicXML format. It handles notations where more specific extension elements such as other-dynamics and other-technical are not appropriate. The smufl attribute can be used to specify a particular notation, allowing application interoperability without requiring every SMuFL glyph to have a MusicXML element equivalent. Using the other-notation type without the smufl attribute allows for extended representation, though without application interoperability.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStopSingle`\@required

``Possible parents``::obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeOtherNotation
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='other-notation'][@type='other-notation']"


class XMLOtherOrnament(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/other-ornament/>`_
    
    The other-ornament element is used to define any ornaments not yet in the MusicXML format. The smufl attribute can be used to specify a particular ornament, allowing application interoperability without requiring every SMuFL ornament to have a MusicXML element equivalent. Using the other-ornament element without the smufl attribute allows for extended representation, though without application interoperability.
    
    
    
    ``complexType``: The other-placement-text type represents a text element with print-style, placement, and smufl attribute groups. This type is used by MusicXML notation extension elements to allow specification of specific SMuFL glyphs without needed to add every glyph as a MusicXML element.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeOtherPlacementText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='other-ornament'][@type='other-placement-text']"


class XMLOtherPercussion(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/other-percussion/>`_
    
    The other-percussion element represents percussion pictograms not defined elsewhere.
    
    
    
    ``complexType``: The other-text type represents a text element with a smufl attribute group. This type is used by MusicXML direction extension elements to allow specification of specific SMuFL glyphs without needed to add every glyph as a MusicXML element.

    ``Possible attributes``: ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`

``Possible parents``::obj:`~XMLPercussion`
    """
    
    TYPE = XSDComplexTypeOtherText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='other-percussion'][@type='other-text']"


class XMLOtherPlay(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/other-play/>`_
    
    
    
    ``complexType``: The other-play element represents other types of playback. The required type attribute indicates the type of playback to which the element content applies.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`\@required

``Possible parents``::obj:`~XMLPlay`
    """
    
    TYPE = XSDComplexTypeOtherPlay
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='other-play'][@type='other-play']"


class XMLOtherTechnical(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/other-technical/>`_
    
    The other-technical element is used to define any technical indications not yet in the MusicXML format. The smufl attribute can be used to specify a particular glyph, allowing application interoperability without requiring every SMuFL technical indication to have a MusicXML element equivalent. Using the other-technical element without the smufl attribute allows for extended representation, though without application interoperability.
    
    
    
    ``complexType``: The other-placement-text type represents a text element with print-style, placement, and smufl attribute groups. This type is used by MusicXML notation extension elements to allow specification of specific SMuFL glyphs without needed to add every glyph as a MusicXML element.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeOtherPlacementText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='other-technical'][@type='other-placement-text']"


class XMLP(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/p/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='p'][@type='empty']"


class XMLPageHeight(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/page-height/>`_
    
    
    
    ``simpleType``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

``Possible parents``::obj:`~XMLPageLayout`
    """
    
    TYPE = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='page-height'][@type='tenths']"


class XMLPageLayout(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/page-layout/>`_
    
    
    
    ``complexType``: Page layout can be defined both in score-wide defaults and in the print element. Page margins are specified either for both even and odd pages, or via separate odd and even page number values. The type is not needed when used as part of a print element. If omitted when used in the defaults element, "both" is the default.
    
    If no page-layout element is present in the defaults element, default page layout values are chosen by the application.
    
    When used in the print element, the page-layout element affects the appearance of the current page only. All other pages use the default values as determined by the defaults element. If any child elements are missing from the page-layout element in a print element, the values determined by the defaults element are used there as well.

    ``Possible children``:    :obj:`~XMLPageHeight`, :obj:`~XMLPageMargins`, :obj:`~XMLPageWidth`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=0@maxOccurs=1
               Element@name=page-height@minOccurs=1@maxOccurs=1
               Element@name=page-width@minOccurs=1@maxOccurs=1
           Element@name=page-margins@minOccurs=0@maxOccurs=2

``Possible parents``::obj:`~XMLDefaults`, :obj:`~XMLPrint`
    """
    
    TYPE = XSDComplexTypePageLayout
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='page-layout'][@type='page-layout']"


class XMLPageMargins(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/page-margins/>`_
    
    
    
    ``complexType``: Page margins are specified either for both even and odd pages, or via separate odd and even page number values. The type attribute is not needed when used as part of a print element. If omitted when the page-margins type is used in the defaults element, "both" is the default value.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeMarginType`

    ``Possible children``:    :obj:`~XMLBottomMargin`, :obj:`~XMLLeftMargin`, :obj:`~XMLRightMargin`, :obj:`~XMLTopMargin`

    ``XSD structure:``

    .. code-block::

       Group@name=all-margins@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Group@name=left-right-margins@minOccurs=1@maxOccurs=1
                   Sequence@minOccurs=1@maxOccurs=1
                       Element@name=left-margin@minOccurs=1@maxOccurs=1
                       Element@name=right-margin@minOccurs=1@maxOccurs=1
               Element@name=top-margin@minOccurs=1@maxOccurs=1
               Element@name=bottom-margin@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLPageLayout`
    """
    
    TYPE = XSDComplexTypePageMargins
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='page-margins'][@type='page-margins']"


class XMLPageWidth(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/page-width/>`_
    
    
    
    ``simpleType``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

``Possible parents``::obj:`~XMLPageLayout`
    """
    
    TYPE = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='page-width'][@type='tenths']"


class XMLPan(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pan/>`_
    
    The pan and elevation elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For pan, 0 is straight ahead, -90 is hard left, 90 is hard right, and -180 and 180 are directly behind the listener.
    
    
    
    ``simpleType``: The rotation-degrees type specifies rotation, pan, and elevation values in degrees. Values range from -180 to 180.

``Possible parents``::obj:`~XMLMidiInstrument`
    """
    
    TYPE = XSDSimpleTypeRotationDegrees
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pan'][@type='rotation-degrees']"


class XMLPart(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/part/>`_



    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF`\@required

    ``Possible children``:    :obj:`~XMLMeasure`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=measure@minOccurs=1@maxOccurs=unbounded

``Possible parents``::obj:`~XMLScorePartwise`
    """
    
    TYPE = XSDComplexTypePart
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='score-partwise']//{*}element[@name='part']"


class XMLPartAbbreviation(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/part-abbreviation/>`_
    
    
    
    ``complexType``: The part-name type describes the name or abbreviation of a score-part element. Formatting attributes for the part-name element are deprecated in Version 2.0 in favor of the new part-name-display and part-abbreviation-display elements.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``justify``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLScorePart`
    """
    
    TYPE = XSDComplexTypePartName
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='part-abbreviation'][@type='part-name']"


class XMLPartAbbreviationDisplay(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/part-abbreviation-display/>`_
    
    
    
    ``complexType``: The name-display type is used for exact formatting of multi-font text in part and group names to the left of the system. The print-object attribute can be used to determine what, if anything, is printed at the start of each system. Enclosure for the display-text element is none by default. Language for the display-text element is Italian ("it") by default.

    ``Possible attributes``: ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

    ``Possible children``:    :obj:`~XMLAccidentalText`, :obj:`~XMLDisplayText`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Choice@minOccurs=0@maxOccurs=unbounded
               Element@name=display-text@minOccurs=1@maxOccurs=1
               Element@name=accidental-text@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLPrint`, :obj:`~XMLScorePart`
    """
    
    TYPE = XSDComplexTypeNameDisplay
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='part-abbreviation-display'][@type='name-display']"


class XMLPartClef(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/part-clef/>`_
    
    The part-clef element is used for transpositions that also include a change of clef, as for instruments such as bass clarinet.
    
    
    
    ``complexType``: The child elements of the part-clef type have the same meaning as for the clef type. However that meaning applies to a transposed part created from the existing score file.

    ``Possible children``:    :obj:`~XMLClefOctaveChange`, :obj:`~XMLLine`, :obj:`~XMLSign`

    ``XSD structure:``

    .. code-block::

       Group@name=clef@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Element@name=sign@minOccurs=1@maxOccurs=1
               Element@name=line@minOccurs=0@maxOccurs=1
               Element@name=clef-octave-change@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLForPart`
    """
    
    TYPE = XSDComplexTypePartClef
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='part-clef'][@type='part-clef']"


class XMLPartGroup(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/part-group/>`_
    
    
    
    ``complexType``: The part-group element indicates groupings of parts in the score, usually indicated by braces and brackets. Braces that are used for multi-staff parts should be defined in the attributes element for that part. The part-group start element appears before the first score-part in the group. The part-group stop element appears after the last score-part in the group.
    
    The number attribute is used to distinguish overlapping and nested part-groups, not the sequence of groups. As with parts, groups can have a name and abbreviation. Values for the child elements are ignored at the stop of a group.
    
    A part-group element is not needed for a single multi-staff part. By default, multi-staff parts include a brace symbol and (if appropriate given the bar-style) common barlines. The symbol formatting for a multi-staff part can be more fully specified using the part-symbol element.

    ``Possible attributes``: ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required

    ``Possible children``:    :obj:`~XMLFootnote`, :obj:`~XMLGroupAbbreviationDisplay`, :obj:`~XMLGroupAbbreviation`, :obj:`~XMLGroupBarline`, :obj:`~XMLGroupNameDisplay`, :obj:`~XMLGroupName`, :obj:`~XMLGroupSymbol`, :obj:`~XMLGroupTime`, :obj:`~XMLLevel`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=group-name@minOccurs=0@maxOccurs=1
           Element@name=group-name-display@minOccurs=0@maxOccurs=1
           Element@name=group-abbreviation@minOccurs=0@maxOccurs=1
           Element@name=group-abbreviation-display@minOccurs=0@maxOccurs=1
           Element@name=group-symbol@minOccurs=0@maxOccurs=1
           Element@name=group-barline@minOccurs=0@maxOccurs=1
           Element@name=group-time@minOccurs=0@maxOccurs=1
           Group@name=editorial@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Group@name=footnote@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=footnote@minOccurs=1@maxOccurs=1
                   Group@name=level@minOccurs=0@maxOccurs=1
                       Sequence@minOccurs=1@maxOccurs=1
                           Element@name=level@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLPartList`
    """
    
    TYPE = XSDComplexTypePartGroup
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='part-group'][@type='part-group']"


class XMLPartLink(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/part-link/>`_
    
    
    
    ``complexType``: The part-link type allows MusicXML data for both score and parts to be contained within a single compressed MusicXML file. It links a score-part from a score document to MusicXML documents that contain parts data. In the case of a single compressed MusicXML file, the link href values are paths that are relative to the root folder of the zip file.

    ``Possible children``:    :obj:`~XMLGroupLink`, :obj:`~XMLInstrumentLink`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=instrument-link@minOccurs=0@maxOccurs=unbounded
           Element@name=group-link@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLScorePart`
    """
    
    TYPE = XSDComplexTypePartLink
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='part-link'][@type='part-link']"


class XMLPartList(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/part-list/>`_
    
    
    
    ``complexType``: The part-list identifies the different musical parts in this document. Each part has an ID that is used later within the musical data. Since parts may be encoded separately and combined later, identification elements are present at both the score and score-part levels. There must be at least one score-part, combined as desired with part-group elements that indicate braces and brackets. Parts are ordered from top to bottom in a score based on the order in which they appear in the part-list.

    ``Possible children``:    :obj:`~XMLPartGroup`, :obj:`~XMLScorePart`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Group@name=part-group@minOccurs=0@maxOccurs=unbounded
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=part-group@minOccurs=1@maxOccurs=1
           Group@name=score-part@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=score-part@minOccurs=1@maxOccurs=1
           Choice@minOccurs=0@maxOccurs=unbounded
               Group@name=part-group@minOccurs=1@maxOccurs=1
                   Sequence@minOccurs=1@maxOccurs=1
                       Element@name=part-group@minOccurs=1@maxOccurs=1
               Group@name=score-part@minOccurs=1@maxOccurs=1
                   Sequence@minOccurs=1@maxOccurs=1
                       Element@name=score-part@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLScorePartwise`
    """
    
    TYPE = XSDComplexTypePartList
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='part-list'][@type='part-list']"


class XMLPartName(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/part-name/>`_
    
    
    
    ``complexType``: The part-name type describes the name or abbreviation of a score-part element. Formatting attributes for the part-name element are deprecated in Version 2.0 in favor of the new part-name-display and part-abbreviation-display elements.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``justify``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLScorePart`
    """
    
    TYPE = XSDComplexTypePartName
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='part-name'][@type='part-name']"


class XMLPartNameDisplay(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/part-name-display/>`_
    
    
    
    ``complexType``: The name-display type is used for exact formatting of multi-font text in part and group names to the left of the system. The print-object attribute can be used to determine what, if anything, is printed at the start of each system. Enclosure for the display-text element is none by default. Language for the display-text element is Italian ("it") by default.

    ``Possible attributes``: ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

    ``Possible children``:    :obj:`~XMLAccidentalText`, :obj:`~XMLDisplayText`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Choice@minOccurs=0@maxOccurs=unbounded
               Element@name=display-text@minOccurs=1@maxOccurs=1
               Element@name=accidental-text@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLPrint`, :obj:`~XMLScorePart`
    """
    
    TYPE = XSDComplexTypeNameDisplay
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='part-name-display'][@type='name-display']"


class XMLPartSymbol(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/part-symbol/>`_
    
    The part-symbol element indicates how a symbol for a multi-staff part is indicated in the score.
    
    
    
    ``complexType``: The part-symbol type indicates how a symbol for a multi-staff part is indicated in the score; brace is the default value. The top-staff and bottom-staff attributes are used when the brace does not extend across the entire part. For example, in a 3-staff organ part, the top-staff will typically be 1 for the right hand, while the bottom-staff will typically be 2 for the left hand. Staff 3 for the pedals is usually outside the brace. By default, the presence of a part-symbol element that does not extend across the entire part also indicates a corresponding change in the common barlines within a part.
    
    ``simpleContent``: The group-symbol-value type indicates how the symbol for a group or multi-staff part is indicated in the score.
        
        Permitted Values: ``'none'``, ``'brace'``, ``'line'``, ``'bracket'``, ``'square'``
    

    ``Possible attributes``: ``bottom_staff``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffNumber`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``top_staff``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffNumber`

``Possible parents``::obj:`~XMLAttributes`
    """
    
    TYPE = XSDComplexTypePartSymbol
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='part-symbol'][@type='part-symbol']"


class XMLPartTranspose(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/part-transpose/>`_
    
    The chromatic element in a part-transpose element will usually have a non-zero value, since octave transpositions can be represented in concert scores using the transpose element.
    
    
    
    ``complexType``: The child elements of the part-transpose type have the same meaning as for the transpose type. However that meaning applies to a transposed part created from the existing score file.

    ``Possible children``:    :obj:`~XMLChromatic`, :obj:`~XMLDiatonic`, :obj:`~XMLDouble`, :obj:`~XMLOctaveChange`

    ``XSD structure:``

    .. code-block::

       Group@name=transpose@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Element@name=diatonic@minOccurs=0@maxOccurs=1
               Element@name=chromatic@minOccurs=1@maxOccurs=1
               Element@name=octave-change@minOccurs=0@maxOccurs=1
               Element@name=double@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLForPart`
    """
    
    TYPE = XSDComplexTypePartTranspose
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='part-transpose'][@type='part-transpose']"


class XMLPedal(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pedal/>`_
    
    
    
    ``complexType``: The pedal type represents piano pedal marks, including damper and sostenuto pedal marks. The line attribute is yes if pedal lines are used. The sign attribute is yes if Ped, Sost, and * signs are used. For compatibility with older versions, the sign attribute is yes by default if the line attribute is no, and is no by default if the line attribute is yes. If the sign attribute is set to yes and the type is start or sostenuto, the abbreviated attribute is yes if the short P and S signs are used, and no if the full Ped and Sost signs are used. It is no by default. Otherwise the abbreviated attribute is ignored. The alignment attributes are ignored if the sign attribute is no.

    ``Possible attributes``: ``abbreviated``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``line``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``sign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePedalType`\@required, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypePedal
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pedal'][@type='pedal']"


class XMLPedalAlter(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pedal-alter/>`_
    
    The pedal-alter element defines the chromatic alteration for a single harp pedal.
    
    
    
    ``simpleType``: The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.

``Possible parents``::obj:`~XMLPedalTuning`
    """
    
    TYPE = XSDSimpleTypeSemitones
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pedal-alter'][@type='semitones']"


class XMLPedalStep(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pedal-step/>`_
    
    The pedal-step element defines the pitch step for a single harp pedal.
    
    
    
    ``simpleType``: The step type represents a step of the diatonic scale, represented using the English letters A through G.
        
        Permitted Values: ``'A'``, ``'B'``, ``'C'``, ``'D'``, ``'E'``, ``'F'``, ``'G'``
    

``Possible parents``::obj:`~XMLPedalTuning`
    """
    
    TYPE = XSDSimpleTypeStep
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pedal-step'][@type='step']"


class XMLPedalTuning(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pedal-tuning/>`_
    
    
    
    ``complexType``: The pedal-tuning type specifies the tuning of a single harp pedal.

    ``Possible children``:    :obj:`~XMLPedalAlter`, :obj:`~XMLPedalStep`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=pedal-step@minOccurs=1@maxOccurs=1
           Element@name=pedal-alter@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLHarpPedals`
    """
    
    TYPE = XSDComplexTypePedalTuning
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pedal-tuning'][@type='pedal-tuning']"


class XMLPerMinute(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/per-minute/>`_
    
    
    
    ``complexType``: The per-minute type can be a number, or a text description including numbers. If a font is specified, it overrides the font specified for the overall metronome element. This allows separate specification of a music font for the beat-unit and a text font for the numeric value, in cases where a single metronome font is not used.

    ``Possible attributes``: ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`

``Possible parents``::obj:`~XMLMetronome`
    """
    
    TYPE = XSDComplexTypePerMinute
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='per-minute'][@type='per-minute']"


class XMLPercussion(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/percussion/>`_
    
    
    
    ``complexType``: The percussion element is used to define percussion pictogram symbols. Definitions for these symbols can be found in Kurt Stone's "Music Notation in the Twentieth Century" on pages 206-212 and 223. Some values are added to these based on how usage has evolved in the 30 years since Stone's book was published.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``enclosure``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeEnclosureShape`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

    ``Possible children``:    :obj:`~XMLBeater`, :obj:`~XMLEffect`, :obj:`~XMLGlass`, :obj:`~XMLMembrane`, :obj:`~XMLMetal`, :obj:`~XMLOtherPercussion`, :obj:`~XMLPitched`, :obj:`~XMLStickLocation`, :obj:`~XMLStick`, :obj:`~XMLTimpani`, :obj:`~XMLWood`

    ``XSD structure:``

    .. code-block::

       Choice@minOccurs=1@maxOccurs=1
           Element@name=glass@minOccurs=1@maxOccurs=1
           Element@name=metal@minOccurs=1@maxOccurs=1
           Element@name=wood@minOccurs=1@maxOccurs=1
           Element@name=pitched@minOccurs=1@maxOccurs=1
           Element@name=membrane@minOccurs=1@maxOccurs=1
           Element@name=effect@minOccurs=1@maxOccurs=1
           Element@name=timpani@minOccurs=1@maxOccurs=1
           Element@name=beater@minOccurs=1@maxOccurs=1
           Element@name=stick@minOccurs=1@maxOccurs=1
           Element@name=stick-location@minOccurs=1@maxOccurs=1
           Element@name=other-percussion@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypePercussion
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='percussion'][@type='percussion']"


class XMLPf(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pf/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pf'][@type='empty']"


class XMLPitch(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pitch/>`_
    
    
    
    ``complexType``: Pitch is represented as a combination of the step of the diatonic scale, the chromatic alteration, and the octave.

    ``Possible children``:    :obj:`~XMLAlter`, :obj:`~XMLOctave`, :obj:`~XMLStep`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=step@minOccurs=1@maxOccurs=1
           Element@name=alter@minOccurs=0@maxOccurs=1
           Element@name=octave@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypePitch
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pitch'][@type='pitch']"


class XMLPitched(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pitched/>`_
    
    
    
    ``complexType``: The pitched-value type represents pictograms for pitched percussion instruments. The smufl attribute is used to distinguish different SMuFL glyphs for a particular pictogram within the Tuned mallet percussion pictograms range.
    
    ``simpleContent``: The pitched-value type represents pictograms for pitched percussion instruments. The chimes and tubular chimes values distinguish the single-line and double-line versions of the pictogram.
        
        Permitted Values: ``'celesta'``, ``'chimes'``, ``'glockenspiel'``, ``'lithophone'``, ``'mallet'``, ``'marimba'``, ``'steel drums'``, ``'tubaphone'``, ``'tubular chimes'``, ``'vibraphone'``, ``'xylophone'``
    

    ``Possible attributes``: ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflPictogramGlyphName`

``Possible parents``::obj:`~XMLPercussion`
    """
    
    TYPE = XSDComplexTypePitched
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pitched'][@type='pitched']"


class XMLPlay(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/play/>`_
    
    
    
    ``complexType``: The play type specifies playback techniques to be used in conjunction with the instrument-sound element. When used as part of a sound element, it applies to all notes going forward in score order. In multi-instrument parts, the affected instrument should be specified using the id attribute. When used as part of a note element, it applies to the current note only.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF`

    ``Possible children``:    :obj:`~XMLIpa`, :obj:`~XMLMute`, :obj:`~XMLOtherPlay`, :obj:`~XMLSemiPitched`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Choice@minOccurs=0@maxOccurs=unbounded
               Element@name=ipa@minOccurs=1@maxOccurs=1
               Element@name=mute@minOccurs=1@maxOccurs=1
               Element@name=semi-pitched@minOccurs=1@maxOccurs=1
               Element@name=other-play@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLNote`, :obj:`~XMLSound`
    """
    
    TYPE = XSDComplexTypePlay
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='play'][@type='play']"


class XMLPlayer(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/player/>`_
    
    
    
    ``complexType``: The player type allows for multiple players per score-part for use in listening applications. One player may play multiple instruments, while a single instrument may include multiple players in divisi sections.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`\@required

    ``Possible children``:    :obj:`~XMLPlayerName`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=player-name@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLScorePart`
    """
    
    TYPE = XSDComplexTypePlayer
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='player'][@type='player']"


class XMLPlayerName(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/player-name/>`_

The player-name element is typically used within a software application, rather than appearing on the printed page of a score.



``Possible parents``::obj:`~XMLPlayer`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='player-name'][@type='xs:string']"


class XMLPlop(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/plop/>`_
    
    The plop element is an indeterminate slide attached to a single note. The plop appears before the main note and comes from above the main pitch.
    
    
    
    ``complexType``: The empty-line type represents an empty element with line-shape, line-type, line-length, dashed-formatting, print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dash_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``line_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineLength`, ``line_shape``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineShape`, ``line_type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineType`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``space_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyLine
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='plop'][@type='empty-line']"


class XMLPluck(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pluck/>`_
    
    The pluck element is used to specify the plucking fingering on a fretted instrument, where the fingering element refers to the fretting fingering. Typical values are p, i, m, a for pulgar/thumb, indicio/index, medio/middle, and anular/ring fingers.
    
    
    
    ``complexType``: The placement-text type represents a text element with print-style and placement attribute groups.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypePlacementText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pluck'][@type='placement-text']"


class XMLPp(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pp/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pp'][@type='empty']"


class XMLPpp(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/ppp/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='ppp'][@type='empty']"


class XMLPppp(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pppp/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pppp'][@type='empty']"


class XMLPpppp(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/ppppp/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='ppppp'][@type='empty']"


class XMLPppppp(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pppppp/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pppppp'][@type='empty']"


class XMLPreBend(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pre-bend/>`_
    
    The pre-bend element indicates that a bend is a pre-bend rather than a normal bend or a release.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLBend`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pre-bend'][@type='empty']"


class XMLPrefix(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/prefix/>`_
    
    Values for the prefix element include plus and the accidental values sharp, flat, natural, double-sharp, flat-flat, and sharp-sharp. The prefix element may contain additional values for symbols specific to particular figured bass styles.
    
    
    
    ``complexType``: The style-text type represents a text element with a print-style attribute group.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLFigure`
    """
    
    TYPE = XSDComplexTypeStyleText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='prefix'][@type='style-text']"


class XMLPrincipalVoice(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/principal-voice/>`_
    
    
    
    ``complexType``: The principal-voice type represents principal and secondary voices in a score, either for analysis or for square bracket symbols that appear in a score. The element content is used for analysis and may be any text value. The symbol attribute indicates the type of symbol used. When used for analysis separate from any printed score markings, it should be set to none. Otherwise if the type is stop it should be set to plain.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``symbol``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePrincipalVoiceSymbol`\@required, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypePrincipalVoice
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='principal-voice'][@type='principal-voice']"


class XMLPrint(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/print/>`_
    
    
    
    ``complexType``: The print type contains general printing parameters, including layout elements. The part-name-display and part-abbreviation-display elements may also be used here to change how a part name or abbreviation is displayed over the course of a piece. They take effect when the current measure or a succeeding measure starts a new system.
    
    Layout group elements in a print element only apply to the current page, system, or staff. Music that follows continues to take the default values from the layout determined by the defaults element.

    ``Possible attributes``: ``blank_page``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePositiveInteger`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``new_page``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``new_system``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``page_number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``staff_spacing``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

    ``Possible children``:    :obj:`~XMLMeasureLayout`, :obj:`~XMLMeasureNumbering`, :obj:`~XMLPageLayout`, :obj:`~XMLPartAbbreviationDisplay`, :obj:`~XMLPartNameDisplay`, :obj:`~XMLStaffLayout`, :obj:`~XMLSystemLayout`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Group@name=layout@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=page-layout@minOccurs=0@maxOccurs=1
                   Element@name=system-layout@minOccurs=0@maxOccurs=1
                   Element@name=staff-layout@minOccurs=0@maxOccurs=unbounded
           Element@name=measure-layout@minOccurs=0@maxOccurs=1
           Element@name=measure-numbering@minOccurs=0@maxOccurs=1
           Element@name=part-name-display@minOccurs=0@maxOccurs=1
           Element@name=part-abbreviation-display@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypePrint
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='print'][@type='print']"


class XMLPullOff(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pull-off/>`_
    
    
    
    ``complexType``: The hammer-on and pull-off elements are used in guitar and fretted instrument notation. Since a single slur can be marked over many notes, the hammer-on and pull-off elements are separate so the individual pair of notes can be specified. The element content can be used to specify how the hammer-on or pull-off should be notated. An empty element leaves this choice up to the application.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeHammerOnPullOff
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='pull-off'][@type='hammer-on-pull-off']"


class XMLRehearsal(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/rehearsal/>`_
    
    The rehearsal element specifies letters, numbers, and section names that are notated in the score for reference during rehearsal. The enclosure is square if not specified. The language is Italian ("it") if not specified. Left justification is used if not specified.
    
    
    
    ``complexType``: The formatted-text-id type represents a text element with text-formatting and id attributes.

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeFormattedTextId
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='rehearsal'][@type='formatted-text-id']"


class XMLRelation(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/relation/>`_
    
    A related resource for the music that is encoded. This is similar to the Dublin Core relation element. Standard type values are music, words, and arrangement, but other types may be used.
    
    
    
    ``complexType``: The typed-text type represents a text element with a type attribute.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLIdentification`
    """
    
    TYPE = XSDComplexTypeTypedText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='relation'][@type='typed-text']"


class XMLRelease(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/release/>`_
    
    
    
    ``complexType``: The release type indicates that a bend is a release rather than a normal bend or pre-bend. The offset attribute specifies where the release starts in terms of divisions relative to the current note. The first-beat and last-beat attributes of the parent bend element are relative to the original note position, not this offset value.

    ``Possible attributes``: ``offset``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeDivisions`

``Possible parents``::obj:`~XMLBend`
    """
    
    TYPE = XSDComplexTypeRelease
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='release'][@type='release']"


class XMLRepeat(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/repeat/>`_
    
    
    
    ``complexType``: The repeat type represents repeat marks. The start of the repeat has a forward direction while the end of the repeat has a backward direction. The times and after-jump attributes are only used with backward repeats that are not part of an ending. The times attribute indicates the number of times the repeated section is played. The after-jump attribute indicates if the repeats are played after a jump due to a da capo or dal segno.

    ``Possible attributes``: ``after_jump``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``direction``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeBackwardForward`\@required, ``times``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNonNegativeInteger`, ``winged``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeWinged`

``Possible parents``::obj:`~XMLBarline`
    """
    
    TYPE = XSDComplexTypeRepeat
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='repeat'][@type='repeat']"


class XMLRest(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/rest/>`_
    
    
    
    ``complexType``: The rest element indicates notated rests or silences. Rest elements are usually empty, but placement on the staff can be specified using display-step and display-octave elements. If the measure attribute is set to yes, this indicates this is a complete measure rest.

    ``Possible attributes``: ``measure``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

    ``Possible children``:    :obj:`~XMLDisplayOctave`, :obj:`~XMLDisplayStep`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Group@name=display-step-octave@minOccurs=0@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=display-step@minOccurs=1@maxOccurs=1
                   Element@name=display-octave@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeRest
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='rest'][@type='rest']"


class XMLRf(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/rf/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='rf'][@type='empty']"


class XMLRfz(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/rfz/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='rfz'][@type='empty']"


class XMLRightDivider(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/right-divider/>`_
    
    
    
    ``complexType``: The empty-print-style-align-object type represents an empty element with print-object and print-style-align attribute groups.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLSystemDividers`
    """
    
    TYPE = XSDComplexTypeEmptyPrintObjectStyleAlign
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='right-divider'][@type='empty-print-object-style-align']"


class XMLRightMargin(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/right-margin/>`_
    
    
    
    ``simpleType``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

``Possible parents``::obj:`~XMLPageMargins`, :obj:`~XMLSystemMargins`
    """
    
    TYPE = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='right-margin'][@type='tenths']"


class XMLRights(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/rights/>`_
    
    The rights element is borrowed from Dublin Core. It contains copyright and other intellectual property notices. Words, music, and derivatives can have different types, so multiple rights elements with different type attributes are supported. Standard type values are music, words, and arrangement, but other types may be used. The type attribute is only needed when there are multiple rights elements.
    
    
    
    ``complexType``: The typed-text type represents a text element with a type attribute.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLIdentification`
    """
    
    TYPE = XSDComplexTypeTypedText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='rights'][@type='typed-text']"


class XMLRoot(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/root/>`_
    
    
    
    ``complexType``: The root type indicates a pitch like C, D, E vs. a scale degree like 1, 2, 3. It is used with chord symbols in popular music. The root element has a root-step and optional root-alter element similar to the step and alter elements, but renamed to distinguish the different musical meanings.

    ``Possible children``:    :obj:`~XMLRootAlter`, :obj:`~XMLRootStep`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=root-step@minOccurs=1@maxOccurs=1
           Element@name=root-alter@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLHarmony`
    """
    
    TYPE = XSDComplexTypeRoot
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='root'][@type='root']"


class XMLRootAlter(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/root-alter/>`_
    
    The root-alter element represents the chromatic alteration of the root of the current chord within the harmony element. In some chord styles, the text for the root-step element may include root-alter information. In that case, the print-object attribute of the root-alter element can be set to no. The location attribute indicates whether the alteration should appear to the left or the right of the root-step; it is right by default.
    
    
    
    ``complexType``: The harmony-alter type represents the chromatic alteration of the root, numeral, or bass of the current harmony-chord group within the harmony element. In some chord styles, the text of the preceding element may include alteration information. In that case, the print-object attribute of this type can be set to no. The location attribute indicates whether the alteration should appear to the left or the right of the preceding element. Its default value varies by element.
    
    ``simpleContent``: The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``location``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftRight`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLRoot`
    """
    
    TYPE = XSDComplexTypeHarmonyAlter
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='root-alter'][@type='harmony-alter']"


class XMLRootStep(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/root-step/>`_
    
    
    
    ``complexType``: The root-step type represents the pitch step of the root of the current chord within the harmony element. The text attribute indicates how the root should appear in a score if not using the element contents.
    
    ``simpleContent``: The step type represents a step of the diatonic scale, represented using the English letters A through G.
        
        Permitted Values: ``'A'``, ``'B'``, ``'C'``, ``'D'``, ``'E'``, ``'F'``, ``'G'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``text``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLRoot`
    """
    
    TYPE = XSDComplexTypeRootStep
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='root-step'][@type='root-step']"


class XMLScaling(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/scaling/>`_
    
    
    
    ``complexType``: Margins, page sizes, and distances are all measured in tenths to keep MusicXML data in a consistent coordinate system as much as possible. The translation to absolute units is done with the scaling type, which specifies how many millimeters are equal to how many tenths. For a staff height of 7 mm, millimeters would be set to 7 while tenths is set to 40. The ability to set a formula rather than a single scaling factor helps avoid roundoff errors.

    ``Possible children``:    :obj:`~XMLMillimeters`, :obj:`~XMLTenths`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=millimeters@minOccurs=1@maxOccurs=1
           Element@name=tenths@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLDefaults`
    """
    
    TYPE = XSDComplexTypeScaling
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='scaling'][@type='scaling']"


class XMLSchleifer(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/schleifer/>`_
    
    The name for this ornament is based on the German, to avoid confusion with the more common slide element defined earlier.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='schleifer'][@type='empty-placement']"


class XMLScoop(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/scoop/>`_
    
    The scoop element is an indeterminate slide attached to a single note. The scoop appears before the main note and comes from below the main pitch.
    
    
    
    ``complexType``: The empty-line type represents an empty element with line-shape, line-type, line-length, dashed-formatting, print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dash_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``line_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineLength`, ``line_shape``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineShape`, ``line_type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineType`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``space_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyLine
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='scoop'][@type='empty-line']"


class XMLScordatura(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/scordatura/>`_
    
    
    
    ``complexType``: Scordatura string tunings are represented by a series of accord elements, similar to the staff-tuning elements. Strings are numbered from high to low.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`

    ``Possible children``:    :obj:`~XMLAccord`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=accord@minOccurs=1@maxOccurs=unbounded

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeScordatura
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='scordatura'][@type='scordatura']"


class XMLScoreInstrument(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/score-instrument/>`_
    
    
    
    ``complexType``: The score-instrument type represents a single instrument within a score-part. As with the score-part type, each score-instrument has a required ID attribute, a name, and an optional abbreviation.
    
    A score-instrument type is also required if the score specifies MIDI 1.0 channels, banks, or programs. An initial midi-instrument assignment can also be made here. MusicXML software should be able to automatically assign reasonable channels and instruments without these elements in simple cases, such as where part names match General MIDI instrument names.
    
    The score-instrument element can also distinguish multiple instruments of the same type that are on the same part, such as Clarinet 1 and Clarinet 2 instruments within a Clarinets 1 and 2 part.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`\@required

    ``Possible children``:    :obj:`~XMLEnsemble`, :obj:`~XMLInstrumentAbbreviation`, :obj:`~XMLInstrumentName`, :obj:`~XMLInstrumentSound`, :obj:`~XMLSolo`, :obj:`~XMLVirtualInstrument`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=instrument-name@minOccurs=1@maxOccurs=1
           Element@name=instrument-abbreviation@minOccurs=0@maxOccurs=1
           Group@name=virtual-instrument-data@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=instrument-sound@minOccurs=0@maxOccurs=1
                   Choice@minOccurs=0@maxOccurs=1
                       Element@name=solo@minOccurs=1@maxOccurs=1
                       Element@name=ensemble@minOccurs=1@maxOccurs=1
                   Element@name=virtual-instrument@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLScorePart`
    """
    
    TYPE = XSDComplexTypeScoreInstrument
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='score-instrument'][@type='score-instrument']"


class XMLScorePart(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/score-part/>`_
    
    Each MusicXML part corresponds to a track in a Standard MIDI Format 1 file. The score-instrument elements are used when there are multiple instruments per track. The midi-device element is used to make a MIDI device or port assignment for the given track. Initial midi-instrument assignments may be made here as well.
    
    
    
    ``complexType``: The score-part type collects part-wide information for each part in a score. Often, each MusicXML part corresponds to a track in a Standard MIDI Format 1 file. In this case, the midi-device element is used to make a MIDI device or port assignment for the given track or specific MIDI instruments. Initial midi-instrument assignments may be made here as well. The score-instrument elements are used when there are multiple instruments per track.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`\@required

    ``Possible children``:    :obj:`~XMLGroup`, :obj:`~XMLIdentification`, :obj:`~XMLMidiDevice`, :obj:`~XMLMidiInstrument`, :obj:`~XMLPartAbbreviationDisplay`, :obj:`~XMLPartAbbreviation`, :obj:`~XMLPartLink`, :obj:`~XMLPartNameDisplay`, :obj:`~XMLPartName`, :obj:`~XMLPlayer`, :obj:`~XMLScoreInstrument`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=identification@minOccurs=0@maxOccurs=1
           Element@name=part-link@minOccurs=0@maxOccurs=unbounded
           Element@name=part-name@minOccurs=1@maxOccurs=1
           Element@name=part-name-display@minOccurs=0@maxOccurs=1
           Element@name=part-abbreviation@minOccurs=0@maxOccurs=1
           Element@name=part-abbreviation-display@minOccurs=0@maxOccurs=1
           Element@name=group@minOccurs=0@maxOccurs=unbounded
           Element@name=score-instrument@minOccurs=0@maxOccurs=unbounded
           Element@name=player@minOccurs=0@maxOccurs=unbounded
           Sequence@minOccurs=0@maxOccurs=unbounded
               Element@name=midi-device@minOccurs=0@maxOccurs=1
               Element@name=midi-instrument@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLPartList`
    """
    
    TYPE = XSDComplexTypeScorePart
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='score-part'][@type='score-part']"


class XMLScorePartwise(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/score-partwise/>`_

The score-partwise element is the root element for a partwise MusicXML score. It includes a score-header group followed by a series of parts with measures inside. The document-attributes attribute group includes the version attribute.



    ``Possible attributes``: ``version``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

    ``Possible children``:    :obj:`~XMLCredit`, :obj:`~XMLDefaults`, :obj:`~XMLIdentification`, :obj:`~XMLMovementNumber`, :obj:`~XMLMovementTitle`, :obj:`~XMLPartList`, :obj:`~XMLPart`, :obj:`~XMLWork`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Group@name=score-header@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=work@minOccurs=0@maxOccurs=1
                   Element@name=movement-number@minOccurs=0@maxOccurs=1
                   Element@name=movement-title@minOccurs=0@maxOccurs=1
                   Element@name=identification@minOccurs=0@maxOccurs=1
                   Element@name=defaults@minOccurs=0@maxOccurs=1
                   Element@name=credit@minOccurs=0@maxOccurs=unbounded
                   Element@name=part-list@minOccurs=1@maxOccurs=1
           Element@name=part@minOccurs=1@maxOccurs=unbounded
    """
    
    TYPE = XSDComplexTypeScorePartwise
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='score-partwise']"

    def write(self, path: 'pathlib.Path', intelligent_choice: bool=False) -> None:
        """
        :param path: Output xml file path, required.
        :param intelligent_choice: Set to True if you wish to use intelligent choice in final checks to be able to change the attachment 
                                   order of XMLElement children in self.child_container_tree if an Exception was thrown and other choices 
                                   can still be checked. (No GUARANTEE!)
        :return: None
        """
        with open(path, 'w') as file:
            file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
            file.write(self.to_string(intelligent_choice=intelligent_choice))


class XMLSecond(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/second/>`_



``Possible parents``::obj:`~XMLSwing`
    """
    
    TYPE = XSDSimpleTypePositiveInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='second'][@type='xs:positiveInteger']"


class XMLSegno(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/segno/>`_
    
    
    
    ``complexType``: The segno type is the visual indicator of a segno sign. The exact glyph can be specified with the smufl attribute. A sound element is also needed to guide playback applications reliably.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflSegnoGlyphName`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLBarline`, :obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeSegno
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='segno'][@type='segno']"


class XMLSemiPitched(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/semi-pitched/>`_
    
    
    
    ``simpleType``: The semi-pitched type represents categories of indefinite pitch for percussion instruments.
        
        Permitted Values: ``'high'``, ``'medium-high'``, ``'medium'``, ``'medium-low'``, ``'low'``, ``'very-low'``
    

``Possible parents``::obj:`~XMLPlay`
    """
    
    TYPE = XSDSimpleTypeSemiPitched
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='semi-pitched'][@type='semi-pitched']"


class XMLSf(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/sf/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='sf'][@type='empty']"


class XMLSffz(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/sffz/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='sffz'][@type='empty']"


class XMLSfp(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/sfp/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='sfp'][@type='empty']"


class XMLSfpp(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/sfpp/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='sfpp'][@type='empty']"


class XMLSfz(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/sfz/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='sfz'][@type='empty']"


class XMLSfzp(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/sfzp/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLDynamics`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='sfzp'][@type='empty']"


class XMLShake(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/shake/>`_
    
    The shake element has a similar appearance to an inverted-mordent element.
    
    
    
    ``complexType``: The empty-trill-sound type represents an empty element with print-style, placement, and trill-sound attributes.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``second_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``start_note``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartNote`, ``trill_step``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillStep`, ``two_note_turn``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTwoNoteTurn`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeEmptyTrillSound
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='shake'][@type='empty-trill-sound']"


class XMLSign(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/sign/>`_
    
    The sign element represents the clef symbol.
    
    
    
    ``simpleType``: The clef-sign type represents the different clef symbols. The jianpu sign indicates that the music that follows should be in jianpu numbered notation, just as the TAB sign indicates that the music that follows should be in tablature notation. Unlike TAB, a jianpu sign does not correspond to a visual clef notation.
    
    The none sign is deprecated as of MusicXML 4.0. Use the clef element's print-object attribute instead. When the none sign is used, notes should be displayed as if in treble clef.
        
        Permitted Values: ``'G'``, ``'F'``, ``'C'``, ``'percussion'``, ``'TAB'``, ``'jianpu'``, ``'none'``
    

``Possible parents``::obj:`~XMLClef`, :obj:`~XMLPartClef`
    """
    
    TYPE = XSDSimpleTypeClefSign
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='sign'][@type='clef-sign']"


class XMLSlash(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/slash/>`_
    
    
    
    ``complexType``: The slash type is used to indicate that slash notation is to be used. If the slash is on every beat, use-stems is no (the default). To indicate rhythms but not pitches, use-stems is set to yes. The type attribute indicates whether this is the start or stop of a slash notation style. The use-dots attribute works as for the beat-repeat element, and only has effect if use-stems is no.

    ``Possible attributes``: ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required, ``use_dots``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``use_stems``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

    ``Possible children``:    :obj:`~XMLExceptVoice`, :obj:`~XMLSlashDot`, :obj:`~XMLSlashType`

    ``XSD structure:``

    .. code-block::

       Group@name=slash@minOccurs=0@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=0@maxOccurs=1
                   Element@name=slash-type@minOccurs=1@maxOccurs=1
                   Element@name=slash-dot@minOccurs=0@maxOccurs=unbounded
               Element@name=except-voice@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLMeasureStyle`
    """
    
    TYPE = XSDComplexTypeSlash
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='slash'][@type='slash']"


class XMLSlashDot(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/slash-dot/>`_
    
    The slash-dot element is used to specify any augmentation dots in the note type used to display repetition marks.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLBeatRepeat`, :obj:`~XMLSlash`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='slash-dot'][@type='empty']"


class XMLSlashType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/slash-type/>`_
    
    The slash-type element indicates the graphical note type to use for the display of repetition marks.
    
    
    
    ``simpleType``: The note-type-value type is used for the MusicXML type element and represents the graphic note type, from 1024th (shortest) to maxima (longest).
        
        Permitted Values: ``'1024th'``, ``'512th'``, ``'256th'``, ``'128th'``, ``'64th'``, ``'32nd'``, ``'16th'``, ``'eighth'``, ``'quarter'``, ``'half'``, ``'whole'``, ``'breve'``, ``'long'``, ``'maxima'``
    

``Possible parents``::obj:`~XMLBeatRepeat`, :obj:`~XMLSlash`
    """
    
    TYPE = XSDSimpleTypeNoteTypeValue
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='slash-type'][@type='note-type-value']"


class XMLSlide(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/slide/>`_
    
    
    
    ``complexType``: Glissando and slide types both indicate rapidly moving from one pitch to the other so that individual notes are not discerned. A slide is continuous between the two pitches and defaults to a solid line. The optional text for a is printed alongside the line.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dash_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``first_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``line_type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineType`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``space_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required

``Possible parents``::obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeSlide
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='slide'][@type='slide']"


class XMLSlur(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/slur/>`_
    
    
    
    ``complexType``: Slur types are empty. Most slurs are represented with two elements: one with a start type, and one with a stop type. Slurs can add more elements using a continue type. This is typically used to specify the formatting of cross-system slurs, or to specify the shape of very complex slurs.

    ``Possible attributes``: ``bezier_offset2``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeDivisions`, ``bezier_offset``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeDivisions`, ``bezier_x2``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``bezier_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``bezier_y2``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``bezier_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dash_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``line_type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineType`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``orientation``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeOverUnder`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``space_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStopContinue`\@required

``Possible parents``::obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeSlur
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='slur'][@type='slur']"


class XMLSmear(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/smear/>`_
    
    The smear element represents the tilde-shaped smear symbol used in brass notation.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='smear'][@type='empty-placement']"


class XMLSnapPizzicato(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/snap-pizzicato/>`_
    
    The snap-pizzicato element represents the snap pizzicato symbol. This is a circle with a line, where the line comes inside the circle. It is distinct from the thumb-position symbol, where the line does not come inside the circle.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='snap-pizzicato'][@type='empty-placement']"


class XMLSoftAccent(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/soft-accent/>`_
    
    The soft-accent element indicates a soft accent that is not as heavy as a normal accent. It is often notated as <>. It can be combined with other articulations to implement the first eight symbols in the SMuFL Articulation supplement range.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='soft-accent'][@type='empty-placement']"


class XMLSoftware(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/software/>`_



``Possible parents``::obj:`~XMLEncoding`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='software'][@type='xs:string']"


class XMLSolo(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/solo/>`_
    
    The solo element is present if performance is intended by a solo instrument.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLInstrumentChange`, :obj:`~XMLScoreInstrument`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='solo'][@type='empty']"


class XMLSound(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/sound/>`_
    
    
    
    ``complexType``: The sound element contains general playback parameters. They can stand alone within a part/measure, or be a component element within a direction.
    
    Tempo is expressed in quarter notes per minute. If 0, the sound-generating program should prompt the user at the time of compiling a sound (MIDI) file.
    
    Dynamics (or MIDI velocity) are expressed as a percentage of the default forte value (90 for MIDI 1.0).
    
    Dacapo indicates to go back to the beginning of the movement. When used it always has the value "yes".
    
    Segno and dalsegno are used for backwards jumps to a segno sign; coda and tocoda are used for forward jumps to a coda sign. If there are multiple jumps, the value of these parameters can be used to name and distinguish them. If segno or coda is used, the divisions attribute can also be used to indicate the number of divisions per quarter note. Otherwise sound and MIDI generating programs may have to recompute this.
    
    By default, a dalsegno or dacapo attribute indicates that the jump should occur the first time through, while a tocoda attribute indicates the jump should occur the second time through. The time that jumps occur can be changed by using the time-only attribute.
    
    The forward-repeat attribute indicates that a forward repeat sign is implied but not displayed. It is used for example in two-part forms with repeats, such as a minuet and trio where no repeat is displayed at the start of the trio. This usually occurs after a barline. When used it always has the value of "yes".
    
    The fine attribute follows the final note or rest in a movement with a da capo or dal segno direction. If numeric, the value represents the actual duration of the final note or rest, which can be ambiguous in written notation and different among parts and voices. The value may also be "yes" to indicate no change to the final duration.
    
    If the sound element applies only particular times through a repeat, the time-only attribute indicates which times to apply the sound element.
    
    Pizzicato in a sound element effects all following notes. Yes indicates pizzicato, no indicates arco.
    
    The pan and elevation attributes are deprecated in Version 2.0. The pan and elevation elements in the midi-instrument element should be used instead. The meaning of the pan and elevation attributes is the same as for the pan and elevation elements. If both are present, the mid-instrument elements take priority.
    
    The damper-pedal, soft-pedal, and sostenuto-pedal attributes effect playback of the three common piano pedals and their MIDI controller equivalents. The yes value indicates the pedal is depressed; no indicates the pedal is released. A numeric value from 0 to 100 may also be used for half pedaling. This value is the percentage that the pedal is depressed. A value of 0 is equivalent to no, and a value of 100 is equivalent to yes.
    
    Instrument changes, MIDI devices, MIDI instruments, and playback techniques are changed using the instrument-change, midi-device, midi-instrument, and play elements. When there are multiple instances of these elements, they should be grouped together by instrument using the id attribute values.
    
    The offset element is used to indicate that the sound takes place offset from the current score position. If the sound element is a child of a direction element, the sound offset element overrides the direction offset element if both elements are present. Note that the offset reflects the intended musical position for the change in sound. It should not be used to compensate for latency issues in particular hardware configurations.

    ``Possible attributes``: ``coda``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``dacapo``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``dalsegno``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``damper_pedal``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNoNumber`, ``divisions``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeDivisions`, ``dynamics``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNonNegativeDecimal`, ``elevation``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeRotationDegrees`, ``fine``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``forward_repeat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``pan``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeRotationDegrees`, ``pizzicato``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``segno``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`, ``soft_pedal``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNoNumber`, ``sostenuto_pedal``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNoNumber`, ``tempo``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNonNegativeDecimal`, ``time_only``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeOnly`, ``tocoda``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

    ``Possible children``:    :obj:`~XMLInstrumentChange`, :obj:`~XMLMidiDevice`, :obj:`~XMLMidiInstrument`, :obj:`~XMLOffset`, :obj:`~XMLPlay`, :obj:`~XMLSwing`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=0@maxOccurs=unbounded
               Element@name=instrument-change@minOccurs=0@maxOccurs=1
               Element@name=midi-device@minOccurs=0@maxOccurs=1
               Element@name=midi-instrument@minOccurs=0@maxOccurs=1
               Element@name=play@minOccurs=0@maxOccurs=1
           Element@name=swing@minOccurs=0@maxOccurs=1
           Element@name=offset@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLDirection`, :obj:`~XMLMeasure`
    """
    
    TYPE = XSDComplexTypeSound
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='sound'][@type='sound']"


class XMLSoundingPitch(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/sounding-pitch/>`_
    
    The sounding-pitch is the pitch which is heard when playing the harmonic.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLHarmonic`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='sounding-pitch'][@type='empty']"


class XMLSource(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/source/>`_

The source for the music that is encoded. This is similar to the Dublin Core source element.



``Possible parents``::obj:`~XMLIdentification`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='source'][@type='xs:string']"


class XMLSpiccato(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/spiccato/>`_
    
    The spiccato element is used for a stroke articulation, as opposed to a dot or a wedge.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='spiccato'][@type='empty-placement']"


class XMLStaccatissimo(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staccatissimo/>`_
    
    The staccatissimo element is used for a wedge articulation, as opposed to a dot or a stroke.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='staccatissimo'][@type='empty-placement']"


class XMLStaccato(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staccato/>`_
    
    The staccato element is used for a dot articulation, as opposed to a stroke or a wedge.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='staccato'][@type='empty-placement']"


class XMLStaff(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staff/>`_

Staff assignment is only needed for music notated on multiple staves. Used by both notes and directions. Staff values are numbers, with 1 referring to the top-most staff in a part.



``Possible parents``::obj:`~XMLDirection`, :obj:`~XMLForward`, :obj:`~XMLHarmony`, :obj:`~XMLNote`
    """
    
    TYPE = XSDSimpleTypePositiveInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='staff'][@type='xs:positiveInteger']"


class XMLStaffDetails(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staff-details/>`_
    
    The staff-details element is used to indicate different types of staves.
    
    
    
    ``complexType``: The staff-details element is used to indicate different types of staves. The optional number attribute specifies the staff number from top to bottom on the system, as with clef. The print-object attribute is used to indicate when a staff is not printed in a part, usually in large scores where empty parts are omitted. It is yes by default. If print-spacing is yes while print-object is no, the score is printed in cutaway format where vertical space is left for the empty part.

    ``Possible attributes``: ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffNumber`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``print_spacing``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``show_frets``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeShowFrets`

    ``Possible children``:    :obj:`~XMLCapo`, :obj:`~XMLLineDetail`, :obj:`~XMLStaffLines`, :obj:`~XMLStaffSize`, :obj:`~XMLStaffTuning`, :obj:`~XMLStaffType`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=staff-type@minOccurs=0@maxOccurs=1
           Sequence@minOccurs=0@maxOccurs=1
               Element@name=staff-lines@minOccurs=1@maxOccurs=1
               Element@name=line-detail@minOccurs=0@maxOccurs=unbounded
           Element@name=staff-tuning@minOccurs=0@maxOccurs=unbounded
           Element@name=capo@minOccurs=0@maxOccurs=1
           Element@name=staff-size@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLAttributes`
    """
    
    TYPE = XSDComplexTypeStaffDetails
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='staff-details'][@type='staff-details']"


class XMLStaffDistance(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staff-distance/>`_
    
    
    
    ``simpleType``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

``Possible parents``::obj:`~XMLStaffLayout`
    """
    
    TYPE = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='staff-distance'][@type='tenths']"


class XMLStaffDivide(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staff-divide/>`_
    
    
    
    ``complexType``: The staff-divide element represents the staff division arrow symbols found at SMuFL code points U+E00B, U+E00C, and U+E00D.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffDivideSymbol`\@required, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeStaffDivide
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='staff-divide'][@type='staff-divide']"


class XMLStaffLayout(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staff-layout/>`_
    
    
    
    ``complexType``: Staff layout includes the vertical distance from the bottom line of the previous staff in this system to the top line of the staff specified by the number attribute. The optional number attribute refers to staff numbers within the part, from top to bottom on the system. A value of 1 is used if not present.
    
    When used in the defaults element, the values apply to all systems in all parts. When used in the print element, the values apply to the current system only. This value is ignored for the first staff in a system.

    ``Possible attributes``: ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffNumber`

    ``Possible children``:    :obj:`~XMLStaffDistance`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=staff-distance@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLDefaults`, :obj:`~XMLPrint`
    """
    
    TYPE = XSDComplexTypeStaffLayout
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='staff-layout'][@type='staff-layout']"


class XMLStaffLines(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staff-lines/>`_

The staff-lines element specifies the number of lines and is usually used for a non 5-line staff. If the staff-lines element is present, the appearance of each line may be individually specified with a line-detail element.



``Possible parents``::obj:`~XMLStaffDetails`
    """
    
    TYPE = XSDSimpleTypeNonNegativeInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='staff-lines'][@type='xs:nonNegativeInteger']"


class XMLStaffSize(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staff-size/>`_
    
    
    
    ``complexType``: The staff-size element indicates how large a staff space is on this staff, expressed as a percentage of the work's default scaling. Values less than 100 make the staff space smaller while values over 100 make the staff space larger. A staff-type of cue, ossia, or editorial implies a staff-size of less than 100, but the exact value is implementation-dependent unless specified here. Staff size affects staff height only, not the relationship of the staff to the left and right margins.
    
    In some cases, a staff-size different than 100 also scales the notation on the staff, such as with a cue staff. In other cases, such as percussion staves, the lines may be more widely spaced without scaling the notation on the staff. The scaling attribute allows these two cases to be distinguished. It specifies the percentage scaling that applies to the notation. Values less that 100 make the notation smaller while values over 100 make the notation larger. The staff-size content and scaling attribute are both non-negative decimal values.
    
    ``simpleContent``: The non-negative-decimal type specifies a non-negative decimal value.

    ``Possible attributes``: ``scaling``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNonNegativeDecimal`

``Possible parents``::obj:`~XMLStaffDetails`
    """
    
    TYPE = XSDComplexTypeStaffSize
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='staff-size'][@type='staff-size']"


class XMLStaffTuning(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staff-tuning/>`_
    
    
    
    ``complexType``: The staff-tuning type specifies the open, non-capo tuning of the lines on a tablature staff.

    ``Possible attributes``: ``line``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffLine`\@required

    ``Possible children``:    :obj:`~XMLTuningAlter`, :obj:`~XMLTuningOctave`, :obj:`~XMLTuningStep`

    ``XSD structure:``

    .. code-block::

       Group@name=tuning@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Element@name=tuning-step@minOccurs=1@maxOccurs=1
               Element@name=tuning-alter@minOccurs=0@maxOccurs=1
               Element@name=tuning-octave@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLStaffDetails`
    """
    
    TYPE = XSDComplexTypeStaffTuning
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='staff-tuning'][@type='staff-tuning']"


class XMLStaffType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staff-type/>`_
    
    
    
    ``simpleType``: The staff-type value can be ossia, editorial, cue, alternate, or regular. An ossia staff represents music that can be played instead of what appears on the regular staff. An editorial staff also represents musical alternatives, but is created by an editor rather than the composer. It can be used for suggested interpretations or alternatives from other sources. A cue staff represents music from another part. An alternate staff shares the same music as the prior staff, but displayed differently (e.g., treble and bass clef, standard notation and tablature). It is not included in playback. An alternate staff provides more information to an application reading a file than encoding the same music in separate parts, so its use is preferred in this situation if feasible. A regular staff is the standard default staff-type.
        
        Permitted Values: ``'ossia'``, ``'editorial'``, ``'cue'``, ``'alternate'``, ``'regular'``
    

``Possible parents``::obj:`~XMLStaffDetails`
    """
    
    TYPE = XSDSimpleTypeStaffType
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='staff-type'][@type='staff-type']"


class XMLStaves(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staves/>`_

The staves element is used if there is more than one staff represented in the given part (e.g., 2 staves for typical piano parts). If absent, a value of 1 is assumed. Staves are ordered from top to bottom in a part in numerical order, with staff 1 above staff 2.



``Possible parents``::obj:`~XMLAttributes`
    """
    
    TYPE = XSDSimpleTypeNonNegativeInteger
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='staves'][@type='xs:nonNegativeInteger']"


class XMLStem(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/stem/>`_
    
    
    
    ``complexType``: Stems can be down, up, none, or double. For down and up stems, the position attributes can be used to specify stem length. The relative values specify the end of the stem relative to the program default. Default values specify an absolute end stem position. Negative values of relative-y that would flip a stem instead of shortening it are ignored. A stem element associated with a rest refers to a stemlet.
    
    ``simpleContent``: The stem-value type represents the notated stem direction.
        
        Permitted Values: ``'down'``, ``'up'``, ``'double'``, ``'none'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeStem
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='stem'][@type='stem']"


class XMLStep(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/step/>`_
    
    
    
    ``simpleType``: The step type represents a step of the diatonic scale, represented using the English letters A through G.
        
        Permitted Values: ``'A'``, ``'B'``, ``'C'``, ``'D'``, ``'E'``, ``'F'``, ``'G'``
    

``Possible parents``::obj:`~XMLPitch`
    """
    
    TYPE = XSDSimpleTypeStep
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='step'][@type='step']"


class XMLStick(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/stick/>`_
    
    
    
    ``complexType``: The stick type represents pictograms where the material of the stick, mallet, or beater is included.The parentheses and dashed-circle attributes indicate the presence of these marks around the round beater part of a pictogram. Values for these attributes are "no" if not present.

    ``Possible attributes``: ``dashed_circle``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``parentheses``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``tip``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTipDirection`

    ``Possible children``:    :obj:`~XMLStickMaterial`, :obj:`~XMLStickType`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=stick-type@minOccurs=1@maxOccurs=1
           Element@name=stick-material@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLPercussion`
    """
    
    TYPE = XSDComplexTypeStick
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='stick'][@type='stick']"


class XMLStickLocation(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/stick-location/>`_
    
    
    
    ``simpleType``: The stick-location type represents pictograms for the location of sticks, beaters, or mallets on cymbals, gongs, drums, and other instruments.
        
        Permitted Values: ``'center'``, ``'rim'``, ``'cymbal bell'``, ``'cymbal edge'``
    

``Possible parents``::obj:`~XMLPercussion`
    """
    
    TYPE = XSDSimpleTypeStickLocation
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='stick-location'][@type='stick-location']"


class XMLStickMaterial(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/stick-material/>`_
    
    
    
    ``simpleType``: The stick-material type represents the material being displayed in a stick pictogram.
        
        Permitted Values: ``'soft'``, ``'medium'``, ``'hard'``, ``'shaded'``, ``'x'``
    

``Possible parents``::obj:`~XMLStick`
    """
    
    TYPE = XSDSimpleTypeStickMaterial
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='stick-material'][@type='stick-material']"


class XMLStickType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/stick-type/>`_
    
    
    
    ``simpleType``: The stick-type type represents the shape of pictograms where the material in the stick, mallet, or beater is represented in the pictogram.
        
        Permitted Values: ``'bass drum'``, ``'double bass drum'``, ``'glockenspiel'``, ``'gum'``, ``'hammer'``, ``'superball'``, ``'timpani'``, ``'wound'``, ``'xylophone'``, ``'yarn'``
    

``Possible parents``::obj:`~XMLStick`
    """
    
    TYPE = XSDSimpleTypeStickType
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='stick-type'][@type='stick-type']"


class XMLStopped(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/stopped/>`_
    
    The stopped element represents the stopped symbol, which looks like a plus sign. The smufl attribute distinguishes different SMuFL glyphs that have a similar appearance such as handbellsMalletBellSuspended and guitarClosePedal. If not present, the default glyph is brassMuteClosed.
    
    
    
    ``complexType``: The empty-placement-smufl type represents an empty element with print-style, placement, and smufl attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacementSmufl
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='stopped'][@type='empty-placement-smufl']"


class XMLStraight(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/straight/>`_
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLSwing`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='straight'][@type='empty']"


class XMLStress(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/stress/>`_
    
    The stress element indicates a stressed note.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='stress'][@type='empty-placement']"


class XMLString(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/string/>`_
    
    
    
    ``complexType``: The string type is used with tablature notation, regular notation (where it is often circled), and chord diagrams. String numbers start with 1 for the highest pitched full-length string.
    
    ``simpleContent``: The string-number type indicates a string number. Strings are numbered from high to low, with 1 being the highest pitched full-length string.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLFrameNote`, :obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='string'][@type='string']"


class XMLStringMute(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/string-mute/>`_
    
    
    
    ``complexType``: The string-mute type represents string mute on and mute off symbols.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeOnOff`\@required, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeStringMute
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='string-mute'][@type='string-mute']"


class XMLStrongAccent(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/strong-accent/>`_
    
    The strong-accent element indicates a vertical accent mark.
    
    
    
    ``complexType``: The strong-accent type indicates a vertical accent mark. The type attribute indicates if the point of the accent is down or up.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeUpDown`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeStrongAccent
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='strong-accent'][@type='strong-accent']"


class XMLSuffix(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/suffix/>`_
    
    Values for the suffix element include plus and the accidental values sharp, flat, natural, double-sharp, flat-flat, and sharp-sharp. Suffixes include both symbols that come after the figure number and those that overstrike the figure number. The suffix values slash, back-slash, and vertical are used for slashed numbers indicating chromatic alteration. The orientation and display of the slash usually depends on the figure number. The suffix element may contain additional values for symbols specific to particular figured bass styles.
    
    
    
    ``complexType``: The style-text type represents a text element with a print-style attribute group.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLFigure`
    """
    
    TYPE = XSDComplexTypeStyleText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='suffix'][@type='style-text']"


class XMLSupports(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/supports/>`_
    
    
    
    ``complexType``: The supports type indicates if a MusicXML encoding supports a particular MusicXML element. This is recommended for elements like beam, stem, and accidental, where the absence of an element is ambiguous if you do not know if the encoding supports that element. For Version 2.0, the supports element is expanded to allow programs to indicate support for particular attributes or particular values. This lets applications communicate, for example, that all system and/or page breaks are contained in the MusicXML file.

    ``Possible attributes``: ``attribute``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNMTOKEN`, ``element``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNMTOKEN`\@required, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`\@required, ``value``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeToken`

``Possible parents``::obj:`~XMLEncoding`
    """
    
    TYPE = XSDComplexTypeSupports
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='supports'][@type='supports']"


class XMLSwing(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/swing/>`_
    
    
    
    ``complexType``: The swing element specifies whether or not to use swing playback, where consecutive on-beat / off-beat eighth or 16th notes are played with unequal nominal durations. 
    
    The straight element specifies that no swing is present, so consecutive notes have equal durations.
    
    The first and second elements are positive integers that specify the ratio between durations of consecutive notes. For example, a first element with a value of 2 and a second element with a value of 1 applied to eighth notes specifies a quarter note / eighth note tuplet playback, where the first note is twice as long as the second note. Ratios should be specified with the smallest integers possible. For example, a ratio of 6 to 4 should be specified as 3 to 2 instead.
    
    The optional swing-type element specifies the note type, either eighth or 16th, to which the ratio is applied. The value is eighth if this element is not present.
    
    The optional swing-style element is a string describing the style of swing used.
    
    The swing element has no effect for playback of grace notes, notes where a type element is not present, and notes where the specified duration is different than the nominal value associated with the specified type. If a swung note has attack and release attributes, those values modify the swung playback.

    ``Possible children``:    :obj:`~XMLFirst`, :obj:`~XMLSecond`, :obj:`~XMLStraight`, :obj:`~XMLSwingStyle`, :obj:`~XMLSwingType`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Choice@minOccurs=1@maxOccurs=1
               Element@name=straight@minOccurs=1@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=first@minOccurs=1@maxOccurs=1
                   Element@name=second@minOccurs=1@maxOccurs=1
                   Element@name=swing-type@minOccurs=0@maxOccurs=1
           Element@name=swing-style@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLSound`
    """
    
    TYPE = XSDComplexTypeSwing
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='swing'][@type='swing']"


class XMLSwingStyle(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/swing-style/>`_



``Possible parents``::obj:`~XMLSwing`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='swing-style'][@type='xs:string']"


class XMLSwingType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/swing-type/>`_
    
    
    
    ``simpleType``: The swing-type-value type specifies the note type, either eighth or 16th, to which the ratio defined in the swing element is applied.
        
        Permitted Values: ``'16th'``, ``'eighth'``
    

``Possible parents``::obj:`~XMLSwing`
    """
    
    TYPE = XSDSimpleTypeSwingTypeValue
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='swing-type'][@type='swing-type-value']"


class XMLSyllabic(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/syllabic/>`_
    
    
    
    ``simpleType``: Lyric hyphenation is indicated by the syllabic type. The single, begin, end, and middle values represent single-syllable words, word-beginning syllables, word-ending syllables, and mid-word syllables, respectively.
        
        Permitted Values: ``'single'``, ``'begin'``, ``'end'``, ``'middle'``
    

``Possible parents``::obj:`~XMLLyric`
    """
    
    TYPE = XSDSimpleTypeSyllabic
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='syllabic'][@type='syllabic']"


class XMLSymbol(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/symbol/>`_
    
    The symbol element specifies a musical symbol using a canonical SMuFL glyph name. It is used when an occasional musical symbol is interspersed into text. It should not be used in place of semantic markup, such as metronome marks that mix text and symbols. Left justification is used if not specified. Enclosure is none if not specified.
    
    
    
    ``complexType``: The formatted-symbol-id type represents a SMuFL musical symbol element with formatting and id attributes.
    
    ``simpleContent``: The smufl-glyph-name type is used for attributes that reference a specific Standard Music Font Layout (SMuFL) character. The value is a SMuFL canonical glyph name, not a code point. For instance, the value for a standard piano pedal mark would be keyboardPedalPed, not U+E650.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``dir``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTextDirection`, ``enclosure``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeEnclosureShape`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``justify``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``letter_spacing``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOrNormal`, ``line_height``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOrNormal`, ``line_through``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOfLines`, ``overline``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOfLines`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``rotation``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeRotationDegrees`, ``underline``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOfLines`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeFormattedSymbolId
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='symbol'][@type='formatted-symbol-id']"


class XMLSync(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/sync/>`_
    
    
    
    ``complexType``: The sync type specifies the style that a score following application should use the synchronize an accompaniment with a performer. If this type is not included in a score, default synchronization depends on the application.
    
    The optional latency attribute specifies a time in milliseconds that the listening application should expect from the performer. The optional player and time-only attributes restrict the element to apply to a single player or set of times through a repeated section, respectively.

    ``Possible attributes``: ``latency``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeMilliseconds`, ``player``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF`, ``time_only``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeOnly`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSyncType`\@required

``Possible parents``::obj:`~XMLListening`
    """
    
    TYPE = XSDComplexTypeSync
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='sync'][@type='sync']"


class XMLSystemDistance(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/system-distance/>`_
    
    
    
    ``simpleType``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

``Possible parents``::obj:`~XMLSystemLayout`
    """
    
    TYPE = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='system-distance'][@type='tenths']"


class XMLSystemDividers(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/system-dividers/>`_
    
    
    
    ``complexType``: The system-dividers element indicates the presence or absence of system dividers (also known as system separation marks) between systems displayed on the same page. Dividers on the left and right side of the page are controlled by the left-divider and right-divider elements respectively. The default vertical position is half the system-distance value from the top of the system that is below the divider. The default horizontal position is the left and right system margin, respectively.
    
    When used in the print element, the system-dividers element affects the dividers that would appear between the current system and the previous system.

    ``Possible children``:    :obj:`~XMLLeftDivider`, :obj:`~XMLRightDivider`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=left-divider@minOccurs=1@maxOccurs=1
           Element@name=right-divider@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLSystemLayout`
    """
    
    TYPE = XSDComplexTypeSystemDividers
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='system-dividers'][@type='system-dividers']"


class XMLSystemLayout(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/system-layout/>`_
    
    
    
    ``complexType``: A system is a group of staves that are read and played simultaneously. System layout includes left and right margins and the vertical distance from the previous system. The system distance is measured from the bottom line of the previous system to the top line of the current system. It is ignored for the first system on a page. The top system distance is measured from the page's top margin to the top line of the first system. It is ignored for all but the first system on a page.
    
    Sometimes the sum of measure widths in a system may not equal the system width specified by the layout elements due to roundoff or other errors. The behavior when reading MusicXML files in these cases is application-dependent. For instance, applications may find that the system layout data is more reliable than the sum of the measure widths, and adjust the measure widths accordingly.
    
    When used in the defaults element, the system-layout element defines a default appearance for all systems in the score. If no system-layout element is present in the defaults element, default system layout values are chosen by the application.
    
    When used in the print element, the system-layout element affects the appearance of the current system only. All other systems use the default values as determined by the defaults element. If any child elements are missing from the system-layout element in a print element, the values determined by the defaults element are used there as well. This type of system-layout element need only be read from or written to the first visible part in the score.

    ``Possible children``:    :obj:`~XMLSystemDistance`, :obj:`~XMLSystemDividers`, :obj:`~XMLSystemMargins`, :obj:`~XMLTopSystemDistance`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=system-margins@minOccurs=0@maxOccurs=1
           Element@name=system-distance@minOccurs=0@maxOccurs=1
           Element@name=top-system-distance@minOccurs=0@maxOccurs=1
           Element@name=system-dividers@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLDefaults`, :obj:`~XMLPrint`
    """
    
    TYPE = XSDComplexTypeSystemLayout
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='system-layout'][@type='system-layout']"


class XMLSystemMargins(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/system-margins/>`_
    
    
    
    ``complexType``: System margins are relative to the page margins. Positive values indent and negative values reduce the margin size.

    ``Possible children``:    :obj:`~XMLLeftMargin`, :obj:`~XMLRightMargin`

    ``XSD structure:``

    .. code-block::

       Group@name=left-right-margins@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Element@name=left-margin@minOccurs=1@maxOccurs=1
               Element@name=right-margin@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLSystemLayout`
    """
    
    TYPE = XSDComplexTypeSystemMargins
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='system-margins'][@type='system-margins']"


class XMLTap(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tap/>`_
    
    
    
    ``complexType``: The tap type indicates a tap on the fretboard. The text content allows specification of the notation; + and T are common choices. If the element is empty, the hand attribute is used to specify the symbol to use. The hand attribute is ignored if the tap glyph is already specified by the text content. If neither text content nor the hand attribute are present, the display is application-specific.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``hand``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTapHand`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeTap
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tap'][@type='tap']"


class XMLTechnical(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/technical/>`_
    
    
    
    ``complexType``: Technical indications give performance information for individual instruments.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`

    ``Possible children``:    :obj:`~XMLArrow`, :obj:`~XMLBend`, :obj:`~XMLBrassBend`, :obj:`~XMLDoubleTongue`, :obj:`~XMLDownBow`, :obj:`~XMLFingering`, :obj:`~XMLFingernails`, :obj:`~XMLFlip`, :obj:`~XMLFret`, :obj:`~XMLGolpe`, :obj:`~XMLHalfMuted`, :obj:`~XMLHammerOn`, :obj:`~XMLHandbell`, :obj:`~XMLHarmonMute`, :obj:`~XMLHarmonic`, :obj:`~XMLHeel`, :obj:`~XMLHole`, :obj:`~XMLOpenString`, :obj:`~XMLOpen`, :obj:`~XMLOtherTechnical`, :obj:`~XMLPluck`, :obj:`~XMLPullOff`, :obj:`~XMLSmear`, :obj:`~XMLSnapPizzicato`, :obj:`~XMLStopped`, :obj:`~XMLString`, :obj:`~XMLTap`, :obj:`~XMLThumbPosition`, :obj:`~XMLToe`, :obj:`~XMLTripleTongue`, :obj:`~XMLUpBow`

    ``XSD structure:``

    .. code-block::

       Choice@minOccurs=0@maxOccurs=unbounded
           Element@name=up-bow@minOccurs=1@maxOccurs=1
           Element@name=down-bow@minOccurs=1@maxOccurs=1
           Element@name=harmonic@minOccurs=1@maxOccurs=1
           Element@name=open-string@minOccurs=1@maxOccurs=1
           Element@name=thumb-position@minOccurs=1@maxOccurs=1
           Element@name=fingering@minOccurs=1@maxOccurs=1
           Element@name=pluck@minOccurs=1@maxOccurs=1
           Element@name=double-tongue@minOccurs=1@maxOccurs=1
           Element@name=triple-tongue@minOccurs=1@maxOccurs=1
           Element@name=stopped@minOccurs=1@maxOccurs=1
           Element@name=snap-pizzicato@minOccurs=1@maxOccurs=1
           Element@name=fret@minOccurs=1@maxOccurs=1
           Element@name=string@minOccurs=1@maxOccurs=1
           Element@name=hammer-on@minOccurs=1@maxOccurs=1
           Element@name=pull-off@minOccurs=1@maxOccurs=1
           Element@name=bend@minOccurs=1@maxOccurs=1
           Element@name=tap@minOccurs=1@maxOccurs=1
           Element@name=heel@minOccurs=1@maxOccurs=1
           Element@name=toe@minOccurs=1@maxOccurs=1
           Element@name=fingernails@minOccurs=1@maxOccurs=1
           Element@name=hole@minOccurs=1@maxOccurs=1
           Element@name=arrow@minOccurs=1@maxOccurs=1
           Element@name=handbell@minOccurs=1@maxOccurs=1
           Element@name=brass-bend@minOccurs=1@maxOccurs=1
           Element@name=flip@minOccurs=1@maxOccurs=1
           Element@name=smear@minOccurs=1@maxOccurs=1
           Element@name=open@minOccurs=1@maxOccurs=1
           Element@name=half-muted@minOccurs=1@maxOccurs=1
           Element@name=harmon-mute@minOccurs=1@maxOccurs=1
           Element@name=golpe@minOccurs=1@maxOccurs=1
           Element@name=other-technical@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeTechnical
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='technical'][@type='technical']"


class XMLTenths(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tenths/>`_
    
    
    
    ``simpleType``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

``Possible parents``::obj:`~XMLScaling`
    """
    
    TYPE = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tenths'][@type='tenths']"


class XMLTenuto(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tenuto/>`_
    
    The tenuto element indicates a tenuto line symbol.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tenuto'][@type='empty-placement']"


class XMLText(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/text/>`_
    
    
    
    ``complexType``: The text-element-data type represents a syllable or portion of a syllable for lyric text underlay. A hyphen in the string content should only be used for an actual hyphenated word. Language names for text elements come from ISO 639, with optional country subcodes from ISO 3166.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dir``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTextDirection`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``lang``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLanguage`, ``letter_spacing``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOrNormal`, ``line_through``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOfLines`, ``overline``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOfLines`, ``rotation``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeRotationDegrees`, ``underline``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberOfLines`

``Possible parents``::obj:`~XMLLyric`
    """
    
    TYPE = XSDComplexTypeTextElementData
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='text'][@type='text-element-data']"


class XMLThumbPosition(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/thumb-position/>`_
    
    The thumb-position element represents the thumb position symbol. This is a circle with a line, where the line does not come within the circle. It is distinct from the snap pizzicato symbol, where the line comes inside the circle.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='thumb-position'][@type='empty-placement']"


class XMLTie(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tie/>`_
    
    
    
    ``complexType``: The tie element indicates that a tie begins or ends with this note. If the tie element applies only particular times through a repeat, the time-only attribute indicates which times to apply it. The tie element indicates sound; the tied element indicates notation.

    ``Possible attributes``: ``time_only``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeOnly`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeTie
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tie'][@type='tie']"


class XMLTied(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tied/>`_
    
    
    
    ``complexType``: The tied element represents the notated tie. The tie element represents the tie sound.
    
    The number attribute is rarely needed to disambiguate ties, since note pitches will usually suffice. The attribute is implied rather than defaulting to 1 as with most elements. It is available for use in more complex tied notation situations.
    
    Ties that join two notes of the same pitch together should be represented with a tied element on the first note with type="start" and a tied element on the second note with type="stop".  This can also be done if the two notes being tied are enharmonically equivalent, but have different step values. It is not recommended to use tied elements to join two notes with enharmonically inequivalent pitches.
    
    Ties that indicate that an instrument should be undamped are specified with a single tied element with type="let-ring".
    
    Ties that are visually attached to only one note, other than undamped ties, should be specified with two tied elements on the same note, first type="start" then type="stop". This can be used to represent ties into or out of repeated sections or codas.

    ``Possible attributes``: ``bezier_offset2``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeDivisions`, ``bezier_offset``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeDivisions`, ``bezier_x2``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``bezier_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``bezier_y2``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``bezier_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dash_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``line_type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineType`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``orientation``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeOverUnder`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``space_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTiedType`\@required

``Possible parents``::obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeTied
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tied'][@type='tied']"


class XMLTime(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/time/>`_
    
    Time signatures are represented by the beats element for the numerator and the beat-type element for the denominator.
    
    
    
    ``complexType``: Time signatures are represented by the beats element for the numerator and the beat-type element for the denominator. The symbol attribute is used to indicate common and cut time symbols as well as a single number display. Multiple pairs of beat and beat-type elements are used for composite time signatures with multiple denominators, such as 2/4 + 3/8. A composite such as 3+2/8 requires only one beat/beat-type pair.
    
    The print-object attribute allows a time signature to be specified but not printed, as is the case for excerpts from the middle of a score. The value is "yes" if not present. The optional number attribute refers to staff numbers within the part. If absent, the time signature applies to all staves in the part.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``halign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLeftCenterRight`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffNumber`, ``print_object``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``separator``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeSeparator`, ``symbol``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeSymbol`, ``valign``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeValign`

    ``Possible children``:    :obj:`~XMLBeatType`, :obj:`~XMLBeats`, :obj:`~XMLInterchangeable`, :obj:`~XMLSenzaMisura`

    ``XSD structure:``

    .. code-block::

       Choice@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Group@name=time-signature@minOccurs=1@maxOccurs=unbounded
                   Sequence@minOccurs=1@maxOccurs=1
                       Element@name=beats@minOccurs=1@maxOccurs=1
                       Element@name=beat-type@minOccurs=1@maxOccurs=1
               Element@name=interchangeable@minOccurs=0@maxOccurs=1
           Element@name=senza-misura@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLAttributes`
    """
    
    TYPE = XSDComplexTypeTime
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='time'][@type='time']"


class XMLTimeModification(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/time-modification/>`_
    
    
    
    ``complexType``: Time modification indicates tuplets, double-note tremolos, and other durational changes. A time-modification element shows how the cumulative, sounding effect of tuplets and double-note tremolos compare to the written note type represented by the type and dot elements. Nested tuplets and other notations that use more detailed information need both the time-modification and tuplet elements to be represented accurately.

    ``Possible children``:    :obj:`~XMLActualNotes`, :obj:`~XMLNormalDot`, :obj:`~XMLNormalNotes`, :obj:`~XMLNormalType`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=actual-notes@minOccurs=1@maxOccurs=1
           Element@name=normal-notes@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=0@maxOccurs=1
               Element@name=normal-type@minOccurs=1@maxOccurs=1
               Element@name=normal-dot@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeTimeModification
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='time-modification'][@type='time-modification']"


class XMLTimeRelation(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/time-relation/>`_
    
    
    
    ``simpleType``: The time-relation type indicates the symbol used to represent the interchangeable aspect of dual time signatures.
        
        Permitted Values: ``'parentheses'``, ``'bracket'``, ``'equals'``, ``'slash'``, ``'space'``, ``'hyphen'``
    

``Possible parents``::obj:`~XMLInterchangeable`
    """
    
    TYPE = XSDSimpleTypeTimeRelation
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='time-relation'][@type='time-relation']"


class XMLTimpani(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/timpani/>`_
    
    
    
    ``complexType``: The timpani type represents the timpani pictogram. The smufl attribute is used to distinguish different SMuFL stylistic alternates.

    ``Possible attributes``: ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflPictogramGlyphName`

``Possible parents``::obj:`~XMLPercussion`
    """
    
    TYPE = XSDComplexTypeTimpani
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='timpani'][@type='timpani']"


class XMLToe(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/toe/>`_
    
    
    
    ``complexType``: The heel and toe elements are used with organ pedals. The substitution value is "no" if the attribute is not present.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``substitution``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeHeelToe
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='toe'][@type='heel-toe']"


class XMLTopMargin(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/top-margin/>`_
    
    
    
    ``simpleType``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

``Possible parents``::obj:`~XMLPageMargins`
    """
    
    TYPE = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='top-margin'][@type='tenths']"


class XMLTopSystemDistance(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/top-system-distance/>`_
    
    
    
    ``simpleType``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.
    
    Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.

``Possible parents``::obj:`~XMLSystemLayout`
    """
    
    TYPE = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='top-system-distance'][@type='tenths']"


class XMLTouchingPitch(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/touching-pitch/>`_
    
    The touching-pitch is the pitch at which the string is touched lightly to produce the harmonic.
    
    
    
    ``complexType``: The empty type represents an empty element with no attributes.

``Possible parents``::obj:`~XMLHarmonic`
    """
    
    TYPE = XSDComplexTypeEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='touching-pitch'][@type='empty']"


class XMLTranspose(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/transpose/>`_
    
    If the part is being encoded for a transposing instrument in written vs. concert pitch, the transposition must be encoded in the transpose element using the transpose type.
    
    
    
    ``complexType``: The transpose type represents what must be added to a written pitch to get a correct sounding pitch. The optional number attribute refers to staff numbers, from top to bottom on the system. If absent, the transposition applies to all staves in the part. Per-staff transposition is most often used in parts that represent multiple instruments.

    ``Possible attributes``: ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStaffNumber`

    ``Possible children``:    :obj:`~XMLChromatic`, :obj:`~XMLDiatonic`, :obj:`~XMLDouble`, :obj:`~XMLOctaveChange`

    ``XSD structure:``

    .. code-block::

       Group@name=transpose@minOccurs=1@maxOccurs=1
           Sequence@minOccurs=1@maxOccurs=1
               Element@name=diatonic@minOccurs=0@maxOccurs=1
               Element@name=chromatic@minOccurs=1@maxOccurs=1
               Element@name=octave-change@minOccurs=0@maxOccurs=1
               Element@name=double@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLAttributes`
    """
    
    TYPE = XSDComplexTypeTranspose
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='transpose'][@type='transpose']"


class XMLTremolo(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tremolo/>`_
    
    
    
    ``complexType``: The tremolo ornament can be used to indicate single-note, double-note, or unmeasured tremolos. Single-note tremolos use the single type, double-note tremolos use the start and stop types, and unmeasured tremolos use the unmeasured type. The default is "single" for compatibility with Version 1.1. The text of the element indicates the number of tremolo marks and is an integer from 0 to 8. Note that the number of attached beams is not included in this value, but is represented separately using the beam element. The value should be 0 for unmeasured tremolos.
    
    When using double-note tremolos, the duration of each note in the tremolo should correspond to half of the notated type value. A time-modification element should also be added with an actual-notes value of 2 and a normal-notes value of 1. If used within a tuplet, this 2/1 ratio should be multiplied by the existing tuplet ratio.
    
    The smufl attribute specifies the glyph to use from the SMuFL Tremolos range for an unmeasured tremolo. It is ignored for other tremolo types. The SMuFL buzzRoll glyph is used by default if the attribute is missing.
    
    Using repeater beams for indicating tremolos is deprecated as of MusicXML 3.0.
    
    ``simpleContent``: The number of tremolo marks is represented by a number from 0 to 8: the same as beam-level with 0 added.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflGlyphName`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTremoloType`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeTremolo
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tremolo'][@type='tremolo']"


class XMLTrillMark(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/trill-mark/>`_
    
    The trill-mark element represents the trill-mark symbol.
    
    
    
    ``complexType``: The empty-trill-sound type represents an empty element with print-style, placement, and trill-sound attributes.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``second_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``start_note``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartNote`, ``trill_step``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillStep`, ``two_note_turn``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTwoNoteTurn`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeEmptyTrillSound
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='trill-mark'][@type='empty-trill-sound']"


class XMLTripleTongue(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/triple-tongue/>`_
    
    The triple-tongue element represents the triple tongue symbol (three dots arranged horizontally).
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='triple-tongue'][@type='empty-placement']"


class XMLTuningAlter(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tuning-alter/>`_
    
    The tuning-alter element is represented like the alter element, with a different name to reflect its different function in string tuning.
    
    
    
    ``simpleType``: The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.

``Possible parents``::obj:`~XMLAccord`, :obj:`~XMLStaffTuning`
    """
    
    TYPE = XSDSimpleTypeSemitones
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tuning-alter'][@type='semitones']"


class XMLTuningOctave(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tuning-octave/>`_
    
    The tuning-octave element is represented like the octave element, with a different name to reflect its different function in string tuning.
    
    
    
    ``simpleType``: Octaves are represented by the numbers 0 to 9, where 4 indicates the octave started by middle C.

``Possible parents``::obj:`~XMLAccord`, :obj:`~XMLStaffTuning`
    """
    
    TYPE = XSDSimpleTypeOctave
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tuning-octave'][@type='octave']"


class XMLTuningStep(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tuning-step/>`_
    
    The tuning-step element is represented like the step element, with a different name to reflect its different function in string tuning.
    
    
    
    ``simpleType``: The step type represents a step of the diatonic scale, represented using the English letters A through G.
        
        Permitted Values: ``'A'``, ``'B'``, ``'C'``, ``'D'``, ``'E'``, ``'F'``, ``'G'``
    

``Possible parents``::obj:`~XMLAccord`, :obj:`~XMLStaffTuning`
    """
    
    TYPE = XSDSimpleTypeStep
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tuning-step'][@type='step']"


class XMLTuplet(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tuplet/>`_
    
    
    
    ``complexType``: A tuplet element is present when a tuplet is to be displayed graphically, in addition to the sound data provided by the time-modification elements. The number attribute is used to distinguish nested tuplets. The bracket attribute is used to indicate the presence of a bracket. If unspecified, the results are implementation-dependent. The line-shape attribute is used to specify whether the bracket is straight or in the older curved or slurred style. It is straight by default.
    
    Whereas a time-modification element shows how the cumulative, sounding effect of tuplets and double-note tremolos compare to the written note type, the tuplet element describes how this is displayed. The tuplet element also provides more detailed representation information than the time-modification element, and is needed to represent nested tuplets and other complex tuplets accurately.
    
    The show-number attribute is used to display either the number of actual notes, the number of both actual and normal notes, or neither. It is actual by default. The show-type attribute is used to display either the actual type, both the actual and normal types, or neither. It is none by default.

    ``Possible attributes``: ``bracket``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``line_shape``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineShape`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``show_number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeShowTuplet`, ``show_type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeShowTuplet`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStop`\@required

    ``Possible children``:    :obj:`~XMLTupletActual`, :obj:`~XMLTupletNormal`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=tuplet-actual@minOccurs=0@maxOccurs=1
           Element@name=tuplet-normal@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLNotations`
    """
    
    TYPE = XSDComplexTypeTuplet
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tuplet'][@type='tuplet']"


class XMLTupletActual(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tuplet-actual/>`_
    
    The tuplet-actual element provide optional full control over how the actual part of the tuplet is displayed, including number and note type (with dots). If any of these elements are absent, their values are based on the time-modification element.
    
    
    
    ``complexType``: The tuplet-portion type provides optional full control over tuplet specifications. It allows the number and note type (including dots) to be set for the actual and normal portions of a single tuplet. If any of these elements are absent, their values are based on the time-modification element.

    ``Possible children``:    :obj:`~XMLTupletDot`, :obj:`~XMLTupletNumber`, :obj:`~XMLTupletType`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=tuplet-number@minOccurs=0@maxOccurs=1
           Element@name=tuplet-type@minOccurs=0@maxOccurs=1
           Element@name=tuplet-dot@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLTuplet`
    """
    
    TYPE = XSDComplexTypeTupletPortion
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tuplet-actual'][@type='tuplet-portion']"


class XMLTupletDot(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tuplet-dot/>`_
    
    
    
    ``complexType``: The tuplet-dot type is used to specify dotted tuplet types.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`

``Possible parents``::obj:`~XMLTupletActual`, :obj:`~XMLTupletNormal`
    """
    
    TYPE = XSDComplexTypeTupletDot
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tuplet-dot'][@type='tuplet-dot']"


class XMLTupletNormal(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tuplet-normal/>`_
    
    The tuplet-normal element provide optional full control over how the normal part of the tuplet is displayed, including number and note type (with dots). If any of these elements are absent, their values are based on the time-modification element.
    
    
    
    ``complexType``: The tuplet-portion type provides optional full control over tuplet specifications. It allows the number and note type (including dots) to be set for the actual and normal portions of a single tuplet. If any of these elements are absent, their values are based on the time-modification element.

    ``Possible children``:    :obj:`~XMLTupletDot`, :obj:`~XMLTupletNumber`, :obj:`~XMLTupletType`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=tuplet-number@minOccurs=0@maxOccurs=1
           Element@name=tuplet-type@minOccurs=0@maxOccurs=1
           Element@name=tuplet-dot@minOccurs=0@maxOccurs=unbounded

``Possible parents``::obj:`~XMLTuplet`
    """
    
    TYPE = XSDComplexTypeTupletPortion
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tuplet-normal'][@type='tuplet-portion']"


class XMLTupletNumber(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tuplet-number/>`_
    
    
    
    ``complexType``: The tuplet-number type indicates the number of notes for this portion of the tuplet.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`

``Possible parents``::obj:`~XMLTupletActual`, :obj:`~XMLTupletNormal`
    """
    
    TYPE = XSDComplexTypeTupletNumber
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tuplet-number'][@type='tuplet-number']"


class XMLTupletType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tuplet-type/>`_
    
    
    
    ``complexType``: The tuplet-type type indicates the graphical note type of the notes for this portion of the tuplet.
    
    ``simpleContent``: The note-type-value type is used for the MusicXML type element and represents the graphic note type, from 1024th (shortest) to maxima (longest).
        
        Permitted Values: ``'1024th'``, ``'512th'``, ``'256th'``, ``'128th'``, ``'64th'``, ``'32nd'``, ``'16th'``, ``'eighth'``, ``'quarter'``, ``'half'``, ``'whole'``, ``'breve'``, ``'long'``, ``'maxima'``
    

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`

``Possible parents``::obj:`~XMLTupletActual`, :obj:`~XMLTupletNormal`
    """
    
    TYPE = XSDComplexTypeTupletType
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='tuplet-type'][@type='tuplet-type']"


class XMLTurn(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/turn/>`_
    
    The turn element is the normal turn shape which goes up then down.
    
    
    
    ``complexType``: The horizontal-turn type represents turn elements that are horizontal rather than vertical. These are empty elements with print-style, placement, trill-sound, and slash attributes. If the slash attribute is yes, then a vertical line is used to slash the turn. It is no if not specified.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``second_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``slash``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``start_note``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartNote`, ``trill_step``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillStep`, ``two_note_turn``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTwoNoteTurn`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeHorizontalTurn
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='turn'][@type='horizontal-turn']"


class XMLType(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/type/>`_
    
    
    
    ``complexType``: The note-type type indicates the graphic note type. Values range from 1024th to maxima. The size attribute indicates full, cue, grace-cue, or large size. The default is full for regular notes, grace-cue for notes that contain both grace and cue elements, and cue for notes that contain either a cue or a grace element, but not both.
    
    ``simpleContent``: The note-type-value type is used for the MusicXML type element and represents the graphic note type, from 1024th (shortest) to maxima (longest).
        
        Permitted Values: ``'1024th'``, ``'512th'``, ``'256th'``, ``'128th'``, ``'64th'``, ``'32nd'``, ``'16th'``, ``'eighth'``, ``'quarter'``, ``'half'``, ``'whole'``, ``'breve'``, ``'long'``, ``'maxima'``
    

    ``Possible attributes``: ``size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSymbolSize`

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeNoteType
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='type'][@type='note-type']"


class XMLUnpitched(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/unpitched/>`_
    
    
    
    ``complexType``: The unpitched type represents musical elements that are notated on the staff but lack definite pitch, such as unpitched percussion and speaking voice. If the child elements are not present, the note is placed on the middle line of the staff. This is generally used with a one-line staff. Notes in percussion clef should always use an unpitched element rather than a pitch element.

    ``Possible children``:    :obj:`~XMLDisplayOctave`, :obj:`~XMLDisplayStep`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Group@name=display-step-octave@minOccurs=0@maxOccurs=1
               Sequence@minOccurs=1@maxOccurs=1
                   Element@name=display-step@minOccurs=1@maxOccurs=1
                   Element@name=display-octave@minOccurs=1@maxOccurs=1

``Possible parents``::obj:`~XMLNote`
    """
    
    TYPE = XSDComplexTypeUnpitched
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='unpitched'][@type='unpitched']"


class XMLUnstress(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/unstress/>`_
    
    The unstress element indicates an unstressed note. It is often notated using a u-shaped symbol.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLArticulations`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='unstress'][@type='empty-placement']"


class XMLUpBow(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/up-bow/>`_
    
    The up-bow element represents the symbol that is used both for up-bowing on bowed instruments, and up-stroke on plucked instruments.
    
    
    
    ``complexType``: The empty-placement type represents an empty element with print-style and placement attributes.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLTechnical`
    """
    
    TYPE = XSDComplexTypeEmptyPlacement
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='up-bow'][@type='empty-placement']"


class XMLVerticalTurn(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/vertical-turn/>`_
    
    The vertical-turn element has the turn symbol shape arranged vertically going from upper left to lower right.
    
    
    
    ``complexType``: The empty-trill-sound type represents an empty element with print-style, placement, and trill-sound attributes.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``second_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``start_note``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartNote`, ``trill_step``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillStep`, ``two_note_turn``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTwoNoteTurn`

``Possible parents``::obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeEmptyTrillSound
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='vertical-turn'][@type='empty-trill-sound']"


class XMLVirtualInstrument(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/virtual-instrument/>`_
    
    
    
    ``complexType``: The virtual-instrument element defines a specific virtual instrument used for an instrument sound.

    ``Possible children``:    :obj:`~XMLVirtualLibrary`, :obj:`~XMLVirtualName`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=virtual-library@minOccurs=0@maxOccurs=1
           Element@name=virtual-name@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLInstrumentChange`, :obj:`~XMLScoreInstrument`
    """
    
    TYPE = XSDComplexTypeVirtualInstrument
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='virtual-instrument'][@type='virtual-instrument']"


class XMLVirtualLibrary(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/virtual-library/>`_

The virtual-library element indicates the virtual instrument library name.



``Possible parents``::obj:`~XMLVirtualInstrument`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='virtual-library'][@type='xs:string']"


class XMLVirtualName(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/virtual-name/>`_

The virtual-name element indicates the library-specific name for the virtual instrument.



``Possible parents``::obj:`~XMLVirtualInstrument`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='virtual-name'][@type='xs:string']"


class XMLVoice(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/voice/>`_



``Possible parents``::obj:`~XMLDirection`, :obj:`~XMLForward`, :obj:`~XMLNote`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='voice'][@type='xs:string']"


class XMLVolume(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/volume/>`_
    
    The volume element value is a percentage of the maximum ranging from 0 to 100, with decimal values allowed. This corresponds to a scaling value for the MIDI 1.0 channel volume controller.
    
    
    
    ``simpleType``: The percent type specifies a percentage from 0 to 100.

``Possible parents``::obj:`~XMLMidiInstrument`
    """
    
    TYPE = XSDSimpleTypePercent
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='volume'][@type='percent']"


class XMLWait(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/wait/>`_
    
    
    
    ``complexType``: The wait type specifies a point where the accompaniment should wait for a performer event before continuing. This typically happens at the start of new sections or after a held note or indeterminate music. These waiting points cannot always be inferred reliably from the contents of the displayed score. The optional player and time-only attributes restrict the type to apply to a single player or set of times through a repeated section, respectively.

    ``Possible attributes``: ``player``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF`, ``time_only``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTimeOnly`

``Possible parents``::obj:`~XMLListen`
    """
    
    TYPE = XSDComplexTypeWait
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='wait'][@type='wait']"


class XMLWavyLine(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/wavy-line/>`_
    
    
    
    ``complexType``: Wavy lines are one way to indicate trills and vibrato. When used with a barline element, they should always have type="continue" set. The smufl attribute specifies a particular wavy line glyph from the SMuFL Multi-segment lines range.

    ``Possible attributes``: ``accelerate``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``beats``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillBeats`, ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``last_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``second_beat``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypePercent`, ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflWavyLineGlyphName`, ``start_note``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartNote`, ``trill_step``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTrillStep`, ``two_note_turn``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTwoNoteTurn`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeStartStopContinue`\@required

``Possible parents``::obj:`~XMLBarline`, :obj:`~XMLOrnaments`
    """
    
    TYPE = XSDComplexTypeWavyLine
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='wavy-line'][@type='wavy-line']"


class XMLWedge(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/wedge/>`_
    
    
    
    ``complexType``: The wedge type represents crescendo and diminuendo wedge symbols. The type attribute is crescendo for the start of a wedge that is closed at the left side, and diminuendo for the start of a wedge that is closed on the right side. Spread values are measured in tenths; those at the start of a crescendo wedge or end of a diminuendo wedge are ignored. The niente attribute is yes if a circle appears at the point of the wedge, indicating a crescendo from nothing or diminuendo to nothing. It is no by default, and used only when the type is crescendo, or the type is stop for a wedge that began with a diminuendo type. The line-type is solid if not specified.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``dash_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``id``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeID`, ``line_type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeLineType`, ``niente``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeYesNo`, ``number``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeNumberLevel`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``space_length``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``spread``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``type``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeWedgeType`\@required

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeWedge
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='wedge'][@type='wedge']"


class XMLWithBar(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/with-bar/>`_
    
    The with-bar element indicates that the bend is to be done at the bridge with a whammy or vibrato bar. The content of the element indicates how this should be notated. Content values of "scoop" and "dip" refer to the SMuFL guitarVibratoBarScoop and guitarVibratoBarDip glyphs.
    
    
    
    ``complexType``: The placement-text type represents a text element with print-style and placement attribute groups.

    ``Possible attributes``: ``color``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeColor`, ``default_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``default_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`, ``placement``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeAboveBelow`, ``relative_x``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`, ``relative_y``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeTenths`

``Possible parents``::obj:`~XMLBend`
    """
    
    TYPE = XSDComplexTypePlacementText
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='with-bar'][@type='placement-text']"


class XMLWood(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/wood/>`_
    
    
    
    ``complexType``: The wood type represents pictograms for wood percussion instruments. The smufl attribute is used to distinguish different SMuFL stylistic alternates.
    
    ``simpleContent``: The wood-value type represents pictograms for wood percussion instruments. The maraca and maracas values distinguish the one- and two-maraca versions of the pictogram.
        
        Permitted Values: ``'bamboo scraper'``, ``'board clapper'``, ``'cabasa'``, ``'castanets'``, ``'castanets with handle'``, ``'claves'``, ``'football rattle'``, ``'guiro'``, ``'log drum'``, ``'maraca'``, ``'maracas'``, ``'quijada'``, ``'rainstick'``, ``'ratchet'``, ``'reco-reco'``, ``'sandpaper blocks'``, ``'slit drum'``, ``'temple block'``, ``'vibraslap'``, ``'whip'``, ``'wood block'``
    

    ``Possible attributes``: ``smufl``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeSmuflPictogramGlyphName`

``Possible parents``::obj:`~XMLPercussion`
    """
    
    TYPE = XSDComplexTypeWood
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='wood'][@type='wood']"


class XMLWordFont(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/word-font/>`_
    
    
    
    ``complexType``: The empty-font type represents an empty element with font attributes.

    ``Possible attributes``: ``font_family``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontFamily`, ``font_size``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontSize`, ``font_style``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontStyle`, ``font_weight``\@ :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeFontWeight`

``Possible parents``::obj:`~XMLDefaults`
    """
    
    TYPE = XSDComplexTypeEmptyFont
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='word-font'][@type='empty-font']"


class XMLWords(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/words/>`_
    
    The words element specifies a standard text direction. The enclosure is none if not specified. The language is Italian ("it") if not specified. Left justification is used if not specified.
    
    
    
    ``complexType``: The formatted-text-id type represents a text element with text-formatting and id attributes.

``Possible parents``::obj:`~XMLDirectionType`
    """
    
    TYPE = XSDComplexTypeFormattedTextId
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='words'][@type='formatted-text-id']"


class XMLWork(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/work/>`_
    
    
    
    ``complexType``: Works are optionally identified by number and title. The work type also may indicate a link to the opus document that composes multiple scores into a collection.

    ``Possible children``:    :obj:`~XMLOpus`, :obj:`~XMLWorkNumber`, :obj:`~XMLWorkTitle`

    ``XSD structure:``

    .. code-block::

       Sequence@minOccurs=1@maxOccurs=1
           Element@name=work-number@minOccurs=0@maxOccurs=1
           Element@name=work-title@minOccurs=0@maxOccurs=1
           Element@name=opus@minOccurs=0@maxOccurs=1

``Possible parents``::obj:`~XMLScorePartwise`
    """
    
    TYPE = XSDComplexTypeWork
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='work'][@type='work']"


class XMLWorkNumber(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/work-number/>`_

The work-number element specifies the number of a work, such as its opus number.



``Possible parents``::obj:`~XMLWork`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='work-number'][@type='xs:string']"


class XMLWorkTitle(XMLElement):
    """
    `external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/work-title/>`_

The work-title element specifies the title of a work, not including its opus or other work number.



``Possible parents``::obj:`~XMLWork`
    """
    
    TYPE = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='work-title'][@type='xs:string']"

__all__=['XMLSenzaMisura', 'XMLAccent', 'XMLAccidental', 'XMLAccidentalMark', 'XMLAccidentalText', 'XMLAccord', 'XMLAccordionHigh', 'XMLAccordionLow', 'XMLAccordionMiddle', 'XMLAccordionRegistration', 'XMLActualNotes', 'XMLAlter', 'XMLAppearance', 'XMLArpeggiate', 'XMLArrow', 'XMLArrowDirection', 'XMLArrowStyle', 'XMLArrowhead', 'XMLArticulations', 'XMLArtificial', 'XMLAssess', 'XMLAttributes', 'XMLBackup', 'XMLBarStyle', 'XMLBarline', 'XMLBarre', 'XMLBasePitch', 'XMLBass', 'XMLBassAlter', 'XMLBassSeparator', 'XMLBassStep', 'XMLBeam', 'XMLBeatRepeat', 'XMLBeatType', 'XMLBeatUnit', 'XMLBeatUnitDot', 'XMLBeatUnitTied', 'XMLBeater', 'XMLBeats', 'XMLBend', 'XMLBendAlter', 'XMLBookmark', 'XMLBottomMargin', 'XMLBracket', 'XMLBrassBend', 'XMLBreathMark', 'XMLCaesura', 'XMLCancel', 'XMLCapo', 'XMLChord', 'XMLChromatic', 'XMLCircularArrow', 'XMLClef', 'XMLClefOctaveChange', 'XMLCoda', 'XMLConcertScore', 'XMLCreator', 'XMLCredit', 'XMLCreditImage', 'XMLCreditSymbol', 'XMLCreditType', 'XMLCreditWords', 'XMLCue', 'XMLDamp', 'XMLDampAll', 'XMLDashes', 'XMLDefaults', 'XMLDegree', 'XMLDegreeAlter', 'XMLDegreeType', 'XMLDegreeValue', 'XMLDelayedInvertedTurn', 'XMLDelayedTurn', 'XMLDetachedLegato', 'XMLDiatonic', 'XMLDirection', 'XMLDirectionType', 'XMLDirective', 'XMLDisplayOctave', 'XMLDisplayStep', 'XMLDisplayText', 'XMLDistance', 'XMLDivisions', 'XMLDoit', 'XMLDot', 'XMLDouble', 'XMLDoubleTongue', 'XMLDownBow', 'XMLDuration', 'XMLDynamics', 'XMLEffect', 'XMLElevation', 'XMLElision', 'XMLEncoder', 'XMLEncoding', 'XMLEncodingDate', 'XMLEncodingDescription', 'XMLEndLine', 'XMLEndParagraph', 'XMLEnding', 'XMLEnsemble', 'XMLExceptVoice', 'XMLExtend', 'XMLEyeglasses', 'XMLF', 'XMLFalloff', 'XMLFeature', 'XMLFermata', 'XMLFf', 'XMLFff', 'XMLFfff', 'XMLFffff', 'XMLFfffff', 'XMLFifths', 'XMLFigure', 'XMLFigureNumber', 'XMLFiguredBass', 'XMLFingering', 'XMLFingernails', 'XMLFirst', 'XMLFirstFret', 'XMLFlip', 'XMLFootnote', 'XMLForPart', 'XMLForward', 'XMLFp', 'XMLFrame', 'XMLFrameFrets', 'XMLFrameNote', 'XMLFrameStrings', 'XMLFret', 'XMLFunction', 'XMLFz', 'XMLGlass', 'XMLGlissando', 'XMLGlyph', 'XMLGolpe', 'XMLGrace', 'XMLGroup', 'XMLGroupAbbreviation', 'XMLGroupAbbreviationDisplay', 'XMLGroupBarline', 'XMLGroupLink', 'XMLGroupName', 'XMLGroupNameDisplay', 'XMLGroupSymbol', 'XMLGroupTime', 'XMLGrouping', 'XMLHalfMuted', 'XMLHammerOn', 'XMLHandbell', 'XMLHarmonClosed', 'XMLHarmonMute', 'XMLHarmonic', 'XMLHarmony', 'XMLHarpPedals', 'XMLHaydn', 'XMLHeel', 'XMLHole', 'XMLHoleClosed', 'XMLHoleShape', 'XMLHoleType', 'XMLHumming', 'XMLIdentification', 'XMLImage', 'XMLInstrument', 'XMLInstrumentAbbreviation', 'XMLInstrumentChange', 'XMLInstrumentLink', 'XMLInstrumentName', 'XMLInstrumentSound', 'XMLInstruments', 'XMLInterchangeable', 'XMLInversion', 'XMLInvertedMordent', 'XMLInvertedTurn', 'XMLInvertedVerticalTurn', 'XMLIpa', 'XMLKey', 'XMLKeyAccidental', 'XMLKeyAlter', 'XMLKeyOctave', 'XMLKeyStep', 'XMLKind', 'XMLLaughing', 'XMLLeftDivider', 'XMLLeftMargin', 'XMLLevel', 'XMLLine', 'XMLLineDetail', 'XMLLineWidth', 'XMLLink', 'XMLListen', 'XMLListening', 'XMLLyric', 'XMLLyricFont', 'XMLLyricLanguage', 'XMLMeasure', 'XMLMeasureDistance', 'XMLMeasureLayout', 'XMLMeasureNumbering', 'XMLMeasureRepeat', 'XMLMeasureStyle', 'XMLMembrane', 'XMLMetal', 'XMLMetronome', 'XMLMetronomeArrows', 'XMLMetronomeBeam', 'XMLMetronomeDot', 'XMLMetronomeNote', 'XMLMetronomeRelation', 'XMLMetronomeTied', 'XMLMetronomeTuplet', 'XMLMetronomeType', 'XMLMf', 'XMLMidiBank', 'XMLMidiChannel', 'XMLMidiDevice', 'XMLMidiInstrument', 'XMLMidiName', 'XMLMidiProgram', 'XMLMidiUnpitched', 'XMLMillimeters', 'XMLMiscellaneous', 'XMLMiscellaneousField', 'XMLMode', 'XMLMordent', 'XMLMovementNumber', 'XMLMovementTitle', 'XMLMp', 'XMLMultipleRest', 'XMLMusicFont', 'XMLMute', 'XMLN', 'XMLNatural', 'XMLNonArpeggiate', 'XMLNormalDot', 'XMLNormalNotes', 'XMLNormalType', 'XMLNotations', 'XMLNote', 'XMLNoteSize', 'XMLNotehead', 'XMLNoteheadText', 'XMLNumeral', 'XMLNumeralAlter', 'XMLNumeralFifths', 'XMLNumeralKey', 'XMLNumeralMode', 'XMLNumeralRoot', 'XMLOctave', 'XMLOctaveChange', 'XMLOctaveShift', 'XMLOffset', 'XMLOpen', 'XMLOpenString', 'XMLOpus', 'XMLOrnaments', 'XMLOtherAppearance', 'XMLOtherArticulation', 'XMLOtherDirection', 'XMLOtherDynamics', 'XMLOtherListen', 'XMLOtherListening', 'XMLOtherNotation', 'XMLOtherOrnament', 'XMLOtherPercussion', 'XMLOtherPlay', 'XMLOtherTechnical', 'XMLP', 'XMLPageHeight', 'XMLPageLayout', 'XMLPageMargins', 'XMLPageWidth', 'XMLPan', 'XMLPart', 'XMLPartAbbreviation', 'XMLPartAbbreviationDisplay', 'XMLPartClef', 'XMLPartGroup', 'XMLPartLink', 'XMLPartList', 'XMLPartName', 'XMLPartNameDisplay', 'XMLPartSymbol', 'XMLPartTranspose', 'XMLPedal', 'XMLPedalAlter', 'XMLPedalStep', 'XMLPedalTuning', 'XMLPerMinute', 'XMLPercussion', 'XMLPf', 'XMLPitch', 'XMLPitched', 'XMLPlay', 'XMLPlayer', 'XMLPlayerName', 'XMLPlop', 'XMLPluck', 'XMLPp', 'XMLPpp', 'XMLPppp', 'XMLPpppp', 'XMLPppppp', 'XMLPreBend', 'XMLPrefix', 'XMLPrincipalVoice', 'XMLPrint', 'XMLPullOff', 'XMLRehearsal', 'XMLRelation', 'XMLRelease', 'XMLRepeat', 'XMLRest', 'XMLRf', 'XMLRfz', 'XMLRightDivider', 'XMLRightMargin', 'XMLRights', 'XMLRoot', 'XMLRootAlter', 'XMLRootStep', 'XMLScaling', 'XMLSchleifer', 'XMLScoop', 'XMLScordatura', 'XMLScoreInstrument', 'XMLScorePart', 'XMLScorePartwise', 'XMLSecond', 'XMLSegno', 'XMLSemiPitched', 'XMLSf', 'XMLSffz', 'XMLSfp', 'XMLSfpp', 'XMLSfz', 'XMLSfzp', 'XMLShake', 'XMLSign', 'XMLSlash', 'XMLSlashDot', 'XMLSlashType', 'XMLSlide', 'XMLSlur', 'XMLSmear', 'XMLSnapPizzicato', 'XMLSoftAccent', 'XMLSoftware', 'XMLSolo', 'XMLSound', 'XMLSoundingPitch', 'XMLSource', 'XMLSpiccato', 'XMLStaccatissimo', 'XMLStaccato', 'XMLStaff', 'XMLStaffDetails', 'XMLStaffDistance', 'XMLStaffDivide', 'XMLStaffLayout', 'XMLStaffLines', 'XMLStaffSize', 'XMLStaffTuning', 'XMLStaffType', 'XMLStaves', 'XMLStem', 'XMLStep', 'XMLStick', 'XMLStickLocation', 'XMLStickMaterial', 'XMLStickType', 'XMLStopped', 'XMLStraight', 'XMLStress', 'XMLString', 'XMLStringMute', 'XMLStrongAccent', 'XMLSuffix', 'XMLSupports', 'XMLSwing', 'XMLSwingStyle', 'XMLSwingType', 'XMLSyllabic', 'XMLSymbol', 'XMLSync', 'XMLSystemDistance', 'XMLSystemDividers', 'XMLSystemLayout', 'XMLSystemMargins', 'XMLTap', 'XMLTechnical', 'XMLTenths', 'XMLTenuto', 'XMLText', 'XMLThumbPosition', 'XMLTie', 'XMLTied', 'XMLTime', 'XMLTimeModification', 'XMLTimeRelation', 'XMLTimpani', 'XMLToe', 'XMLTopMargin', 'XMLTopSystemDistance', 'XMLTouchingPitch', 'XMLTranspose', 'XMLTremolo', 'XMLTrillMark', 'XMLTripleTongue', 'XMLTuningAlter', 'XMLTuningOctave', 'XMLTuningStep', 'XMLTuplet', 'XMLTupletActual', 'XMLTupletDot', 'XMLTupletNormal', 'XMLTupletNumber', 'XMLTupletType', 'XMLTurn', 'XMLType', 'XMLUnpitched', 'XMLUnstress', 'XMLUpBow', 'XMLVerticalTurn', 'XMLVirtualInstrument', 'XMLVirtualLibrary', 'XMLVirtualName', 'XMLVoice', 'XMLVolume', 'XMLWait', 'XMLWavyLine', 'XMLWedge', 'XMLWithBar', 'XMLWood', 'XMLWordFont', 'XMLWords', 'XMLWork', 'XMLWorkNumber', 'XMLWorkTitle']
