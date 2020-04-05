from unittest import TestCase
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
import os

from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self):
        self.score = TreeScoreTimewise()
        self.score.add_part()

    def test_1(self):
        self.score.add_measure().time = (3, 4)
        self.score.add_measure().time = (2, 4)
        self.score.add_measure().time = (2, 4)
        self.score.add_measure().time = (2, 4)
        self.score.get_measure(4).time.force_show = True
        self.score.add_measure().time = (3, 8)

        self.score.finish()
        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
