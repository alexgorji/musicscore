from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
import os

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[1, 1, 1, 1, 1])
        sf.chords[0].add_wedge('crescendo')
        sf.chords[2].add_wedge('stop')
        sf.chords[2].add_wedge('diminuendo')
        sf.chords[-1].add_wedge('stop')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
