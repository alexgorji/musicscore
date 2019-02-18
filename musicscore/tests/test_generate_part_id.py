from unittest import TestCase
from musicscore.score import Part


class TestGeneratePartId(TestCase):

    def test_generate_part_id(self):
        def get_id(number):
            for i in range(number):
                part = Part()

        get_id(3)
        part = Part(id='p10')
        get_id(1)
        result = ['p1', 'p2', 'p3', 'p10', 'p4']
        self.assertEqual(part._ids, ['p1', 'p2', 'p3', 'p10', 'p4'])
        with self.assertRaises(ValueError):
            part = Part(id='p4')
