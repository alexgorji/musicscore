import os
import unittest

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechordflags3 import CheckPreviousFlag
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = os.path.abspath(__file__).split('.')[0]


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '.xml'
        sf = SimpleFormat(quarter_durations=[3, 1, 1])
        chord = sf.chords[2]
        chord.add_flag(CheckPreviousFlag())
        sf.to_stream_voice().add_to_score(self.score)
        # print(chord.previous)
        #
        self.score.write(xml_path)
        # self.assertEqual(True, False)
