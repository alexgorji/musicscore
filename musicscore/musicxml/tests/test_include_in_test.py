from unittest import TestCase
from musicscore.musicxml.elements.xml_note import XMLNote, XMLPitch, XMLLyricGroup, XMLLyric


class TestMode(TestCase):
    def setUp(self):
        self.xml_note = XMLNote(event=XMLPitch('E', 2, 3), duration=2)
        self.xml_note.lyric = XMLLyricGroup()
        self.xml_note.lyric.add_sibling(XMLLyric('lyric 1'))
        self.xml_note.lyric.add_sibling(XMLLyric('lyric 2'))
        self.xml_note.duration = 10

    def test_include_in_test(self):
        with self.assertWarns(Warning):
            self.xml_note.include_in_test = False
        self.xml_note.test_mode = False
        self.xml_note.event.include_in_test = False
        self.xml_note.event.alter.include_in_test = True
        self.xml_note.lyric[0].include_in_test = False
        result = '''<note>
  <duration>10</duration>
  <lyric>lyric 2</lyric>
</note>
'''
        self.assertEqual(self.xml_note.to_string(), result)
