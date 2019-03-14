from unittest import TestCase
from musicscore.musicxml.elements.score_header import PartName, ScorePart, PartList


class TestXMLPartName(TestCase):
    def setUp(self):
        self.part_name = PartName(name="part 1")

    def test_xml_part_name(self):
        result = '<part-name>part 1</part-name>\n'
        self.assertEqual(self.part_name.to_string(), result)


class TestXMLScorePart(TestCase):
    def setUp(self):
        self.score_part = ScorePart(id=1)
        self.score_part.add_child(PartName(name="part"))

    def test_xml_score_part(self):
        result = '<score-part id="1">\n  <part-name>part</part-name>\n</score-part>\n'
        self.assertEqual(self.score_part.to_string(), result)


class TestXMLPartList(TestCase):
    def setUp(self):
        self.part_list = PartList()
        score_part = ScorePart(id=1)
        score_part.add_child(PartName(name="part"))
        self.part_list.add_child(score_part)

    def test_xml_part_list(self):
        result = '<part-list>\n  <score-part id="1">\n    <part-name>part</part-name>\n  </score-part>\n</part-list>\n'
        self.assertEqual(self.part_list.to_string(), result)


