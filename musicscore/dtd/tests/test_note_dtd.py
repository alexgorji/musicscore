from musicscore.dtd.note import Note, FullNote, Grace, Duration, Beam, Tie, Chord, Pitch, Rest, DurationGroup
from musicscore.dtd.dtd import ChildOccurrenceDTDConflict, ChildTypeDTDConflict, ChildIsNotOptional
from unittest import TestCase


class TestNoteDTD(TestCase):
    def setUp(self):
        self.note = Note()

    def test_add_child_type(self):
        self.note.add_child(FullNote())
        self.note.add_child(Grace())
        with self.assertRaises(ChildTypeDTDConflict):
            self.note.add_child(Duration(1))

    def test_add_child_max_occurrence(self):
        self.note.add_child(FullNote())
        with self.assertRaises(ChildOccurrenceDTDConflict):
            self.note.add_child(FullNote())

    def test_close(self):
        self.note.add_child(FullNote())
        self.note.add_child(Grace())
        self.note.close()
        result = ['Grace', 'FullNote', 'Instrument', 'EditorialVoice', 'Type', 'Dot', 'Accidental', 'TimeModification',
                  'Stem', 'Notehead', 'NotheadText', 'Staff', 'Beam', 'Notations', 'Lyric', 'Play']
        self.assertEqual([node.type_.__name__ for node in self.note._DTD.get_current_combination()], result)

        self.note.reset_children()
        self.note.add_child(FullNote())
        with self.assertRaises(ChildIsNotOptional):
            self.note.close()

    def test_sort_children(self):
        self.note.add_child(FullNote())
        self.note.add_child(Beam())
        self.note.add_child(Tie())
        self.note.add_child(Beam())
        self.note.add_child(DurationGroup())
        self.note.add_child(Tie())
        self.note.close()
        result = ['FullNote', 'DurationGroup', 'Tie', 'Tie', 'Beam', 'Beam']
        self.assertEqual([type(child).__name__ for child in self.note.get_children()], result)

    def test_full_note(self):
        full_note = FullNote()
        pitch = full_note.add_child(Pitch())
        chord = full_note.add_child(Chord())

        full_note.close()
        result = [chord, pitch]
        self.assertEqual(full_note.get_children(), result)
        with self.assertRaises(ChildTypeDTDConflict):
            full_note.add_child(Rest())

    def test_to_string(self):
        full_note = FullNote()
        full_note.add_child(Pitch())
        full_note.add_child(Chord())
        full_note.close()

        duration_group = DurationGroup()
        duration_group.add_child(Duration(1))

        self.note.add_child(full_note)
        self.note.add_child(Beam())
        self.note.add_child(Tie())
        self.note.add_child(Beam())
        self.note.add_child(duration_group)
        self.note.add_child(Tie())
        self.note.close()
        result = '''<note>
  <chord/>
  <pitch/>
  <duration>1</duration>
  <tie/>
  <tie/>
  <beam/>
  <beam/>
</note>
'''
        self.assertEqual(self.note.to_string(), result)
