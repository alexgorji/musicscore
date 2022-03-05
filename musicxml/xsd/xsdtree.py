import io
import re
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from typing import Optional

from musicxml.generate_classes.utils import musicxml_xsd_et_root
from musicxml.util.helprervariables import xml_name_first_character_without_colon, name_character_without_colon, name_character, \
    xml_name_first_character
from tree.tree import Tree
from musicxml.util.core import cap_first, convert_to_xsd_class_name

"""
XSD = XML Schema Definition
"""


class XSDTree(Tree):
    """
    XSDTree gets a xml.etree.ElementTree.Element by initiation as its xml_element_tree_element property and
    prepares all needed information for generating a XSDTreeElement class (XSDTreeElement can be XSDSimpleType, XSDComplexType, XSDGroup,
    XMLAttribute and XMLAttributeGroup)
    """

    def __init__(self, xml_element_tree_element, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._namespace = None
        self._tag = None
        self._xsd_element_tree_element = None
        self._xml_tree_class_name = None
        self._xsd_indicator = None

        self.xml_element_tree_element = xml_element_tree_element

    # ------------------
    # private properties

    # ------------------
    # private methods

    def _get_xsd_tree_class_name(self):
        tag = cap_first(self.tag)

        name = 'XSD' + f'{tag}'
        if self.name:
            name += ''.join([cap_first(partial) for partial in self.name.split('-')])
        elif self.get_attributes().get('ref'):
            name += ''.join([cap_first(partial) for partial in self.get_attributes().get('ref').split('-')])
        else:
            raise AttributeError
        return name

    def _populate_children(self):
        for child in [XSDTree(node) for node in self.xml_element_tree_element.findall('./')]:
            self.add_child(child)

    def _check_child_to_be_added(self, child):
        if not isinstance(child, XSDTree):
            raise TypeError

    # ------------------
    # public properties
    @property
    def xsd_tree_base_class_names(self):

        if self.is_simple_type:
            # simple type
            if self.get_restriction():
                base = self.get_restriction().get_attributes()['base']
                return [convert_to_xsd_class_name(base)]
            elif self.get_union_member_types():
                return []
            else:
                raise AttributeError(f"Simple type {self} has no restriction with base attribute or union with memberTypes.")
        elif self.is_complex_type:
            # complex type
            if self.get_simple_content_extension():
                base = self.get_simple_content_extension().get_attributes()['base']
                return [convert_to_xsd_class_name(base, type_='simple_type')]
            else:
                return []
                # raise AttributeError(f"Complex type {self} has no simple content extension with base attribute.")
        else:
            raise NotImplementedError

    @property
    def compact_repr(self):
        attrs = self.get_attributes()
        return f"{self.tag}{''.join([f'@{attribute}={attrs[attribute]}' for attribute in attrs])}"

    @property
    def is_simple_type(self):
        if self.tag == 'simpleType':
            return True
        return False

    @property
    def is_complex_type(self):
        if self.tag == 'complexType':
            return True
        return False

    @property
    def name(self):
        try:
            return self.xml_element_tree_element.attrib['name']
        except KeyError:
            return

    @property
    def namespace(self):
        if not self._namespace:
            self._namespace = re.match(r'({.*})(.*)', self.xml_element_tree_element.tag).group(1)
        return self._namespace

    @property
    def tag(self):
        if not self._tag:
            self._tag = re.match(r'({.*})(.*)', self.xml_element_tree_element.tag).group(2)
        return self._tag

    @property
    def text(self):
        return self.xml_element_tree_element.text

    @property
    def xml_element_tree_element(self):
        return self._xsd_element_tree_element

    @xml_element_tree_element.setter
    def xml_element_tree_element(self, value):
        if not isinstance(value, ET.Element):
            raise TypeError(
                f"XSDTree must be initiated with an xml_element_tree_element of type xml.etree.ElementTree.Element not "
                f"{type(value)}")
        self._xsd_element_tree_element = value

    @property
    def xsd_element_class_name(self):
        if self._xml_tree_class_name is None:
            self._xml_tree_class_name = self._get_xsd_tree_class_name()
        return self._xml_tree_class_name

    # ------------------
    # public methods
    def get_attributes(self):
        return self.xml_element_tree_element.attrib

    def get_children(self):
        if not self._children:
            self._populate_children()
        return self._children

    def get_complex_content(self):
        for node in self.get_children():
            if node.tag == 'complexContent':
                return node

    def get_complex_content_extension(self):
        if self.get_complex_content().get_children()[0].tag == 'extension':
            return self.get_complex_content().get_children()[0]

    def get_doc(self):
        output = ''
        for node in self.traverse():
            if node.tag == 'documentation':
                output = node.text.strip()
                output.replace('\t', '    ')
                break
        permitted = self.get_permitted()
        pattern = self.get_pattern()
        if permitted:
            output += '\n    '
            output += '\n    '
            permitted = [f"``'{perm}'``" if perm else "``''``" for perm in permitted]
            output += f"Permitted Values: {', '.join(perm for perm in permitted)}\n"
        if pattern:
            output += '\n    '
            output += '\n    '
            output += f"    \nPattern: {pattern}\n"

        return output

    def get_restriction(self):
        for node in self.get_children():
            if node.tag == 'restriction':
                return node

    def get_pattern(self, parent_xsd_tree=None):
        def get_xsd_pattern(restriction_):
            if restriction_ and restriction_.get_children() and restriction_.get_children()[0].tag == 'pattern':
                return rf"{restriction.get_children()[0].get_attributes()['value']}"
            else:
                if parent_xsd_tree:
                    parent_restriction = parent_xsd_tree.get_restriction()
                    if parent_restriction and parent_restriction.get_children() and parent_restriction.get_children()[0].tag == 'pattern':
                        return rf"{parent_restriction.get_children()[0].get_attributes()['value']}"

        def translate_pattern(pattern_):
            if pattern_ == "[\i-[:]][\c-[:]]*":
                return rf"{xml_name_first_character_without_colon}{name_character_without_colon}*"
            pattern_ = pattern_.replace('\c', name_character)
            pattern_ = pattern_.replace('\i', xml_name_first_character)
            return pattern_

        restriction = self.get_restriction()
        pattern = get_xsd_pattern(restriction)
        if pattern:
            return translate_pattern(pattern)
        else:
            return None

    def get_permitted(self):
        restriction = self.get_restriction()
        if restriction:
            enumerations = [child for child in restriction.get_children() if
                            child.tag == 'enumeration']
            return [enumeration.get_attributes()['value'] for enumeration in enumerations]

    def get_simple_content(self):
        for node in self.get_children():
            if node.tag == 'simpleContent':
                return node

    def get_simple_content_extension(self):
        for node in self.get_children():
            if node.tag == 'simpleContent':
                if node.get_children()[0].tag == 'extension':
                    return node.get_children()[0]

    def get_union(self):
        for node in self.get_children():
            if node.tag == 'union':
                return node

    def get_union_member_types(self):
        if self.get_union():
            return self.get_union().get_attributes()['memberTypes'].split(' ')

    def get_xsd(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            ET.dump(self.xml_element_tree_element)
            output = buf.getvalue()
        output = output.strip()
        output += '\n'
        return output

    def get_xsd_indicator(self):
        return self._xsd_indicator

    # ------------------
    # magic methods
    def __deepcopy__(self, copy_parent=False):
        def copy_et_element(el):
            output = ET.Element(el.tag, el.attrib)
            output.text = el.text
            return output
            # return copy.deepcopy(el)

        copied = self.__class__(xml_element_tree_element=copy_et_element(self.xml_element_tree_element))
        copied._tag = self.tag
        if copy_parent and self.get_parent():
            copied._parent = self.get_parent().__deepcopy__(copy_parent=True)
        for ch in self.get_children():
            copied.add_child(ch.__deepcopy__())
        return copied

    def __repr__(self):
        attrs = self.get_attributes()
        output = f"{self.__class__.__name__}(tag={self.tag}"
        if attrs:
            output += f", {' '.join([f'{attribute}={attrs[attribute]}' for attribute in attrs])})"
        else:
            output += ')'
        return output

    def __str__(self):
        return f"{self.__class__.__name__} {self.compact_repr}"


class XSDTreeElement:
    """
    Abstract class of all generated XSD Classes
    """
    XSD_TREE: Optional[XSDTree] = None
    _SEARCH_FOR_ELEMENT = ""
    _XSD_TREE = None

    @classmethod
    def get_xsd_tree(cls):
        if cls._XSD_TREE:
            return cls._XSD_TREE
        found_xsd_element = musicxml_xsd_et_root.find(cls._SEARCH_FOR_ELEMENT)
        if not found_xsd_element:
            return cls.XSD_TREE
        else:
            cls._XSD_TREE = XSDTree(found_xsd_element)
            return cls._XSD_TREE

    @classmethod
    def get_xsd(cls):
        return cls.get_xsd_tree().get_xsd()
