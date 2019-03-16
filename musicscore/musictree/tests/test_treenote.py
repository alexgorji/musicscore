from unittest import TestCase
from musicscore.musictree.musicnote import TreeNote
from musicscore.musicxml.elements.note import Duration


class TestTreeNote(TestCase):
    def setUp(self):
        self.note = TreeNote()

    def test_quarter_duration(self):
        self.note.add_child(Duration(self.note.quarter_duration))
        result = ['Rest', 'Duration']
        self.assertEqual([type(child).__name__ for child in self.note.get_children()], result)
        self.note.quarter_duration = 0
        self.note.sort_children()
        result = ['Grace', 'Rest']
        self.assertEqual([type(child).__name__ for child in self.note.get_children()], result)
