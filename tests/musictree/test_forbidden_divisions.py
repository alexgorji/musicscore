from unittest import TestCase
import random
import os

from musicscore.musicstream.streamvoice import SimpleFormat, TreeMeasure, TreePart
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        random.seed(1)
        durations = [random.random() + random.random() for i in range(10)]
        self.sf = SimpleFormat(quarter_durations=durations)
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        self.sf.to_stream_voice().add_to_score(self.score, part_number=1)
        self.sf.to_stream_voice().add_to_score(self.score, part_number=2)
        for measure in self.score.get_children_by_type(TreeMeasure):
            measure.get_children_by_type(TreePart)[-1].forbidden_divisions = [8]
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_2(self):
        xml_path = path + '_test_2.xml'
        self.score.max_division = 6
        self.sf.to_stream_voice().add_to_score(self.score, part_number=1)
        self.sf.to_stream_voice().add_to_score(self.score, part_number=2)
        for measure in self.score.get_children_by_type(TreeMeasure):
            measure.get_children_by_type(TreePart)[-1].forbidden_divisions = [5]
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_3(self):
        xml_path = path + '_test_3.xml'
        self.score.max_division = 6
        self.score.forbidden_divisions = [8]
        self.sf.to_stream_voice().add_to_score(self.score, part_number=1)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)
