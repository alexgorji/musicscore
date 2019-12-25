import os
from unittest import TestCase

from musicscore.musicstream import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(durations=[3, 1])
        sf.chords[1].to_rest()
        sf.chords[0].add_tie('start')
        sf.chords[1].add_tie('stop')
        sf.chords[0].is_adjoinable = False
        xml_path = path + '_test_1.xml'
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
