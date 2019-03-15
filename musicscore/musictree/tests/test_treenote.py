from unittest import TestCase
from musicscore.musictree.musicnote import TreeNote
from musicscore.musicxml.elements.note import Duration


class TestTreeNote(TestCase):
    def setUp(self):
        self.note = TreeNote()

    def test_quarter_duration(self):
        print(self.note.get_children())
        self.note.add_child(Duration(self.note.quarter_duration))
        print(self.note.get_children())
        self.note.quarter_duration = 0
        self.note.sort_children()
        print(self.note.get_children())
