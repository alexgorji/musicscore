import os
from unittest import TestCase

from musicscore.musictree.treemeasure import TreePart
from musicscore.musicxml.groups.musicdata import Attributes

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):

    def setUp(self) -> None:
        self.part = TreePart(id='test_part')

    def test_1(self):
        self.assertIsNone(self.part.staves)

    def test_2(self):
        p = self.part
        p.staves = 1
        expected = 1
        actual = p.staves
        self.assertEqual(expected, actual)

    def test_3(self):
        p = self.part
        p.staves = 1
        p.staves = 2
        expected = 2
        actual = p.staves
        self.assertEqual(expected, actual)
