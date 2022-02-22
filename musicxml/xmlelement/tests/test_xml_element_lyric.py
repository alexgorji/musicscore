from unittest import TestCase

from musicxml.exceptions import XMLElementChildrenRequired
from musicxml.xmlelement.xmlelement import *


class TestXMLLyric(TestCase):
    def test_xml_lyric_humming_children_container_tree(self):
        """
        Test that xml lyric has an empty children container tree corresponding to its xsd complex type for managing its children.
        """
        lyric = XMLLyric()
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Choice@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=syllabic@minOccurs=0@maxOccurs=1
            Element@name=text@minOccurs=1@maxOccurs=1
            Sequence@minOccurs=0@maxOccurs=unbounded
                Sequence@minOccurs=0@maxOccurs=1
                    Element@name=elision@minOccurs=1@maxOccurs=1
                    Element@name=syllabic@minOccurs=0@maxOccurs=1
                Element@name=text@minOccurs=1@maxOccurs=1
            Element@name=extend@minOccurs=0@maxOccurs=1
        Element@name=extend@minOccurs=1@maxOccurs=1
        Element@name=laughing@minOccurs=1@maxOccurs=1
        Element@name=humming@minOccurs=1@maxOccurs=1
    Element@name=end-line@minOccurs=0@maxOccurs=1
    Element@name=end-paragraph@minOccurs=0@maxOccurs=1
    Group@name=editorial@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Group@name=footnote@minOccurs=0@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=footnote@minOccurs=1@maxOccurs=1
            Group@name=level@minOccurs=0@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=level@minOccurs=1@maxOccurs=1
"""
        assert lyric.child_container_tree.tree_representation() == expected
        with self.assertRaises(XMLElementChildrenRequired) as err:
            lyric.to_string()
        assert err.exception.args[0] == "XMLLyric requires at least following children: ('XMLText', 'XMLExtend', 'XMLLaughing', " \
                                        "'XMLHumming')"
        lyric.add_child(XMLHumming())
        expected = """<lyric>
  <humming />
</lyric>
"""
        assert lyric.to_string() == expected
        footnote = lyric.add_child(XMLFootnote('something'))
        level = lyric.add_child(XMLLevel('1'))
        # with self.assertRaises(XMLElementValueRequiredError) as err:
        #     lyric.to_string()
        # assert err.exception.args[0] == 'XMLFootnote requires a value.'
        footnote.value_ = 'some footnote'
        # with self.assertRaises(XMLElementValueRequiredError) as err:
        #     lyric.to_string()
        # assert err.exception.args[0] == 'XMLLevel requires a value.'
        with self.assertRaises(TypeError) as err:
            level.value_ = 3
        assert err.exception.args[0] == "XMLLevel: XSDSimpleTypeString's value '3' can only be of types ['str'] not int."

        level.value_ = '3'
        expected = """<lyric>
  <humming />
  <footnote>some footnote</footnote>
  <level>3</level>
</lyric>
"""
        assert lyric.to_string() == expected
