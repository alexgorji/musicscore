from musicscore.musicxml.elements.note import Note, Grace, Duration, Beam, Tie, Type, Lyric
from musicscore.musicxml.elements.fullnote import Chord, Pitch, DisplayStep, DisplayOctave, Rest
from musicscore.dtd.dtd import ChildOccurrenceDTDConflict, ChildTypeDTDConflict, ChildIsNotOptional
from unittest import TestCase


class TestNoteBeamDTD(TestCase):
    def setUp(self):
        self.note = Note()
        self.note.add_child(Pitch())
        self.note.add_child(Duration())

    def test_note_beam(self):
        self.note.add_child(Beam('begin', number=2))
        result = '''<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <beam number="2">begin</beam>
</note>
'''
        self.assertEqual(self.note.to_string(), result)