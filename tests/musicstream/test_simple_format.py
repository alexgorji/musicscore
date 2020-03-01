import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.sf = SimpleFormat([1, 2, 3, 4, 3, 2, 1])
        self.score = TreeScoreTimewise()

    def test_1(self):
        self.sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + 'test_1.xml'
        self.score.write(xml_path)
        TestScore().assert_template(result_path=xml_path)

    def test_2(self):
        expected = 16
        actual = self.sf.quarter_duration
        self.assertEqual(expected, actual)
