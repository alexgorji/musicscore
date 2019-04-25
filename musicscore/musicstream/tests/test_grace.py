from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescore_timewise import TreeScoreTimewise

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(durations=[0, 4])
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 1)
        result_path = path + '_test_1'
        self.score.write(path=result_path)

    def test_2(self):
        sf = SimpleFormat(durations=[1, 0, 3])
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 1)
        result_path = path + '_test_2'
        self.score.write(path=result_path)

    def test_3(self):
        sf = SimpleFormat(durations=[4, 0])
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 1)
        result_path = path + '_test_3'
        self.score.write(path=result_path)

    def test_4(self):
        sf = SimpleFormat(durations=[1.5, 0, 2.5])
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 1)
        result_path = path + '_test_4'
        self.score.write(path=result_path)

    def test_5(self):
        sf = SimpleFormat(durations=[1.75, 0, 2.25])
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 1)
        result_path = path + '_test_5'
        self.score.write(path=result_path)

    def test_6(self):
        sf = SimpleFormat(durations=[1.75, 0, 2, 0, 4.25])
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 1)
        result_path = path + '_test_6'
        self.score.write(path=result_path)

    def test_7(self):
        sf = SimpleFormat(durations=[1.3, 0, 2, 0, 0.7])
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 1)
        self.score.add_beats()
        self.score.quantize()
        self.score.split_not_notatable()
        self.score.update_tuplets()
        # self.score.update_types()
        # self.score.update_dots()
        # self.score.finish()


        # print([chord.quarter_duration for chord in self.score.get_measure(1).get_part(1).chords])
        # print([chord.parent_beat for chord in self.score.get_measure(1).get_part(1).chords])
        # result_path = path + '_test_7'
        # self.score.write(path=result_path)
