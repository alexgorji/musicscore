from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(midis=[(60)], quarter_durations=[2.2])
        sf.chords[0].add_tie('start')
        v = sf.to_stream_voice(1)
        # print(v.chords[0].tie_types)
        v.add_to_score(self.score)
        ch = self.score.get_measure(1).get_part(1).chords[0]
        result_path = path + '_test_1'
        self.score.write(path=result_path)
