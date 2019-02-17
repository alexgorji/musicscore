from unittest import TestCase
from musicscore.musicxml.elements.xml_note import XMLNote, XMLPitch, XMLLyricGroup, XMLLyric, XMLType


class TestXMLNote(TestCase):
    def setUp(self):
        self.note = XMLNote(event=XMLPitch('E', 1, 2), duration=10)

    def test_to_string(self):
        self.note.chord = True
        result = '<note>\n  <chord/>\n  <pitch>\n    <step>E</step>\n    <alter>1</alter>\n    <octave>2</octave>\n  </pitch>\n  <duration>10</duration>\n</note>\n'
        self.assertEqual(self.note.to_string(), result)

    def test_lyrics(self):
        self.note.lyric = XMLLyricGroup()
        self.note.lyric.add_sibling(XMLLyric('lyric 1'))
        self.note.lyric.add_sibling(XMLLyric('lyric 2'))
        result = '<note>\n  <pitch>\n    <step>E</step>\n    <alter>1</alter>\n    <octave>2</octave>\n  </pitch>\n  <duration>10</duration>\n  <lyric>lyric 1</lyric>\n  <lyric>lyric 2</lyric>\n</note>\n'
        self.assertEqual(self.note.to_string(), result)

    def test_type(self):
        self.note.type = XMLType(value='quarter')
        result = '''<note>
  <pitch>
    <step>E</step>
    <alter>1</alter>
    <octave>2</octave>
  </pitch>
  <duration>10</duration>
  <type>quarter</type>
</note>
'''
        self.assertEqual(self.note.to_string(), result)
