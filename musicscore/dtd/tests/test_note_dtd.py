from musicscore.dtd.note import Note, FullNote, Grace, Duration, Beam, Tie
from musicscore.dtd.dtd import ChildOccurrenceDTDConflict, ChildTypeDTDConflict, ChildIsNotOptional
from unittest import TestCase


class TestNoteDTD(TestCase):
    def setUp(self):
        self.note = Note()

    def test_add_child_type(self):
        # self.note.reset_children()
        self.note.add_child(FullNote())
        self.note.add_child(Grace())
        with self.assertRaises(ChildTypeDTDConflict):
            self.note.add_child(Duration())

    def test_add_child_max_occurrence(self):
        self.note.add_child(FullNote())
        with self.assertRaises(ChildOccurrenceDTDConflict):
            self.note.add_child(FullNote())

    def test_close(self):
        # self.note.reset_children()
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
        # self.note.reset_children()
        self.note.add_child(FullNote())
        self.note.add_child(Beam())
        self.note.add_child(Tie())
        self.note.add_child(Beam())
        self.note.add_child(Duration())
        self.note.add_child(Tie())
        # self.note.sort_children()
        self.note.close()
        result = ['FullNote', 'Duration', 'Tie', 'Tie', 'Beam', 'Beam']
        self.assertEqual([type(child).__name__ for child in self.note.get_children()], result)
