from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[1, 3.5])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, part_number=2, first_measure=2)
        result_path = path + '_test_1'
        self.score.write(path=result_path)

        TestScore().assert_template(result_path=result_path)
