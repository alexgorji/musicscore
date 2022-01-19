from unittest import TestCase

from musicxml.exceptions import XSDWrongAttribute
from musicxml.xmlelement.xmlelement import *

from musictree.musictree import Measure, Chord, MusicTree, Part


class TestMeasure(TestCase):
    def test_add_child(self):
        """
        Test that only a MusicTree element of type Chord can be added as child.
        """
        m = Measure()
        c = m.add_child(Chord())
        assert m.get_children() == [c]
        with self.assertRaises(TypeError):
            m.add_child(Measure())
        with self.assertRaises(TypeError):
            m.add_child(MusicTree())
        with self.assertRaises(TypeError):
            m.add_child(Part())

    def test_dot_operator(self):
        """
        Test that measures xml_object children can be attained with dot operator
        """
        m = Measure()
        assert isinstance(m.xml_attributes, XMLAttributes)
        assert isinstance(m.xml_attributes.xml_divisions, XMLDivisions)
        assert m.xml_attributes.xml_divisions.value == 1

    def test_attributes(self):
        """
        Test that a dot operator can directly reach the xml_object
        """
        m = Measure()
        m.xml_object.width = 5
        assert m.width == 5

        m.width = 7
        assert m.xml_object.width == 7

        with self.assertRaises(AttributeError):
            m.hello = 'bbb'
        m.xml_object.width = 10
        assert m.xml_object.width == 10
        assert m.width == 10

        m = Measure()
        m.width = 10
        assert m.width == 10
        assert m.xml_object.width == 10

    def test_create_child(self):
        """
        Test that a dot operator can create and add child if necessary
        """
        m = Measure(number='1')
        assert m.xml_barline is None
        m.xml_barline = XMLBarline()
        m.xml_barline.xml_bar_style = 'light-light'
        expected = """<measure number="1">
    <attributes>
        <divisions>1</divisions>
    </attributes>
    <barline>
        <bar-style>light-light</bar-style>
    </barline>
</measure>
"""
        assert m.xml_object.to_string() == expected
