from unittest import TestCase
import os

from quicktions import Fraction

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[7])
        v = sf.to_stream_voice()
        v.add_to_score(self.score)
        result_path = path + '_test_1'
        self.score.write(path=result_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[12.5])
        v = sf.to_stream_voice()
        v.add_to_score(self.score)
        result_path = path + '_test_2'
        self.score.write(path=result_path)

    def test_3(self):
        # sf = SimpleFormat(durations=[Fraction(4) + Fraction(1, 2), Fraction(1, 2)])
        sf = SimpleFormat(quarter_durations=[Fraction(4, 1) + Fraction(5, 7), Fraction(5, 7)])
        # sf = SimpleFormat(durations=[Fraction(4, 1) + Fraction(5, 7), Fraction(2, 7)])
        v = sf.to_stream_voice()
        v.add_to_score(self.score)

        self.score.finish()
        # print([chord.quarter_duration for chord in self.score.get_measure(2).get_part(1).chords])
        # print([chord.tie_types for chord in self.score.get_measure(2).get_part(1).chords])
        result_path = path + '_test_3'
        self.score.write(path=result_path)
