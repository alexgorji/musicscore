from unittest import TestCase

from musicscore.musictree.treebeat import TreeBeat
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

    def test_duration(self):
        m = TreeMeasure(time=(3, 8))
        self.assertEqual(m.quarter_duration, 1.5)

        m.set_beats([TreeBeat(duration=1), TreeBeat(duration=0.5), TreeBeat(duration=2)])
        result = [0, 1, 1.5]
        self.assertEqual([beat.offset for beat in m.get_beats()], result)
