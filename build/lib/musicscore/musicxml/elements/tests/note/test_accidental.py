from musicscore.musicxml.elements.note import Note, Grace, Duration, Beam, Tie, Type, Lyric, Accidental
from musicscore.musicxml.elements.fullnote import Chord, Pitch, DisplayStep, DisplayOctave, Rest, Step, Octave, Alter

from unittest import TestCase


class TestAccidentalDTD(TestCase):
    def setUp(self):
        self.note = Note()
        self.note.add_child(Duration())
        pitch = self.note.add_child(Pitch())
        pitch.add_child(Alter(1))
        self.note.add_child(Accidental('sharp'))

    def test_accidental(self):
        result = '''<note>
  <pitch>
    <step>C</step>
    <alter>1</alter>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <accidental>sharp</accidental>
</note>
'''
        self.assertEqual(self.note.to_string(), result)
