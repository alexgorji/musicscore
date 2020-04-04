from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        sf = SimpleFormat(quarter_durations=[1, 1])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

    def test_1(self):
        self.score.add_title('test title', font_family='DejaVu Sans')
        self.score.add_subtitle('test subtitle', font_family='DejaVu Sans')
        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        self.score.page_style.format = 'landscape'
        self.score.add_title('test title', font_family='DejaVu Sans')
        self.score.add_subtitle('test subtitle', font_family='DejaVu Sans')

        result_path = path + '_test_2'
        self.score.write(path=result_path)
        # TestScore().assert_template(result_path=result_path)
