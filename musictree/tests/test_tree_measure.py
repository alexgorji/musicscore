from unittest import TestCase

from musictree.treechord import TreeChord
from musictree.treemeasure import TreeMeasure


class TestTreeMeasure(TestCase):
    def test_add_chord(self):
        measure = TreeMeasure()
        assert len(measure.chords) == 0
        chord = measure.add_chord()
        assert isinstance(chord, TreeChord)
        assert len(measure.chords) == 1
        assert measure.chords[-1] == chord
