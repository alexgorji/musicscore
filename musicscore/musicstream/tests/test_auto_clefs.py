from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescore_timewise import TreeScoreTimewise
from musicscore.musicxml.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        # sf = SimpleFormat(midis = [52, 51, 70, 100, 110, 107, 90, 80, 70, 60, 50, 40, 30])
        sf = SimpleFormat(midis=[30, 40, 50, 60, 70, 80, 90, 100, 110, 100, 90, 80, 70, 60, 50, 40, 30])
        sf.auto_clef()
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 1)

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        # TestScore().assert_template(result_path=result_path)
