from unittest import TestCase
from musicscore.musicxml.elements.xml_note import XMLNote, XMLPitch, XMLLyric


class TestMode(TestCase):
    def setUp(self):
        self.xml_note = XMLNote(event=XMLPitch('E', 2, 3), duration=2)
        self.xml_note.add_child(XMLLyric('lyric 1'))
        self.xml_note.add_child(XMLLyric('lyric 2'))

        self.xml_note.duration = 10

    def test_mode(self):
        self.xml_note.test_mode = True
        result = '''<note>
  <pitch>
    <step/>
    <alter/>
    <octave/>
  </pitch>
  <duration/>
  <lyric/>
  <lyric/>
</note>
'''
        self.assertEqual(self.xml_note.to_string(), result)
        self.xml_note.test_mode = False
        result = '''<note>
  <pitch>
    <step>E</step>
    <alter>2</alter>
    <octave>3</octave>
  </pitch>
  <duration>10</duration>
  <lyric>lyric 1</lyric>
  <lyric>lyric 2</lyric>
</note>
'''
        self.assertEqual(self.xml_note.to_string(), result)

