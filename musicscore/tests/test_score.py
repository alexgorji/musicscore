from unittest import TestCase
from musicscore.score import Score, Measure


class ScoreTest(TestCase):
    def setUp(self):
        self.score = Score()

    def test_measures(self):
        self.score.measures = [Measure()]
        self.score.measures = []
        with self.assertRaises(TypeError):
            self.score.measures = [2, 3]