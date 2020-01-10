from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.main_score = TreeScoreTimewise()

    def test_1(self):
        section_score_1 = TreeScoreTimewise()
        sf = SimpleFormat(durations=[1, 3, 2])
        section_score_1.set_time_signatures(durations=sum(sf.durations), barline_style='light-light')
        sf.to_stream_voice().add_to_score(section_score_1)

        section_score_2 = TreeScoreTimewise()
        sf = SimpleFormat(durations=[2, 1, 3])
        section_score_2.set_time_signatures(durations=sum(sf.durations), barline_style='heavy')
        sf.to_stream_voice().add_to_score(section_score_2)

        self.main_score.extend(section_score_1)
        self.main_score.extend(section_score_2)

        xml_path = path + '_test_1.xml'
        self.main_score.write(path=xml_path)
        # TestScore().assert_template(result_path=result_path)
