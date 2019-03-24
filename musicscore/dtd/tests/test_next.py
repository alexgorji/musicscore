

from unittest import TestCase

from musicscore.musicxml.elements.note import Note


class Test(TestCase):
    def setUp(self):
        self.dtd = Note().dtd

    # def test_next(self):
    #     for i in range(14):
    #         print([leaf for leaf in self.dtd.next().traverse_leaves()])
