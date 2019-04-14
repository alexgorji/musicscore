from unittest import TestCase

from musicscore.musicxml.common.common import Voice
from musicscore.musicxml.elements.fullnote import Pitch
from musicscore.musicxml.elements.note import Note, Duration


class Test(TestCase):
    def setUp(self) -> None:
        self.note = Note()
        self.note.add_child(Pitch())
        self.note.add_child(Duration())

    def test_voice(self):
        self.note.add_child(Voice('1'))
        print(self.note.get_children())
        # print(self.note.to_string())