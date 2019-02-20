from unittest import TestCase
from musicscore.score import Score
from musicscore.musicxml.elements.xml_score_header import XMLScorePart


class TestScore(TestCase):
    def setUp(self):
        self.score = Score()

    def test_score_part_list(self):
        self.score.add_part()
        # print(self.score.partwise.to_string())
        # print(self.score.partwise.part_list.to_string())
        # print(self.score.timewise.part_list.to_string())
