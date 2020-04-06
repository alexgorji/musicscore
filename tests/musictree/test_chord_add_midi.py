from unittest import TestCase

from musicscore.musictree.treechord import TreeChord
from musicscore.musicxml.elements.fullnote import Pitch, Step


class Test(TestCase):
    def setUp(self) -> None:
        self.chord = TreeChord()

    def test_1(self):
        self.chord.add_midi(60)
        steps = [step.value for note in self.chord.notes for pitch in note.get_children_by_type(Pitch) for step in pitch.get_children_by_type(Step)]
        self.assertEqual(steps, ['B', 'C'])
