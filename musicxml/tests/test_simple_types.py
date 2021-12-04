import importlib
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest import TestCase

from musicxml.types.simpletype import XMLSimpleType, XMLSimpleTypeAboveBelow
from musicxml.xmlelement import XMLElementTreeElement

xsd_path = Path(__file__).parent.parent / 'musicxml_4_0.xsd'


class TestSimpleTypes(TestCase):
    def setUp(self) -> None:
        with open(xsd_path) as file:
            xmltree = ET.parse(file)
        self.root = xmltree.getroot()
        ns = '{http://www.w3.org/2001/XMLSchema}'
        self.all_simple_type_elements = [XMLElementTreeElement(simpletype) for simpletype in
                                         self.root.findall(f"{ns}simpleType")]

    def test_simple_type_XMLElement_generator_xsd_snippet(self):
        """
        Test that the instance of with XMLElementGenerator generated class can show corresponding xsd snippet and
        show its version
        """
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
        assert isinstance(XMLSimpleTypeAboveBelow, type(XMLSimpleType))
        assert XMLSimpleTypeAboveBelow.__doc__ == 'The above-below type is used to indicate whether one element appears ' \
                                                  'above or below another element.'

    def test_simple_type_xsd_is_converted_to_classes(self):
        for simple_type in self.all_simple_type_elements:
            module = importlib.import_module('musicxml.types.simpletype')
            my_class = getattr(module, simple_type.class_name)
            assert simple_type.class_name == my_class.__name__

    def test_simple_type_all_bases(self):
        """
        Test that simple types base attribute in restriction are converted to parent classes
        """
        all_restriction_bases = []
        for simpletype in self.all_simple_type_elements:
            if simpletype.base_class_names not in all_restriction_bases:
                all_restriction_bases.append(simpletype.base_class_names)
        print(all_restriction_bases)

        # for simple_type in self.all_simple_type_elements:
        #     module = importlib.import_module('musicxml.types.simpletype')
        #     my_class = getattr(module, simple_type.class_name)
        #     assert isinstance(my_class, simple_type.base_classes)

    def test_simple_type_validator_from_restriction(self):
        """
        Test that the instance of with XMLElementGenerator generated class has a validator corresponding to its xsd
        restriction
        """
        XMLSimpleTypeAboveBelow('above')
        XMLSimpleTypeAboveBelow('below')
        with self.assertRaises(TypeError):
            XMLSimpleTypeAboveBelow('side')
        with self.assertRaises(TypeError):
            XMLSimpleTypeAboveBelow(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeAboveBelow(1)
