from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

import os

from musicscore.musicxml.types.complextypes.notations import Slur
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[2, 2])
        slur = sf.chords[0].add_slur('start')
        slur.line_type = 'dashed'
        sf.chords[1].add_slur('stop')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)

        TestScore().assert_template(xml_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[2, 2], midis=[(60, 63), (72, 76)])
        slur = sf.chords[0].add_slur('start')
        slur.line_type = 'dashed'
        sf.chords[1].add_slur('stop')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)

        TestScore().assert_template(xml_path)

    def test_3(self):
        sf = SimpleFormat(quarter_durations=[2, 2, 2, 2], midis=[60, 63, 66, 69])
        # slur_1_1 = Slur(type='start', number=1)
        # slur_1_2 = Slur(type='stop', number=1)
        sf.chords[0].add_slur(type='start', number=1)
        sf.chords[-1].add_slur(type='stop', number=1)

        # slur_2_1 = Slur(type='start', number=2, line_type='dashed')
        # slur_2_2 = Slur(type='stop', number=2)
        sf.chords[0].add_slur(type='start', number=2, line_type='dashed')
        sf.chords[2].add_slur(type='stop', number=2)

        # slur_3_1 = Slur(type='start', number=3, line_type='dotted')
        # slur_3_2 = Slur(type='stop', number=3)
        sf.chords[2].add_slur(type='start', number=3, line_type='dotted')
        sf.chords[-1].add_slur(type='stop', number=3)

        # slur_4_1 = Slur(type='start', number=4, line_type='wavy')
        # slur_4_2 = Slur(type='stop', number=4)
        sf.chords[1].add_slur(type='start', number=4, line_type='wavy')
        sf.chords[2].add_slur(type='stop', number=4)

        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_3.xml'
        self.score.write(xml_path)

        TestScore().assert_template(xml_path)
