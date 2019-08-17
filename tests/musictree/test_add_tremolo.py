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
        sf = SimpleFormat(durations=[7])

        sf.chords[0].add_tremolo()

        sf.to_stream_voice().add_to_score(self.score, 1, 1)
        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        sf = SimpleFormat(durations=[2, 2])

        sf.chords[0].add_tremolo(type='start')
        sf.chords[1].add_tremolo(type='stop')
        sf.to_stream_voice().add_to_score(self.score, 1, 1)
        result_path = path + '_test_2'
        self.score.write(path=result_path)
        # TestScore().assert_template(result_path=result_path)

    # def test_2(self):
    #     sf = SimpleFormat(durations=[1, 1])
    #
    #     sf.chords[0].add_words('a')
    #     sf.chords[1].add_words('b')
    #     sf.chords[0].add_words('aa', relative_y=-15)
    #
    #     v = sf.to_stream_voice(1)
    #     v.add_to_score(self.score, 1, 1)
    #
    #     result_path = path + '_test_2'
    #     self.score.write(path=result_path)
    #     TestScore().assert_template(result_path=result_path)
    #
    # def test_3(self):
    #     sf = SimpleFormat(durations=[1.95, 2.05])
    #
    #     sf.chords[0].add_words('a')
    #     sf.chords[1].add_words('b')
    #     sf.chords[0].add_words('aa', relative_y=-15)
    #
    #     v = sf.to_stream_voice(1)
    #     v.add_to_score(self.score, 1, 1)
    #
    #     result_path = path + 'test_3'
    #     self.score.write(path=result_path)
    #     # TestScore().assert_template(result_path=result_path)
