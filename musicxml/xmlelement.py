import io
import re
import xml.etree.ElementTree as ET
from abc import ABC
from contextlib import redirect_stdout
from pathlib import Path

from tree.tree import TreePresentation

xsd_path = Path(__file__).parent / 'musicxml_4_0.xsd'


class MusicXMLElement(ABC):
    """
    Abstract class as root of all generated XML Classes
    """

    @classmethod
    def get_xsd(cls):
        return cls.XML_ET_ELEMENT.get_xsd()


class XMLSimpleType(MusicXMLElement):
    """
    Parent Class for all SimpleType classes
    """


class XMLElementTreeElement(TreePresentation):
    """
    XMLElementTreeElement gets an xml.etree.ElementTree.Element by initiation as its xml_element_tree_element property and
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
        tag = self.tag[:]
        tag = tag[0].upper() + tag[1:]

        name = 'XML' + f'{tag}'
        name += ''.join([partial.capitalize() for partial in self.name.split('-')])
        return name

    def _populate_children(self):
        self._children = [XMLElementTreeElement(node, parent=self) for node in
                          self.xml_element_tree_element.findall('./')]

    # ------------------
    # public properties

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
    def xml_element_tree_element(self):
        return self._xml_element_tree_element

    @xml_element_tree_element.setter
    def xml_element_tree_element(self, value):
        if not isinstance(value, ET.Element):
            raise TypeError(
                f"XMLElementTreeElement must be initiated with an xml_element_tree_element of type xml.etree.ElementTree.Element not "
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
        to_be_found = f"./{self.namespace}annotation/{self.namespace}documentation"
        return self.xml_element_tree_element.find(to_be_found).text

    def get_parent(self):
        return self._parent

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


with open(xsd_path) as file:
    xmltree = ET.parse(file)

root = xmltree.getroot()

ns = '{http://www.w3.org/2001/XMLSchema}'

simple_type_elements = root.findall(f"{ns}simpleType")

for simple_type in simple_type_elements:
    xml_element_tree_element = XMLElementTreeElement(simple_type)
    attributes = "{'__doc__': xml_element_tree_element.get_doc(), 'XML_ET_ELEMENT':xml_element_tree_element}"
    if xml_element_tree_element.tag == 'simpleType':
        parent_class = 'XMLSimpleType'
    else:
        raise NotImplemented()
    class_name = xml_element_tree_element.class_name
    exec(f"{class_name} = type('{class_name}', ({parent_class},), {attributes})")
