import os
from unittest import TestCase

from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.groups.musicdata import Direction
from tests.score_templates.xml_test_score import TestScore
from musicscore.musicxml.types.complextypes.direction import DirectionType, Sound
from musicscore.musicxml.types.complextypes.directiontype import Metronome
from musicscore.musicxml.types.complextypes.metronome import BeatUnit, PerMinute

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        self.score.add_measure()
        self.score.add_part()
        part = self.score.get_measure(1).get_part(1)
        d = part.add_child(Direction())
        dt = d.add_child(DirectionType())
        m = dt.add_child(Metronome())
        m.add_child(BeatUnit('quarter'))
        m.add_child(PerMinute('100'))
        d.add_child(Sound(tempo=100))

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
