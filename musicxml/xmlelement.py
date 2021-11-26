import xml.etree.ElementTree as ET
import re


class XMLSimpleType:
    """
    Abstract Class for all SimpleType classes
    """


class XMLElement:
    def __init__(self, xml_element):
        self._xml_element = None
        self._xml_element_class_name = None
        self._tag = None
        self._namespace = None
        self.xml_element = xml_element

    def get_doc(self):
        to_be_found = f"./{self.namespace}annotation/{self.namespace}documentation"
        return self.xml_element.find(to_be_found).text

    @property
    def xml_element(self):
        return self._xml_element

    @xml_element.setter
    def xml_element(self, value):
        if not isinstance(value, ET.Element):
            raise TypeError(f"XMLElement must be initiated with an xml_element of type {type(ET.Element)} not "
                            f"{type(value)}")
        self._xml_element = value

    @property
    def class_name(self):
        if self._xml_element_class_name is None:
            self._xml_element_class_name = self._get_element_class_name(self.xml_element)
        return self._xml_element_class_name

    @property
    def tag(self):
        if not self._tag:
            self._tag = re.match(r'({.*})(.*)', self.xml_element.tag).group(2)
        return self._tag

    @property
    def namespace(self):
        if not self._namespace:
            self._namespace = re.match(r'({.*})(.*)', self.xml_element.tag).group(1)
        return self._namespace

    def _get_element_class_name(self, xml_element):
        tag = self.tag[:]
        tag = tag[0].upper() + tag[1:]

        name = 'XML' + f'{tag}'
        name += ''.join([partial.capitalize() for partial in xml_element.attrib['name'].split('-')])
        return name


with open("../musicxml_4_0.xsd") as file:
    xmltree = ET.parse(file)

root = xmltree.getroot()

ns = '{http://www.w3.org/2001/XMLSchema}'

simple_type_elements = root.findall(f"{ns}simpleType")

for simple_type in simple_type_elements:
    xml_element = XMLElement(simple_type)
    attributes = {'__doc__': xml_element.get_doc()}
    if xml_element.tag == 'simpleType':
        parent_class = 'XMLSimpleType'
    else:
        raise NotImplemented()
    class_name = xml_element.class_name
    exec(f"{class_name} = type('{class_name}', ({parent_class},), {attributes})")
