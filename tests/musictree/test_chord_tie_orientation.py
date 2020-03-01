from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[2, 2], midis=[60, 60])
        sf.chords[0].tie_orientation = 'over'
        sf.chords[0].add_tie('start')
        sf.chords[0].is_adjoinable = False
        sf.chords[1].add_tie('stop')

        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[6], midis=[60])
        sf.chords[0].tie_orientation = 'over'

        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
