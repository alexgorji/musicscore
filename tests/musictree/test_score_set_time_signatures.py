from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[4, 4, 3, 2, 3, 4, 5, 6, 1, 2])
        self.score.set_time_signatures(quarter_durations=sf.quarter_duration)

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[4, 4, 3, 2, 3, 4, 5, 6, 1, 2])
        self.score.set_time_signatures(times={1: (3, 4), 5: (2, 4)})

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_2'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_3(self):
        sf = SimpleFormat(quarter_durations=[4, 4, 3, 2, 3, 4, 5, 6, 1, 2])
        self.score.set_time_signatures(quarter_durations=[8, 3, 5, 4, 11, 3])

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_3'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_4(self):
        sf = SimpleFormat(quarter_durations=[4, 4, 3, 2, 3, 4, 5, 6, 1, 2])
        self.score.set_time_signatures(quarter_durations=[8, 3, 5, 4, 11, 3], times={1: (3, 4)})

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_4'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
