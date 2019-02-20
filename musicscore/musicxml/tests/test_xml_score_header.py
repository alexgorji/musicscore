from unittest import TestCase
from musicscore.musicxml.elements.xml_score_header import XMLPartName, XMLScorePart, XMLPartList


class TestXMLPartName(TestCase):
    def setUp(self):
        self.part_name = XMLPartName(name="part 1")

    def test_xml_part_name(self):
        result = '<part-name print-object="no">part 1</part-name>\n'
        self.assertEqual(self.part_name.to_string(), result)


class TestXMLScorePart(TestCase):
    def setUp(self):
        self.score_part = XMLScorePart(id=1)

    def test_xml_score_part(self):
        result = '<score-part id="1">\n  <part-name print-object="no">part</part-name>\n</score-part>\n'
        self.assertEqual(self.score_part.to_string(), result)


class TestXMLPartList(TestCase):
    def setUp(self):
        self.part_list = XMLPartList()
        self.part_list.add_child(XMLScorePart(id=1))

    def test_xml_part_list(self):
        result = '<part-list>\n  <score-part id="1">\n    <part-name print-object="no">part</part-name>\n  </score-part>\n</part-list>\n'
        self.assertEqual(self.part_list.to_string(), result)


