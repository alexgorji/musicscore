from unittest import TestCase
from musicscore.musicxml.elements.xml_note import XMLNote, XMLPitch, XMLLyric, XMLType


class TestXMLNote(TestCase):
    def setUp(self):
        self.xml_note = XMLNote(event=XMLPitch('E', 1, 2), duration=10)

    # def test_to_string(self):
    #     self.xml_note.chord = True
    #     result = '<note>\n  <chord/>\n  <pitch>\n    <step>E</step>\n    <alter>1</alter>\n    <octave>2</octave>\n  </pitch>\n  <duration>10</duration>\n</note>\n'
    #     self.assertEqual(self.xml_note.to_string(), result)
    #
    # # def test_lyrics(self):
    # #     self.note.lyric = XMLLyricGroup()
    # #     self.note.lyric.add_sibling(XMLLyric('lyric 1'))
    # #     self.note.lyric.add_sibling(XMLLyric('lyric 2'))
    # #     result = '<note>\n  <pitch>\n    <step>E</step>\n    <alter>1</alter>\n    <octave>2</octave>\n  </pitch>\n  <duration>10</duration>\n  <lyric>lyric 1</lyric>\n  <lyric>lyric 2</lyric>\n</note>\n'
    # #     self.assertEqual(self.note.to_string(), result)

    def test_type(self):
        self.xml_note.add_child(XMLType(value='quarter'))
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
        self.assertEqual(self.xml_note.to_string(), result)

    def test_lyrics(self):
        self.xml_note.add_child(XMLLyric('lyric 1'))
        self.xml_note.add_child(XMLLyric('lyric 2'))
        result = '''<note>
  <pitch>
    <step>E</step>
    <alter>1</alter>
    <octave>2</octave>
  </pitch>
  <duration>10</duration>
  <lyric>lyric 1</lyric>
  <lyric>lyric 2</lyric>
</note>
'''
        self.assertEqual(self.xml_note.to_string(), result)
