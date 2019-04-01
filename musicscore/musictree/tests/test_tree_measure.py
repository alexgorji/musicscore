from unittest import TestCase

from musicscore.musictree.treemeasure import TreeMeasure


class Test(TestCase):
    def setUp(self) -> None:
        self.measure = TreeMeasure()

    def test_number(self):
        self.assertTrue(isinstance(self.measure.number, str))
        with self.assertRaises(TypeError):
            self.measure.number = 3

        copied = self.measure.__copy__()
        self.assertTrue(isinstance(copied.number, str))
        with self.assertRaises(TypeError):
            copied.number = 3
