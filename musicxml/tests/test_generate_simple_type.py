import xml.etree.ElementTree as ET
from pathlib import Path
from unittest import TestCase

from musicxml.xmlelement import XMLSimpleType

xsd_path = Path(__file__).parent.parent / 'musicxml_4_0.xsd'


class TestGenerateSimpleType(TestCase):
    def setUp(self) -> None:
        with open(xsd_path) as file:
            xmltree = ET.parse(file)
        self.root = xmltree.getroot()
        ns = '{http://www.w3.org/2001/XMLSchema}'
        self.simple_type_element = self.root.find(f"{ns}simpleType[@name='above-below']")

    def test_simple_type_XMLElement_generator_xsd_snippet(self):
        """
        Test that the instance of with XMLElementGenerator generated class can show corresponding xsd snippet and
        show its version
        """
        from musicxml.xmlelement import XMLSimpleTypeAboveBelow
        expected = """<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="above-below">
		<xs:annotation>
			<xs:documentation>The above-below type is used to indicate whether one element appears above or below another element.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="above" />
			<xs:enumeration value="below" />
		</xs:restriction>
	</xs:simpleType>
"""
        assert XMLSimpleTypeAboveBelow.get_xsd() == expected

    def test_simple_type_XMLElement_generator_doc_string_from_annotation(self):
        """
        Test that the instance of with with XMLElementGenerator generated class has a documentation string
        matching its xsd annotation
        """
        from musicxml.xmlelement import XMLSimpleTypeAboveBelow
        assert isinstance(XMLSimpleTypeAboveBelow, type(XMLSimpleType))
        assert XMLSimpleTypeAboveBelow.__doc__ == 'The above-below type is used to indicate whether one element appears ' \
                                                  'above or below another element.'

    def test_simple_type_XMLElement_generator_validator_from_restriction(self):
        """
        Test that the instance of with XMLElementGenerator generated class has a validator corresponding to its xsd
        restriction
        """
        self.fail('Incomplete')
