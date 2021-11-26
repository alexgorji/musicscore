from unittest import TestCase
import xml.etree.ElementTree as ET

from musicxml.xmlelement import XMLElement, XMLSimpleType


class TestXMLElement(TestCase):
    def setUp(self) -> None:
        with open("../musicxml_4_0.xsd") as file:
            xmltree = ET.parse(file)
        self.root = xmltree.getroot()
        ns = '{http://www.w3.org/2001/XMLSchema}'
        self.simple_type_element = self.root.find(f"{ns}simpleType[@name='above-below']")

    def test_self_simple_type_element(self):
        assert self.simple_type_element.tag == '{http://www.w3.org/2001/XMLSchema}simpleType'
        assert self.simple_type_element.attrib['name'] == 'above-below'

    def test_xml_property(self):
        """
        Test that a XMLElementGenerator must get an xml element
        :return: 
        """""
        with self.assertRaises(TypeError):
            XMLElement()
        with self.assertRaises(TypeError):
            XMLElement('Naja')

        xml_element = XMLElement(self.simple_type_element)
        assert isinstance(xml_element.xml_element, ET.Element)

    def test_xml_element_tag(self):
        xml_element = XMLElement(self.simple_type_element)
        assert xml_element.tag == 'simpleType'

    def test_xml_element_class_name(self):
        xml_element = XMLElement(self.simple_type_element)
        assert xml_element.class_name == 'XMLSimpleTypeAboveBelow'

    def test_xml_element_class(self):
        from musicxml.xmlelement import XMLSimpleTypeAboveBelow

    def test_get_doc(self):
        xml_element = XMLElement(self.simple_type_element)
        assert xml_element.get_doc() == 'The above-below type is used to indicate whether one element appears above or below another element.'


class TestGenerateSimpleType(TestCase):
    def setUp(self) -> None:
        with open("../musicxml_4_0.xsd") as file:
            xmltree = ET.parse(file)
        self.root = xmltree.getroot()
        ns = '{http://www.w3.org/2001/XMLSchema}'
        self.simple_type_element = self.root.find(f"{ns}simpleType[@name='above-below']")

    def test_XMLElement_generator_for_simple_type_with_annotation(self):
        """
        Test if the XMLElementGenerator class can generate a XMLSimpleType class with documentation string
        """
        from musicxml.xmlelement import XMLSimpleTypeAboveBelow
        assert isinstance(XMLSimpleTypeAboveBelow, type(XMLSimpleType))
        assert XMLSimpleTypeAboveBelow.__doc__ == 'The above-below type is used to indicate whether one element appears above or below another element.'
