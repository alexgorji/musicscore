from unittest import TestCase
from musicscore.musicxml.elements.scoreheader import PartList
from musicscore.musicxml.types.complextypes.partlist import ScorePart
from musicscore.musicxml.types.complextypes.scorepart import PartName


class TestXMLPartName(TestCase):
    def setUp(self):
        self.part_name = PartName(name="part 1")

    def test_xml_part_name(self):
        result = '<part-name>part 1</part-name>\n'
        self.assertEqual(self.part_name.to_string(), result)


class TestXMLScorePart(TestCase):
    def setUp(self):
        self.score_part = ScorePart(id='p1')
        self.score_part.add_child(PartName(name="part"))

    def test_xml_score_part(self):
        result = '<score-part id="p1">\n  <part-name>part</part-name>\n</score-part>\n'
        self.assertEqual(self.score_part.to_string(), result)


class TestXMLPartList(TestCase):
    def setUp(self):
        self.part_list = PartList()
        score_part = ScorePart(id='p1')
        score_part.add_child(PartName(name="part"))
        self.part_list.add_child(score_part)

    def test_xml_part_list(self):
        result = '<part-list>\n  <score-part id="p1">\n    <part-name>part</part-name>\n  </score-part>\n</part-list>\n'
        self.assertEqual(self.part_list.to_string(), result)
