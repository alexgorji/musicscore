from unittest import TestCase

from musicscore.musicstream import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

import os

from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(durations=[2, 2])
        slur = sf.chords[0].add_slur('start')
        slur.line_type = 'dashed'
        sf.chords[1].add_slur('stop')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)

        TestScore().assert_template(xml_path)

    def test_2(self):
        sf = SimpleFormat(durations=[2, 2], midis=[(60, 63), (72, 76)])
        slur = sf.chords[0].add_slur('start')
        slur.line_type = 'dashed'
        sf.chords[1].add_slur('stop')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)

        TestScore().assert_template(xml_path)
