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
        for chord in sf.chords:
            chord.add_articulation('accent')
            chord.add_articulation('tenuto')
        sf.chords[0].add_slur('start')
        sf.chords[-1].add_slur('stop')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
