import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treeinstruments import Violin, Cello, Viola
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        sf = SimpleFormat(quarter_durations=[4])
        sf.to_stream_voice().add_to_score(self.score, part_number=1)
        sf.to_stream_voice().add_to_score(self.score, part_number=2)
        sf.to_stream_voice().add_to_score(self.score, part_number=3)
        sf.to_stream_voice().add_to_score(self.score, part_number=4)
        self.score.get_score_parts()[0].instrument = Violin(1)
        self.score.get_score_parts()[1].instrument = Violin(2)
        self.score.get_score_parts()[2].instrument = Viola()
        self.score.get_score_parts()[3].instrument = Cello()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        self.score.get_score_parts()[0].add_part_group(number=1, type='start', name='', symbol='bracket', barline='yes')
        self.score.get_score_parts()[2].add_part_group(number=1, type='stop')
        self.score.write(path=xml_path)
        TestScore().assert_template(result_path=xml_path)

    def test_2(self):
        xml_path = path + '_test_2.xml'
        self.score.get_score_parts()[1].add_part_group(number=1, type='start', name='', symbol='bracket', barline='yes')
        self.score.get_score_parts()[2].add_part_group(number=1, type='stop')
        self.score.write(path=xml_path)
        TestScore().assert_template(result_path=xml_path)

    def test_3(self):
        xml_path = path + '_test_3.xml'
        self.score.get_score_parts()[0].add_part_group(number=1, type='start', name='', symbol='bracket', barline='yes')
        self.score.get_score_parts()[3].add_part_group(number=1, type='stop')
        self.score.write(path=xml_path)
        TestScore().assert_template(result_path=xml_path)
