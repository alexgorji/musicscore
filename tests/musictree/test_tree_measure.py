from unittest import TestCase

from musicscore.musictree.treebeat import TreeBeat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart


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
        m = TreeMeasure(time=(3, 4))
        self.assertEqual(m.quarter_duration, 3)

        p = TreePart(id='one')
        m.add_child(p)

        tree_part_voice = p.get_staff(1).get_voice(1)
        tree_part_voice.set_beats([TreeBeat(duration=2), TreeBeat(duration=0.5), TreeBeat(duration=0.5)])
        result = [0, 2, 2.5]
        self.assertEqual([beat.offset for beat in tree_part_voice.beats], result)
