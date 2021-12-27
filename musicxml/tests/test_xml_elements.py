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
