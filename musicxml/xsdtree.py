import io
import re
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout

from musicxml.util.core import cap_first, convert_to_xsd_class_name
from tree.tree import TreePresentation

"""
XSD = XML Schema Definition
"""


class XSDTree(TreePresentation):
    """
    XSDTree gets a xml.etree.ElementTree.Element by initiation as its xsd_element_tree_element property and
    prepares all needed information for generating a XSDElement class (XSDElement can be XSDSimpleType, XSDComplexType, XMLGroup,
    XMLAttribute and XMLAttributeGroup)
    """

    def __init__(self, xsd_element_tree_element, parent=None):
        self._children = []
        self._namespace = None
        self._tag = None
        self._xsd_element_tree_element = None
        self._xml_tree_class_name = None
        self._parent = parent

        self.xsd_element_tree_element = xsd_element_tree_element

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
        self._children = [XSDTree(node, parent=self) for node in
                          self.xsd_element_tree_element.findall('./')]

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
                return [convert_to_xsd_class_name(type_) for type_ in self.get_union_member_types()]
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
            return self.xsd_element_tree_element.attrib['name']
        except KeyError:
            return

    @property
    def namespace(self):
        if not self._namespace:
            self._namespace = re.match(r'({.*})(.*)', self.xsd_element_tree_element.tag).group(1)
        return self._namespace

    @property
    def tag(self):
        if not self._tag:
            self._tag = re.match(r'({.*})(.*)', self.xsd_element_tree_element.tag).group(2)
        return self._tag

    @property
    def text(self):
        return self.xsd_element_tree_element.text

    @property
    def xsd_element_tree_element(self):
        return self._xsd_element_tree_element

    @xsd_element_tree_element.setter
    def xsd_element_tree_element(self, value):
        if not isinstance(value, ET.Element):
            raise TypeError(
                f"XSDTree must be initiated with an xsd_element_tree_element of type xml.etree.ElementTree.Element not "
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
        return self.xsd_element_tree_element.attrib

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
        for node in self.traverse():
            if node.tag == 'documentation':
                return node.text

    def get_parent(self):
        return self._parent

    def get_restriction(self):
        for node in self.get_children():
            if node.tag == 'restriction':
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
            ET.dump(self.xsd_element_tree_element)
            output = buf.getvalue()
        output = output.strip()
        output += '\n'
        return output

    # ------------------
    # magic methods

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


class XSDElement:
    """
    Abstract class of all generated XSD Classes
    """
    XSD_TREE = None

    @classmethod
    def get_xsd(cls):
        return cls.XSD_TREE.get_xsd()
