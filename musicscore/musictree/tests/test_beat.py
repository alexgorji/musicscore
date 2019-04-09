from quicktions import Fraction
from unittest import TestCase
import musicscore.musictree.treebeat as q


class Test(TestCase):

    def test_find_nearest(self):
        durations = [0.4, 0.2, 0.1, 0.3]
        b = q.TreeBeat(max_division=5)
        result = [Fraction(2, 5), Fraction(1, 5), Fraction(0, 1), Fraction(2, 5)]
        self.assertEqual(b.get_quantized_durations(durations), result)
        self.assertEqual(b.best_div, 5)
