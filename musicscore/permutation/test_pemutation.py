from unittest import TestCase

from musicscore.permutation.permutation import Permutation
from musicscore.permutation.permutation import permute


class Test(TestCase):

    def test_1(self):
        result = ['c', 'a', 'b']
        self.assertEqual(permute(input_list=['a', 'b', 'c'], permutation_order=(3, 1, 2)), result)

    def test_2(self):
        p = Permutation(input_list=['a', 'b', 'c'], main_permutation_order=(3, 1, 2))
        result = [[3, 1, 2], [2, 3, 1], [1, 2, 3], [1, 2, 3], [3, 1, 2], [2, 3, 1], [2, 3, 1], [1, 2, 3], [3, 1, 2]]
        self.assertEqual(p.multiplied_order, result)
        result = ['c', 'a', 'b', 'b', 'c', 'a', 'a', 'b', 'c', 'a', 'b', 'c', 'c', 'a', 'b', 'b', 'c', 'a', 'b', 'c',
                  'a', 'a', 'b', 'c', 'c', 'a', 'b', 'c', 'a', 'b']
        self.assertEqual([p.next_element().value for i in range(30)], result)


