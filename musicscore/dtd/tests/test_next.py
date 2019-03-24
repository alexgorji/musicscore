

from unittest import TestCase

from musicscore.musicxml.elements.note import Note


class Test(TestCase):
    def setUp(self):
        self.dtd = Note().dtd

    def test_next(self):
        pass