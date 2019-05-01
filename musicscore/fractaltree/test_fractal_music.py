from unittest import TestCase

from musicscore.fractaltree.fractaltree import FractalMusic


class Test(TestCase):

    def test_1(self):
        fm = FractalMusic(duration=12, tree_permutation_order=(3, 1, 2), proportions=[1, 2, 3], multi=(1, 2))
        fm.midi_generator.midi_range = [55, 72]
        fm.add_layer()
        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)
        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)

        print(fm.layers)
