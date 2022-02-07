from pathlib import Path
from unittest import TestCase

from musictree.accidental import Accidental
from musictree.chord import Chord
from musictree.exceptions import VoiceIsAlreadyFullError
from musictree.measure import Measure
from musictree.midi import G, A, B, C, D, E, F, Midi
from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import IdTestCase


class TestPitchPitch(IdTestCase):
    def test_pitches_pitches(self):
        """
        All pitches from G to c'''' in ascending steps; First without accidentals, then with a sharp and then with a flat accidental, then
        with explicit natural accidentals. Double alterations and cautionary accidentals are tested at the end.
        """
        score = Score()
        part = score.add_child(Part('p1'))
        steps = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        octaves = [3, 4, 5, 6]
        midi_notes_without_accidental = [G(2), A(2), B(2)] + [eval(step)(octave) for octave in octaves for step in steps] + [C(7)]
        chords = [Chord(midis=m, quarter_duration=1) for m in midi_notes_without_accidental]
        sharp_chords = [Chord(midis=Midi(m.value + 1, accidental=Accidental(mode='sharp')), quarter_duration=1) for m in
                        midi_notes_without_accidental]
        flat_chords = [Chord(midis=Midi(m.value - 1, accidental=Accidental(mode='flat')), quarter_duration=1) for m in
                       midi_notes_without_accidental]
        chords.extend(sharp_chords)
        chords.extend(flat_chords)
        m = part.add_child(Measure(1))
        for ch in chords:
            try:
                m.add_chord(ch)
            except VoiceIsAlreadyFullError:
                m = part.add_child(Measure(m.number + 1))
                m.add_chord(ch)
        score.update_xml_notes()
        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
