from unittest import TestCase

from musicxml.exceptions import XMLElementChildrenRequired
from musicxml.xmlelement.xmlelement import *


class TestXMLLyric(TestCase):
    def test_xml_lyric_children_container_tree(self):
        """
        Test that xml lyric has an empty children container tree corresponding to its xsd complex type for managing its children.
        """
        lyric = XMLLyric()
        expected = """Sequence
    Choice
        Sequence
            'Element@name=syllabic@minOccurs=0'
            'Element@name=text'
            'Sequence@minOccurs=0@maxOccurs=unbounded'
                'Sequence@minOccurs=0'
                    'Element@name=elision'
                    'Element@name=syllabic@minOccurs=0'
                'Element@name=text'
            'Element@name=extend'
            'Element@name=laughing'
            'Element@name=humming'
        """
        assert lyric.children_container_tree.tree_repr == expected

    def test_xml_lyric_required_child(self):
        """
        Test lyric needs at least one child
        """
        lyric = XMLLyric()
        with self.assertRaises(XMLElementChildrenRequired):
            lyric.to_string()

        lyric.add_child(XMLHumming)
        lyric.to_string()

        lyric = XMLLyric()
        lyric.add_child(XMLLaughings)
        lyric.to_string()

        lyric = XMLLyric()
        lyric.add_child(XMLExtend)
        lyric.to_string()

        lyric = XMLLyric()
        lyric.add_child(XMLText)
        lyric.to_string()
