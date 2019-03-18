from unittest import TestCase

from musicscore.musictree.treetimewise import TreeScoreTimewise


class TestTreeTimewise(TestCase):
    def setUp(self):
        self.score = TreeScoreTimewise()
        self.score.add_measure()
        self.score.add_part('one')

    def test_score(self):
        print(self.score.to_string())