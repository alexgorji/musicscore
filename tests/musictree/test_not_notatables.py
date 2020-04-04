from unittest import TestCase

from quicktions import Fraction

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescoretimewise import TreeScoreTimewise


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        self.score.add_measure(TreeMeasure(time=(5, 4)))
        sf = SimpleFormat(quarter_durations=[5])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        self.score.finish()
        output = []
        for measure in self.score.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                for beat in part.get_beats():
                    output.append([ch.quarter_duration for ch in beat.chords])

        result = [[Fraction(3, 1)], [], [], [Fraction(2, 1)], []]
        self.assertEqual(output, result)