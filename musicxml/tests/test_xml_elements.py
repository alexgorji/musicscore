from unittest import TestCase

from musicxml.xmlelement import XMLElement
from musicxml.types.complextype import *


class TestXMLElements(TestCase):
    def test_element_simple_content(self):
        """
        Test if complex types with a simple context (extension of a simple type) work properly in an XMLElement.
        A simple example is

        complexType@name=offset

        simpleContent
            extension@base=divisions
                attribute@name=sound@type=yes-no
        """
        el = XMLElement(type_=XSDComplexTypeOffset, value=-2, attributes={'sound': 'yes'})
        assert el.to_string() == '<offset sound="yes">-2</offset>'
        with self.assertRaises(TypeError):
            XMLElement(type_=XSDComplexTypeOffset, value='wrong', attributes={'sound': 'yes'})

        with self.assertRaises(TypeError):
            XMLElement(type_=XSDComplexTypeOffset, value=-2, attributes={'sound': 3})

        with self.assertRaises(ValueError):
            XMLElement(type_=XSDComplexTypeOffset, value=-2, attributes={'sound': 'maybe'})

    def test_element_empty(self):
        """
        Test that empty complex type is created properly
        """
        el = XMLElement(type_=XSDComplexTypeEmpty)
        assert el.to_string() == '<empty />'