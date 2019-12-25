from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.midi import C, D, E, F, G, A, B
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        midis = [C(4, 'flat'), C(4), C(4, 'sharp')]
        sf = SimpleFormat(midis=midis)
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, 1, 1)

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        # TestScore().assert_template(result_path=result_path)

    def test_2(self):
        midis = [D(4), D(4), D(4), D(4), C(4), C(4), C(4), B(3), C(4), C(4), C(4), F(4), E(4), D(4), F(4), F(4), F(4),
                 E(4), D(4), E(4), F(4)]

        durations = [2, 3, 1, 2, 3, 1, 4, 2, 4, 2, 2, 3, 1, 2, 2, 2, 2, 3, 1, 1, 4]
        durations = [d / 2 for d in durations]
        sf = SimpleFormat(midis=midis, durations=durations)
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, 1, 1)

        result_path = path + '_test_2'
        self.score.write(path=result_path)

    def test_3(self):
        midi = E(6)
        # print(midi.value)
        midi.transpose(3)
        # print(midi.value)
