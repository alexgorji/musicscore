from unittest import TestCase

from quicktions import Fraction

from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePartVoice, TreePart


# class Test(TestCase):
#     def setUp(self) -> None:
#         self.tv = TreePartVoice()
#         m = TreeMeasure()
#         p = m.add_child(TreePart('one'))
#         self.tv.part = p
#
#     def test_1(self):
#         self.tv.add_chord(TreeChord(quarter_duration=1.5))
#         self.tv.add_chord(TreeChord(quarter_duration=0.5))
#         self.tv.add_chord(TreeChord(quarter_duration=2))
#         remain = self.tv.add_chord(TreeChord())
#         result = [Fraction(3, 2), Fraction(1, 2), Fraction(2, 1)]
#         self.assertEqual([chord.quarter_duration for chord in self.tv.chords], result)
#         self.assertEqual(remain.quarter_duration, 1)
