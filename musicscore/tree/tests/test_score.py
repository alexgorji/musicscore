from unittest import TestCase
from musicscore.score import Score, Part


class TestScore(TestCase):
    def setUp(self):
        self.score = Score()

    def test_score_part_list(self):
        self.score.add_part()
        self.score.add_part(Part(name='new name', print_object='yes'))
        self.score.add_part(Part(id='p10'))
        print(self.score.partwise.to_string())
