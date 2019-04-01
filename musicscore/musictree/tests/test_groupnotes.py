from unittest import TestCase

from musicscore.musictree.midi import Midi
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treenote import TreeNote
from musicscore.musictree.treescore_timewise import TreeScoreTimewise
import os

from musicscore.musicxml.elements.note import Beam

path = os.path.abspath(__file__).split('.')[0]


class TestGrouping(TestCase):
    def setUp(self):
        self.score = TreeScoreTimewise()
        self.score.add_part('one')

    def test_grouping(self):
        for i in range(2):
            # self.make_measure(i + 1, (3, 8, 2, 4))
            self.make_measure(i + 1, (3, 4))

        measure = self.score.get_measure(1)

        measure.get_part(1).group_beams()
        self.score.finish()

        self.score.write(path=path)

    def make_measure(self, number, time_signature=(4, 4)):
        self.score.add_measure(TreeMeasure(time=time_signature))
        for i in range(time_signature[0] * 2):
            self.score.add_note(number, 1, TreeNote(event=Midi(60).get_pitch_rest(), quarter_duration=0.5))
