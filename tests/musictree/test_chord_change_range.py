from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
import os

from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def test_1(self):
        score = TreeScoreTimewise()

        sf = SimpleFormat(midis=[(60, 64, 68, 73)], quarter_durations=[4])
        sf.to_stream_voice().add_to_score(score=score)

        sf.chords[0].change_range(60, 86)
        sf.to_stream_voice().add_to_score(score=score, part_number=2)

        xml_path = path + '.xml'
        score.write(xml_path)
        TestScore().assert_template(xml_path)
