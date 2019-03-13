# from unittest import TestCase
# from musicscore.musicxml.elements.xml_partwise import XMLScorePartwise, XMLPartPartwise, XMLMeasurePartwise
# from musicscore.musicxml.elements.xml_score_header import XMLScorePart
# from musicscore.musicxml.elements.note import Note, Duration
# from musicscore.musicxml.elements.fullnote import Pitch
# from musicscore.musicxml.elements.attributes import Time, XMLClef, Divisions, Attributes
# from musicscore.musicxml.elements.xml_score_header import XMLPartList
#
# import os
# path = os.path.abspath(__file__).split('.')[0]
#
#
# class TestXMLScorePartwise(TestCase):
#     def setUp(self):
#         self.score = XMLScorePartwise()
#         part_id = 'P1'
#         part_list = self.score.add_child(XMLPartList())
#         part_list.add_child(XMLScorePart(id=part_id))
#         part = self.score.add_child(XMLPartPartwise(id=part_id))
#         measure = self.make_measure()
#         part.add_child(measure)
#
#     def make_measure(self):
#         measure = XMLMeasurePartwise(number=1)
#         xml_attributes = measure.add_child(Attributes())
#         xml_attributes.add_child(Time(4, 4))
#         xml_attributes.add_child(XMLClef('G', 2))
#         xml_attributes.add_child(Divisions(1))
#         note = Note()
#         note.add_child(Pitch())
#         note.add_child(Duration(4))
#         measure.add_child(note)
#         return measure
#
#     def test_xml_score(self):
#         self.score.write(path=path)
#
#
#
