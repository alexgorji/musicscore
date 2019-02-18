from unittest import TestCase
from musicscore.score import Score


class TestScore(TestCase):
    def setUp(self):
        self.score = Score()

    def test_score_part_list(self):
        self.score.add_part()
        print(self.score.partwise.part_list.to_string())
        print(self.score.timewise.part_list.to_string())
