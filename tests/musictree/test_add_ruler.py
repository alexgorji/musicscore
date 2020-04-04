from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]

#
# class Test(TestCase):
#     def setUp(self) -> None:
#         self.score = TreeScoreTimewise()
#
#     def test_1(self):
#         sf = SimpleFormat(durations=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
#         v = sf.to_stream_voice(1)
#         v.add_to_score(self.score)
#
#         result_path = path + '_test_1'
#         self.score.finish()
#         self.score.add_ruler()
#         self.score.write(path=result_path)
#         # TestScore().assert_template(result_path=result_path)
