from unittest import TestCase

from musictree.midi import G, A, B, C, D, E, F
from musictree.part import Part
from musictree.score import Score


class TestPitchPitch(TestCase):
    def test_pitches_pitches(self):
        """
        All pitches from G to c'''' in ascending steps; First without accidentals, then with a sharp and then with a flat accidental, then
        with explicit natural accidentals. Double alterations and cautionary accidentals are tested at the end.
        """
        score = Score()
        part = score.add_child(Part)
        steps = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        octaves = [2, 3, 4, 5]
        midi_notes_without_accidental = [G(2), A(2), B(2)] + [eval(step)(octave) for octave in octaves for step in steps] + [C(6)]

        print(len(midi_notes_without_accidental))
        print(midi_notes_without_accidental)
