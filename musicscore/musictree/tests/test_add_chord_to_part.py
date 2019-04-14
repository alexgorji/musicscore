from unittest import TestCase

from quicktions import Fraction

from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musicxml.elements.note import Tie


class Test(TestCase):
    def setUp(self) -> None:
        self.part = TreePart('one')
        self.measure = TreeMeasure()
        self.measure.add_child(self.part)

    def test_add(self):
        chord_1 = TreeChord(quarter_duration=1.5)
        chord_2 = TreeChord(quarter_duration=3.5)
        self.part.add_chord(chord_1)
        remain = self.part.add_chord(chord_2)
        self.part.finish()
        result = [Fraction(1, 1), Fraction(1, 2), Fraction(1, 2), Fraction(2, 1)]
        self.assertEqual([chord.quarter_duration for chord in self.part.chords], result)
        result =['start', 'stop', 'start', 'stop']
        self.assertEqual([tie.type for chord in self.part.chords for tie in chord.get_children_by_type(Tie)], result)
        self.assertEqual(remain.quarter_duration, 1)
        self.assertEqual([tie.type for tie in remain.get_children_by_type(Tie)], ['stop'])