import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[4, 4, 4, 4, 4])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        self.score.get_measure(3).add_page_break()

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[4, 4, 4, 4, 4])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, 1)
        sf = SimpleFormat(quarter_durations=[4, 4, 4, 4, 4])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, 2)
        self.score.get_measure(3).add_page_break()

        result_path = path + '_test_2'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
