import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treeinstruments import Violin
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        sf = SimpleFormat(quarter_durations=[4])
        sf.to_stream_voice().add_to_score(self.score)

    def test_1(self):
        self.score.get_score_parts()[0].instrument = Violin()
        self.score.get_score_parts()[0].instrument.part_name.font_size = 9

        xml_path = path + '_test_1.xml'
        self.score.write(path=xml_path)
        # TestScore().assert_template(result_path=xml_path)
