import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        sf = SimpleFormat(quarter_durations=[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

    def test_1(self):
        self.score.page_style.orientation = 'landscape'
        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        for index, measure in enumerate(self.score.get_children_by_type(TreeMeasure)):
            if index % 4 == 0:
                measure.add_system_break()
        self.score.page_style.orientation = 'landscape'
        self.score.page_style.system_distance = 150
        result_path = path + '_test_2'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_3(self):
        # self.score.page_style.format = 'landscape'
        self.score.get_measure(5).add_system_break()
        # p = self.score.get_measure(5).get_part(1).get_children_by_type(Print)[0]
        # s = p.add_child(SystemLayout())
        # s.add_child(SystemDistance(300))
        self.score.get_measure(10).add_system_break()
        self.score.get_measure(10).add_system_distance(200)
        self.score.get_measure(12).add_system_distance(200)
        # self.score.page_style.system_distance = 20

        result_path = path + '_test_3'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
