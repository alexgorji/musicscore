import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechordflags4 import HideAccidental4
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        midis = [60, 61, 62, 61]
        sf = SimpleFormat(midis=midis)
        for chord in sf.chords:
            chord.add_flag(HideAccidental4())

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)
