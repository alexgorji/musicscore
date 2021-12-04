import importlib

from musicxml.types.simpletype import XMLSimpleType, XMLSimpleTypeAboveBelow
from musicxml.util.helperclasses import MusicXmlTestCase


class TestSimpleTypes(MusicXmlTestCase):

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
            simple_type_class = getattr(module, simple_type.class_name)
            assert simple_type.class_name == simple_type_class.__name__

    def test_base_classes_are_implemented(self):
        for simple_type in self.all_simple_type_elements:
            module = importlib.import_module('musicxml.types.simpletype')
            simpletype_class = getattr(module, simple_type.class_name)
            mro = simpletype_class.__mro__
            for base_class_name in simple_type.base_class_names:
                base_class = getattr(module, base_class_name)
                assert base_class in mro

    def test_simple_type_validator_from_restriction(self):
        """
        Test that the instance of with XMLElementGenerator generated class has a validator corresponding to its xsd
        restriction
        """
        with self.assertRaises(TypeError):
            XMLSimpleTypeAboveBelow(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeAboveBelow(1)

        XMLSimpleTypeAboveBelow('above')
        XMLSimpleTypeAboveBelow('below')
        with self.assertRaises(TypeError):
            XMLSimpleTypeAboveBelow('side')
