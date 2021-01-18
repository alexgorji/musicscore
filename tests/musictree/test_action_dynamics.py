from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
import os

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        dynamics_list = ['ppp', 'pp', 'p', 'mp', 'mf', 'f', 'ff', 'fff']
        sf = SimpleFormat(quarter_durations=8 * [2])
        for chord, dynamics in zip(sf.chords, dynamics_list):
            chord.add_action_dynamics(dynamics)

        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
