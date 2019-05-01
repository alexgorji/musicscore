from unittest import TestCase

from quicktions import Fraction

from musicscore.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(proportions=[1, 2, 3], tree_permutation_order=(3, 1, 2))

    def test_1(self):
        self.ft.add_layer()
        self.ft.add_layer()
        self.assertEqual(self.ft.get_layer(0, key='value'), 10)
        result = [Fraction(5, 1), Fraction(5, 3), Fraction(10, 3)]
        self.assertEqual(self.ft.get_layer(1, key='value'), result)
        result = [[Fraction(5, 6), Fraction(5, 3), Fraction(5, 2)], [Fraction(5, 6), Fraction(5, 18), Fraction(5, 9)],
                  [Fraction(10, 9), Fraction(5, 3), Fraction(5, 9)]]
        self.assertEqual(self.ft.get_layer(2, key='value'), result)

    def test_2(self):
        self.ft.add_layer()
        self.ft.add_layer(lambda n: True if n.fractal_order > 1 else False)
        # print([node.fractal_order for node in self.ft.get_layer(1)])
        # print([node.fertile for node in self.ft.get_layer(1)])
        self.ft.add_layer(lambda n: True if n.fractal_order > 1 else False)
        self.ft.add_layer(lambda n: True if n.fractal_order > 1 else False)
        self.ft.add_layer(lambda n: True if n.fractal_order > 1 else False)
        # self.ft.add_layer(lambda n: True if n.fractal_order > 1 else False)
        # print([node.fertile for node in self.ft.traverse_leaves()])
        # print([node.name for node in self.ft.traverse_leaves()])
        # self.ft.add_layer(lambda n: True if n.fractal_order > 1 else False)
        # print([name for name in self.ft.get_layer(0, key='name')])
        # print([name for name in self.ft.get_layer(1, key='name')])
        # print([name for name in self.ft.get_layer(2, key='name')])
        result = [[[['1.1']], [['1.2.1'], ['1.2.2.1', '1.2.2.2', '1.2.2.3'], ['1.2.3.1', '1.2.3.2', '1.2.3.3']], [['1.3.1.1', '1.3.1.2', '1.3.1.3'], ['1.3.2'], ['1.3.3.1', '1.3.3.2', '1.3.3.3']]], '2', [[['3.1.1'], ['3.1.2.1', '3.1.2.2', '3.1.2.3'], ['3.1.3.1', '3.1.3.2', '3.1.3.3']], [['3.2.1.1', '3.2.1.2', '3.2.1.3'], ['3.2.2'], ['3.2.3.1', '3.2.3.2', '3.2.3.3']], [['3.3']]]]
        self.assertEqual([name for name in self.ft.get_layer(4, key='name')], result)
        # self.ft.add_layer()
        # print(self.ft.layers)
