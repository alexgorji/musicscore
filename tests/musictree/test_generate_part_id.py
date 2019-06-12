# from unittest import TestCase
# from musicscore.partwise import PartPartwise
#
#
# class TestGeneratePartId(TestCase):
#
#     def test_generate_part_id(self):
#         PartPartwise.reset_ids()
#
#         def get_id(number):
#             for i in range(number):
#                 part = PartPartwise()
#         get_id(1)
#         PartPartwise.reset_ids()
#         get_id(3)
#         part = PartPartwise(id='p10')
#         get_id(1)
#         result = ['p1', 'p2', 'p3', 'p10', 'p4']
#         self.assertEqual(part._ids, result)
#         with self.assertRaises(ValueError):
#             part = PartPartwise(id='p4')
