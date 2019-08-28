import os
from unittest import TestCase

from musicscore.musicstream import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.score.page_style.format = 'portrait'

    def test_1(self):
        sf = SimpleFormat(durations=(1.5, 0.5, 1.5))
        v = sf.to_stream_voice(1)
        self.score.set_time_signatures(times={1: (7, 8)})
        v.add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.finish()
        self.score.to_partwise()
        self.score.write(xml_path)
