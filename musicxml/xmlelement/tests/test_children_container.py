from unittest import TestCase

from musicxml.xmlelement.xmlelement import XMLChildContainerFactory, XMLChildContainer
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdelement import XSDElement
from musicxml.xsd.xsdindicators import XSDSequence, XSDChoice
from musicxml.xsd.xsdindicators import *
from musicxml.xsd.xsdtree import XSDTree
import xml.etree.ElementTree as ET


class TestChildrenContainer(TestCase):
    def setUp(self) -> None:
        element_xsd = '<xs:element xmlns:xs="http://www.w3.org/2001/XMLSchema" name="alter" type="semitones" minOccurs="0"/>'
        sequence_xsd = """
                <xs:sequence xmlns:xs="http://www.w3.org/2001/XMLSchema">
                    <xs:element name="step" type="step"/>
                    <xs:element name="alter" type="semitones" minOccurs="0"/>
                    <xs:element name="octave" type="octave"/>
                </xs:sequence>
        """
        choice_xsd = """<xs:choice xmlns:xs="http://www.w3.org/2001/XMLSchema">
                <xs:element name="pitch" type="pitch"/>
                <xs:element name="unpitched" type="unpitched"/>
                <xs:element name="rest" type="rest"/>
            </xs:choice>
        """
        self.element = XSDElement(XSDTree(ET.fromstring(element_xsd)))
        self.sequence = XSDSequence(XSDTree(ET.fromstring(sequence_xsd)))
        self.choice = XSDChoice(XSDTree(ET.fromstring(choice_xsd)))

    def test_children_container_node_type(self):
        """
        Test that an XMLChildContainer must initiate with an XSDElement, XSDGroup, XSDSequence or
        XSDChoice instances.
        """

        XMLChildContainer(self.element)
        XMLChildContainer(self.sequence)
        XMLChildContainer(self.choice)
        XMLChildContainer(XSDGroupEditorial())
        with self.assertRaises(TypeError):
            XMLChildContainer()
        with self.assertRaises(TypeError):
            XMLChildContainer(3)

    def test_children_container_compact_repr(self):
        """
        Test that children container has a compact_repr attribute
        """
        container = XMLChildContainer(self.element, min_occurrences=0)
        assert container.compact_repr == 'Element@name=alter@minOccurs=0@maxOccurs=1'
        container = XMLChildContainer(self.sequence)
        assert container.compact_repr == 'Sequence@minOccurs=1@maxOccurs=1'
        container = XMLChildContainer(self.choice, min_occurrences=0, max_occurrences='unbounded')
        assert container.compact_repr == 'Choice@minOccurs=0@maxOccurs=unbounded'
        container = XMLChildContainer(XSDGroupEditorial(), min_occurrences=1, max_occurrences=2)
        assert container.compact_repr == 'Group@name=editorial@minOccurs=1@maxOccurs=2'

    def test_children_container_factory_only_sequence(self):
        """
        Test a complex type with a simple sequence of elements
        """
        """
        complexType@name=pitch
            sequence
                element@name=step@type=step
                element@name=alter@type=semitones@minOccurs=0
                element@name=octave@type=octave
        """
        factory = XMLChildContainerFactory(complex_type=XSDComplexTypePitch)
        container = factory.get_child_container()
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Element@name=step@minOccurs=1@maxOccurs=1
    Element@name=alter@minOccurs=0@maxOccurs=1
    Element@name=octave@minOccurs=1@maxOccurs=1
"""
        assert container.tree_repr() == expected
