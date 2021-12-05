import importlib

from musicxml.types.simpletype import XMLSimpleType, XMLSimpleTypeAboveBelow, XMLSimpleTypeNumberOrNormal, \
    XMLSimpleTypePositiveIntegerOrEmpty, XMLSimpleTypeNonNegativeDecimal, XMLSimpleTypeDecimal, XMLSimpleTypeInteger, \
    XMLSimpleTypeNonNegativeInteger, XMLSimpleTypePositiveInteger, XMLSimpleTypeString, XMLSimpleTypeToken, \
    XMLSimpleTypeNMTOKEN, XMLSimpleTypeDate
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

    def test_xs_integer(self):
        with self.assertRaises(TypeError):
            XMLSimpleTypeInteger(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeInteger('string')
        with self.assertRaises(TypeError):
            XMLSimpleTypeInteger(1.4)
        XMLSimpleTypeInteger(0)
        XMLSimpleTypeInteger(-4)
        XMLSimpleTypeInteger(3)

    def test_xs_none_negative_integer(self):
        with self.assertRaises(TypeError):
            XMLSimpleTypeNonNegativeInteger(1.4)
        with self.assertRaises(TypeError):
            XMLSimpleTypeNonNegativeInteger(-1.4)
        with self.assertRaises(ValueError):
            XMLSimpleTypeNonNegativeInteger(-4)
        XMLSimpleTypeNonNegativeInteger(0)
        XMLSimpleTypeNonNegativeInteger(3)

    def test_xs_positive_integer(self):
        with self.assertRaises(TypeError):
            XMLSimpleTypePositiveInteger(1.4)
        with self.assertRaises(TypeError):
            XMLSimpleTypePositiveInteger(-1.4)
        with self.assertRaises(ValueError):
            XMLSimpleTypePositiveInteger(-4)
        with self.assertRaises(ValueError):
            XMLSimpleTypePositiveInteger(0)
        XMLSimpleTypePositiveInteger(3)

    def test_xs_decimal(self):
        with self.assertRaises(TypeError):
            XMLSimpleTypeDecimal(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeDecimal('string')
        XMLSimpleTypeDecimal(1.4)
        XMLSimpleTypeDecimal(0)
        XMLSimpleTypeDecimal(-4)

    def test_non_negative_decimal(self):
        with self.assertRaises(TypeError):
            XMLSimpleTypeNonNegativeDecimal(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeNonNegativeDecimal('string')
        XMLSimpleTypeNonNegativeDecimal(1.4)
        XMLSimpleTypeNonNegativeDecimal(0)
        with self.assertRaises(ValueError):
            XMLSimpleTypeNonNegativeDecimal(-4)
        with self.assertRaises(ValueError):
            XMLSimpleTypeNonNegativeDecimal(-1.4)

    def test_xs_string(self):
        with self.assertRaises(TypeError):
            XMLSimpleTypeString(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeString(1)
        with self.assertRaises(TypeError):
            XMLSimpleTypeString(1.5)
        XMLSimpleTypeString("")
        XMLSimpleTypeString("hello")

    def test_xs_token(self):
        with self.assertRaises(TypeError):
            XMLSimpleTypeToken(1)
        XMLSimpleTypeString("Hello Alfons")
        assert XMLSimpleTypeToken("Hello\tAlfons").value == "Hello Alfons"
        assert XMLSimpleTypeToken("Hello\rAlfons").value == "Hello Alfons"
        assert XMLSimpleTypeToken("Hello\nAlfons").value == "Hello Alfons"
        assert XMLSimpleTypeToken("Hello    Alfons").value == "Hello Alfons"
        assert XMLSimpleTypeToken("Hello\n  Alfons").value == "Hello Alfons"

    def test_xs_NMTOKEN(self):
        with self.assertRaises(TypeError):
            XMLSimpleTypeNMTOKEN(1)
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello\tAlfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello,Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello;Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello%Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello|Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello'Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello?Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("HelloAlfons!")
        XMLSimpleTypeNMTOKEN("Hello_Alfons")
        XMLSimpleTypeNMTOKEN("HeL1.o")
        XMLSimpleTypeNMTOKEN("HeL1:._-o")
        XMLSimpleTypeNMTOKEN("ÖÜöüäÄ:._-o")

    def test_xs_date(self):
        XMLSimpleTypeDate('1982-11-23+07:00')
        XMLSimpleTypeDate('1982-11-23')
        with self.assertRaises(ValueError):
            XMLSimpleTypeDate('1982-21-23')
        with self.assertRaises(ValueError):
            XMLSimpleTypeDate('19822123')
        with self.assertRaises(TypeError):
            XMLSimpleTypeDate(19821223)

    def test_simple_type_number_or_normal(self):
        """
        Test if the intern simple format of restriction is applied
        """
        with self.assertRaises(TypeError):
            XMLSimpleTypeNumberOrNormal('something')
        XMLSimpleTypeNumberOrNormal(1)
        XMLSimpleTypeNumberOrNormal(1.5)
        XMLSimpleTypeNumberOrNormal(-1)
        XMLSimpleTypeNumberOrNormal(-1.5)
        XMLSimpleTypeNumberOrNormal(0)
        XMLSimpleTypeNumberOrNormal('normal')

    def test_simple_type_positive_integer_or_empty(self):
        """
        Test if the intern simple format of restriction is applied
        """
        with self.assertRaises(TypeError):
            XMLSimpleTypePositiveIntegerOrEmpty('something')
        with self.assertRaises(TypeError):
            XMLSimpleTypePositiveIntegerOrEmpty(-1.5)
        with self.assertRaises(TypeError):
            XMLSimpleTypePositiveIntegerOrEmpty(1.5)
        with self.assertRaises(ValueError):
            XMLSimpleTypePositiveIntegerOrEmpty(-1)
        with self.assertRaises(ValueError):
            XMLSimpleTypePositiveIntegerOrEmpty(0)
        XMLSimpleTypePositiveIntegerOrEmpty(1)
        XMLSimpleTypeNumberOrNormal('')

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
        with self.assertRaises(ValueError):
            XMLSimpleTypeAboveBelow('side')
