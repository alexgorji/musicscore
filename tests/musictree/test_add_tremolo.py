from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treechordflags1 import FingerTremoloFlag1
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[7])

        sf.chords[0].add_tremolo()

        sf.to_stream_voice().add_to_score(self.score)
        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[2, 2])

        sf.chords[0].add_tremolo(type='start')
        sf.chords[1].add_tremolo(type='stop')
        sf.to_stream_voice().add_to_score(self.score)
        result_path = path + '_test_2'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_3(self):
        sf = SimpleFormat(quarter_durations=[1.5, 1.5])

        sf.chords[0].add_tremolo(type='start')
        sf.chords[1].add_tremolo(type='stop')
        sf.to_stream_voice().add_to_score(self.score)
        result_path = path + '_test_3'
        self.score.write(path=result_path)
        # TestScore().assert_template(result_path=result_path)

    def test_4(self):
        sf = SimpleFormat(quarter_durations=[0.5, 0.5], midis=[60, 63])

        sf.chords[0].add_tremolo(type='start')
        sf.chords[1].add_tremolo(type='stop')

        sf.to_stream_voice().add_to_score(self.score)
        result_path = path + '_test_4'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    # def test_4(self):
    #     sf = SimpleFormat(durations=[1.5, 1.5])
    #
    #     sf.chords[0].add_tremolo(type='unmeasured')
    #     sf.chords[1].add_tremolo(type='unmeasured')
    #     sf.to_stream_voice().add_to_score(self.score)
    #     result_path = path + '_test_4'
    #     self.score.write(path=result_path)
    #     # TestScore().assert_template(result_path=result_path)
