# from unittest import TestCase
# from musicscore.partwise import Partwise
#
#
# class TestPartwise(TestCase):
#     def setUp(self):
#         self.partwise = Partwise()
#
#     def test_add_part(self):
#         self.partwise.add_part()
#         self.partwise.add_part()
#         self.partwise.test_mode = True
#         result = '''<score-partwise>
#   <part-list>
#     <score-part>
#       <part-name/>
#     </score-part>
#     <score-part>
#       <part-name/>
#     </score-part>
#   </part-list>
#   <part/>
#   <part/>
# </score-partwise>
# '''
#         self.assertEqual(self.partwise.to_string(), result)
#
#     def test_add_measure(self):
#         part = self.partwise.add_part()
#         part.add_measure()
#         self.partwise.test_mode = True
#         result = '''<score-partwise>
#   <part-list>
#     <score-part>
#       <part-name/>
#     </score-part>
#   </part-list>
#   <part>
#     <measure/>
#   </part>
# </score-partwise>
# '''
#         self.assertEqual(self.partwise.to_string(), result)
#
