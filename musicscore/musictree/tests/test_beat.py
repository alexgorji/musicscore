from unittest import TestCase
import musicscore.musictree.treebeat as q


class Test(TestCase):

    def test_find_nearest(self):
        durations = [0.4, 0.2, 0.1, 0.3]
        b = q.Beat(max_division=5)
        print(b.get_quantized_durations(durations))
        print(b.best_div)
