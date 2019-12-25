from quicktions import Fraction
from unittest import TestCase
import musicscore.musictree.treebeat as q
from musicscore.musictree.treechord import TreeChord


class Test(TestCase):

    def test_1(self):
        durations = [0.4, 0.2, 0.1, 0.3]
        b = q.TreeBeat(max_division=5, forbidden_divisions=[])

        result = [Fraction(2, 5), Fraction(1, 5), Fraction(1, 5), Fraction(1, 5)]

        self.assertEqual(b.get_quantized_durations(durations), result)
        self.assertEqual(b.best_div, 5)

    def test_2(self):
        b = q.TreeBeat(max_division=5, forbidden_divisions=[])
        b.add_chord(TreeChord((60, 61), quarter_duration=1))
        b.quantize()
        self.assertEqual([chord.quarter_duration for chord in b.chords], [1])

    def test_3(self):
        b = q.TreeBeat(max_division=5, forbidden_divisions=[])
        b.add_chord(TreeChord((60, 61), quarter_duration=0.5))
        b.add_chord(TreeChord((60, 61), quarter_duration=0.5))
        b.quantize()
        self.assertEqual([chord.quarter_duration for chord in b.chords], [Fraction(1, 2), Fraction(1, 2)])

    def test_4(self):
        b = q.TreeBeat(max_division=5, forbidden_divisions=[])
        b.add_chord(TreeChord((60, 61), 5))
        b.quantize()
        self.assertEqual([chord.quarter_duration for chord in b.chords], [5])

    def test_5(self):
        b = q.TreeBeat(max_division=7, forbidden_divisions=[])
        b.add_chord(TreeChord((60, 61), quarter_duration=0.5))
        b.add_chord(TreeChord((60, 61), quarter_duration=0.2))
        b.add_chord(TreeChord((60, 61), quarter_duration=0.3))
        b.quantize()
        self.assertEqual([chord.quarter_duration for chord in b.chords],
                         [Fraction(1, 2), Fraction(1, 6), Fraction(1, 3)])