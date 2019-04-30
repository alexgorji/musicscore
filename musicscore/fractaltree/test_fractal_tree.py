from unittest import TestCase

from musicscore.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(proportions=[1, 2, 3], tree_permutation_order=(3, 1, 2))

    def test_1(self):
        print(self.ft.proportions)
        print(self.ft.tree_permutation_order)
        print(self.ft.multi)
        print(self.ft.name)
        print(self.ft.value)
        print(self.ft.children_fractal_values)