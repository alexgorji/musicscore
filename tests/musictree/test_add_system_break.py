from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        sf = SimpleFormat(quarter_durations=30 * [4])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

    def test_1(self):
        self.score.page_style.orientation = 'landscape'

        for index, measure in enumerate(self.score.get_children_by_type(TreeMeasure)):
            if index % 4 == 0:
                measure.add_system_break()

        result_path = path + '_test_1'
        self.score.finish()
        partwise = self.score.to_partwise()
        partwise.write(path=result_path)
        # self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
