import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treeinstruments import Violin
from musicscore.musictree.treepart import TreePart, TreePartStaff, TreePartVoice
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.part = TreePart(id='test_part')

    def test_1(self):
        self.assertIsNone(self.part.staves)

    def test_2(self):
        self.part.add_tree_part_staff(TreePartStaff(2))
        expected = 2
        actual = list(self.part.tree_part_staves)[0]
        self.assertEqual(expected, actual)

    def test_3(self):
        self.part.set_tree_part_staff(staff_number=3)
        expected = 3
        actual = list(self.part.tree_part_staves)[0]
        self.assertEqual(expected, actual)

    def test_4(self):
        tps = self.part.set_tree_part_staff(2)
        tps.add_tree_part_voice(TreePartVoice(2))
        expected = 2
        actual = list(self.part.tree_part_staves[2].tree_part_voices)[0]
        self.assertEqual(expected, actual)

    def test_5(self):
        tree_part_staff = self.part.set_tree_part_staff(1)
        tree_part_staff.add_tree_part_voice(TreePartVoice(2))
        with self.assertRaises(AttributeError):
            tree_part_staff.add_tree_part_voice(TreePartVoice(2))

    def test_6(self):
        tps = self.part.set_tree_part_staff(1)
        tpv_1 = tps.set_tree_part_voice(1)
        tpv_2 = tps.set_tree_part_voice(2)
        expected = [tpv_1, tpv_2]
        actual = self.part.tree_part_voices
        self.assertEqual(expected, actual)

