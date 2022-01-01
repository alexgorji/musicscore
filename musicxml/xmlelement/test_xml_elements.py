from unittest import TestCase

from musicxml.exceptions import XMLElementChildrenRequired, XMLElementValueRequiredError
from .xmlelement import XMLElement
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdsimpletype import *


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

    def test_element_name(self):
        el = XMLElement(type_=XSDComplexTypeOffset, value=-2)
        assert el.name == 'offset'
        with self.assertRaises(ValueError):
            XMLElement(type_=XSDComplexTypeOffset, value=-2, name='something')
        el = XMLElement(type_=XSDSimpleTypeString, name='something')
        assert el.name == 'something'
        with self.assertRaises(ValueError):
            XMLElement(type_=XSDSimpleTypeString, value=-2)

    def test_element_with_simple_type(self):
        """
        <xs:element name="elevation" type="rotation-degrees" minOccurs="0">
            <xs:annotation>
                <xs:documentation>The elevation and pan elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For elevation, 0 is level with the listener, 90 is directly above, and -90 is directly below.</xs:documentation>
            </xs:annotation>
        </xs:element>
        """
        el = XMLElement(type_=XSDSimpleTypeRotationDegrees, name='elevation',
                        doc='The elevation and pan elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For elevation, 0 is level with the listener, 90 is directly above, and -90 is directly below.')
        with self.assertRaises(TypeError):
            el.value = 'something'
        with self.assertRaises(ValueError):
            el.value = 200
        with self.assertRaises(XMLElementValueRequiredError):
            el.to_string()

        el.value = 170
        assert el.to_string() == '<rotation-degrees>170</rotation-degrees>'
        assert el.__doc__ == 'The elevation and pan elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For elevation, 0 is level with the listener, 90 is directly above, and -90 is directly below.'

    def test_element_empty(self):
        """
        Test that empty complex type is created properly
        """
        el = XMLElement(type_=XSDComplexTypeEmpty)
        assert el.to_string() == '<empty />'

    def test_sequence_indicator(self):
        """
        Test that a sequence indicator with only elements as children can verify the behavior of its corresponding element
        """
        """
        complexType@name=pitch
        sequence
            element@name=step@type=step
            element@name=alter@type=semitones@minOccurs=0
            element@name=octave@type=octave
        """

        """
        Element Pitch must have one and only one child element step and one and only one child element octave. It can have only one child 
        alter. The sequence order will be automatically set according to the sequence (step, alter, octave)
        """

        el = XMLElement(XSDComplexTypePitch)
        with self.assertRaises(XMLElementChildrenRequired):
            el.to_string()
