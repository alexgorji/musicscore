from musicscore.dtd.note import Note, FullNote, Grace, Duration, Beam, Tie
from musicscore.dtd.dtd import ChildOccurrenceDTDConflict, ChildTypeDTDConflict
from unittest import TestCase


class TestNoteDTD(TestCase):
    def setUp(self):
        self.note = Note()

    def test_add_child_max_occurrence(self):
        self.note.add_child(FullNote())
        with self.assertRaises(ChildOccurrenceDTDConflict):
            self.note.add_child(FullNote())

    def test_add_child_type(self):
        self.note.reset_children()
        self.note.add_child(FullNote())
        self.note.add_child(Grace())
        with self.assertRaises(ChildTypeDTDConflict):
            self.note.add_child(Duration())

    def test_add_child_type_2(self):
        self.note.reset_children()
        self.note.add_child(FullNote())
        self.note.add_child(Duration())
        self.note.add_child(Beam())
        self.note.add_child(Beam())
        self.note.add_child(Tie())
        self.note.add_child(Tie())
        self.note.close()
        # print(self.note.get_children())

    def test_sort_children(self):
        self.note.reset_children()
        self.note.add_child(FullNote())
        self.note.add_child(Beam())
        self.note.add_child(Tie())
        self.note.add_child(Beam())
        self.note.add_child(Duration())
        self.note.add_child(Tie())
        self.note.sort_children()
        result = ['FullNote', 'Duration', 'Tie', 'Tie', 'Beam', 'Beam']
        self.assertEqual([type(child).__name__ for child in self.note.get_children()], result)


