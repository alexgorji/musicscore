from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from quicktions import Fraction
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[1.5, 1.5])
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[2, 1.5])
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_3(self):
        sf = SimpleFormat(quarter_durations=[2.5, 1.5])
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_3.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_4(self):
        sf = SimpleFormat(quarter_durations=[1.5, 2.5])
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_4.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_5(self):
        sf = SimpleFormat(quarter_durations=[1.5, 0.5, 2], midis=[0, 0, 60])
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_5.xml'
        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)

    def test_6(self):
        durations = [Fraction(1, 2), Fraction(5, 2), Fraction(1, 5), Fraction(4, 5)]
        sf = SimpleFormat(quarter_durations=durations, midis=[60, 0, 0, 60])
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_6.xml'
        self.score.write(xml_path)
