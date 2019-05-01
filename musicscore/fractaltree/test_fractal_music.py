from unittest import TestCase

from musicscore.fractaltree.fractaltree import FractalMusic


class Test(TestCase):

    def test_1(self):
        fm = FractalMusic()
        fm.add_layer()
        print(fm)