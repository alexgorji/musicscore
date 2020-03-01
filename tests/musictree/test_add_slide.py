import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat, TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[4, 4, 4], midis=[64, 74, 63])
        sf.chords[0].add_slide('start')
        sf.chords[1].add_slide('stop')
        sf.chords[1].add_slide('start')
        sf.chords[2].add_slide('stop')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)
