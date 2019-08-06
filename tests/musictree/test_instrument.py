from unittest import TestCase

from musicscore.musictree.treescoretimewise import TreeScoreTimewise


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.score.add_score_part()