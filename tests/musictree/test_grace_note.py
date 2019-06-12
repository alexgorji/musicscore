from unittest import TestCase
import os

from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        self.score.add_measure()
        self.score.add_part()
        self.score.add_chord(1, 1, TreeChord())
        self.score.add_chord(1, 1, TreeChord(quarter_duration=0))
        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
