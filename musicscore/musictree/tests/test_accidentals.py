from unittest import TestCase

from musicscore.musictree.midi import Midi
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treenote import TreeNote
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescore_timewise import TreeScoreTimewise
import os

from musicscore.musicxml.elements.attributes import Attributes

path = os.path.abspath(__file__).split('.')[0]



class TestTreeTimewise(TestCase):
    def setUp(self):
        self.score = TreeScoreTimewise()
        self.score.add_measure()
        part = self.score.add_part('one')

    def test_accidentals(self):
        midis = [60, 61, 62, 60, 63, 64, 65, 61]
        for midi in midis:
            self.score.add_note(1, 1, TreeNote(event=Midi(midi).get_pitch_rest(), quarter_duration=0.5))

        # measure = self.score.get_children_by_type(TreeMeasure)[0]
        # part = measure.get_children_by_type(TreePart)[0]
        # part.finish()

        self.score.finish()
        #
        self.score.write(path=path)

