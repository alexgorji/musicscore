from musicscore.basic_functions import substitute
from unittest import TestCase


class Test(TestCase):
    def test_substitute(self):
        input_list = [1, 2, 3, 4, 5]
        new_elements = ['a', 'b', 'c']
        result = [1, 2, 'a', 'b', 'c', 4, 5]

        self.assertEqual(substitute(input_list, 3, new_elements), result)

        result = [1, 2, 'z', 4, 5]
        new_elements = 'z'
        self.assertEqual(substitute(input_list, 3, new_elements), result)
