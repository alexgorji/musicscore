from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treeclef import BASS_CLEF
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[1, 1])
        sf.chords[0].add_clef(BASS_CLEF)
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, 1, 1)

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        # TestScore().assert_template(result_path=result_path)
