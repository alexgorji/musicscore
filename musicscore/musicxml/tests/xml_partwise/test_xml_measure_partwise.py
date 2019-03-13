# from unittest import TestCase
# from musicscore.musicxml.elements.xml_partwise import XMLMeasurePartwise
# from musicscore.musicxml.elements.attributes import Attributes, Time, XMLClef, Divisions
# from musicscore.musicxml.elements.note import Note
# from musicscore.musicxml.elements.fullnote import Pitch
#
#
# class TestMeasurePartwise(TestCase):
#     def setUp(self):
#         self.measure = XMLMeasurePartwise(number=1)
#
#     def test_meaure_partwise(self):
#         attributes = self.measure.add_child(Attributes())
#         attributes.add_child(Time(3, 4))
#         attributes.add_child(XMLClef('G', 2))
#         attributes.add_child(Divisions(2))
#         result = '''<measure number="1">
#   <attributes>
#     <divisions>2</divisions>
#     <time>
#       <beats>3</beats>
#       <beat-type>4</beat-type>
#     </time>
#     <clef>
#       <sign>G</sign>
#       <line>2</line>
#     </clef>
#   </attributes>
# </measure>
# '''
#         self.assertEqual(self.measure.to_string(), result)
#
#     def test_measure_music_data(self):
#         self.measure.test_mode = True
#         note = self.measure.add_child(Note(Pitch(), 10))
#         for child in note.get_children():
#             child.include_in_test = False
#         attributes = self.measure.add_child(Attributes())
#         attributes.add_child(Time(3, 4))
#         attributes.add_child(Divisions(3))
#         with self.assertRaises(TypeError):
#             self.measure.add_child(None)
#         note = self.measure.add_child(Note(Pitch(), 10))
#         for child in note.get_children():
#             child.include_in_test = False
#         result = '''<measure>
#   <note>
#     <pitch>
#       <step/>
#       <octave/>
#     </pitch>
#     <duration/>
#   </note>
#   <attributes>
#     <divisions/>
#     <time>
#       <beats/>
#       <beat-type/>
#     </time>
#   </attributes>
#   <note>
#     <pitch>
#       <step/>
#       <octave/>
#     </pitch>
#     <duration/>
#   </note>
# </measure>
# '''
#         self.assertEqual(self.measure.to_string(), result)
