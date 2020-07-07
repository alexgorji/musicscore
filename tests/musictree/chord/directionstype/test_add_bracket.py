import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'

        sf = SimpleFormat(quarter_durations=5 * [2.25])
        sf.chords[0].add_bracket(type='start', line_end='none', relative_x=50)
        sf.chords[1].add_bracket(type='continue', line_end='none')
        sf.chords[2].add_bracket(type='stop', line_end='arrow', relative_x=-30, relative_y=20)

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)
