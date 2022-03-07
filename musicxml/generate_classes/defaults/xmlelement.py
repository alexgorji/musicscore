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
