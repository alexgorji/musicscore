import io
import re
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout

from musicxml.util.helperfunctions import cap_first
from tree.tree import TreePresentation


class XSDTree(TreePresentation):
    """
    XSDTree gets an xml.etree.ElementTree.Element by initiation as its xml_element_tree_element property and
    prepares all needed information for generating an MusicXMLElement class
    """

    def __init__(self, xml_element_tree_element, parent=None):
        self._children = []
        self._namespace = None
        self._tag = None
        self._xml_element_tree_element = None
        self._xml_element_class_name = None
        self._parent = parent

        self.xml_element_tree_element = xml_element_tree_element

    # ------------------
    # private properties

    # ------------------
    # private methods

    def _get_element_class_name(self):
        tag = cap_first(self.tag)

        name = 'XML' + f'{tag}'
        name += ''.join([cap_first(partial) for partial in self.name.split('-')])
        return name

    def _populate_children(self):
        self._children = [XSDTree(node, parent=self) for node in
                          self.xml_element_tree_element.findall('./')]

    # ------------------
    # public properties
    @property
    def base_class_names(self):
        def convert_name(name):
            try:
                name = name.split(':')[1]
            except IndexError:
                pass
            name = cap_first(name)
            name = ''.join([cap_first(partial) for partial in name.split('-')])
            name = 'XMLSimpleType' + name
            return name

        if self.get_restriction():
            base = self.get_restriction().get_attributes()['base']
            return [convert_name(base)]
        elif self.get_union_member_types():
            return [convert_name(type_) for type_ in self.get_union_member_types()]
        else:
            raise AttributeError(f"{self} has no restriction with base attribute or union with memberTypes.")

    @property
    def class_name(self):
        if self._xml_element_class_name is None:
            self._xml_element_class_name = self._get_element_class_name()
        return self._xml_element_class_name

    @property
    def compact_repr(self):
        attrs = self.get_attributes()
        return f"{self.tag}{''.join([f'@{attribute}={attrs[attribute]}' for attribute in attrs])}"

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
        return self._xml_element_tree_element

    @xml_element_tree_element.setter
    def xml_element_tree_element(self, value):
        if not isinstance(value, ET.Element):
            raise TypeError(
                f"XSDTree must be initiated with an xml_element_tree_element of type xml.etree.ElementTree.Element not "
                f"{type(value)}")
        self._xml_element_tree_element = value

    # ------------------
    # public methods
    def get_attributes(self):
        return self.xml_element_tree_element.attrib

    def get_children(self):
        if not self._children:
            self._populate_children()
        return self._children

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
