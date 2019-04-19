from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescore_timewise import TreeScoreTimewise

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(midis=[70, 72, 73], durations=[2, 0.5, 0.5])
        voice1 = sf.to_voice(1)
        voice1.add_to_score(self.score, 1, 1)

        sf = SimpleFormat(midis=[50, 52, 53], durations=[0.5, 1, 2])
        voice2 = sf.to_voice(2)
        voice2.add_to_score(self.score, 1, 1)

        p = self.score.get_measure(1).get_part(1)
        print(p.voices)

        # self.score.write(path=path + '_test_1')
