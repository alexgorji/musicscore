"""
Tempo Markings: note=bpm, text (note=bpm), note=note, (note=note), (note=bpm)
"""
from pathlib import Path

from musicscore import Score, Chord
from musicscore.metronome import Metronome
from musicscore.tests.util import IdTestCase


class TestLily31c(IdTestCase):
    def test_lily_31c_MetronomeMarks(self):
        score = Score()
        part = score.add_part('p1')
        [part.add_chord(Chord(72, 2)) for _ in range(5)]
        chords = part.get_chords()

        chords[0].metronome = Metronome(per_minute=100, beat_unit=1.5)
        # chords[1].metronome = Metronome(per_minute=100, beat_unit=8, parenthesis=True, relative_x=40)
        # chords[1].add_words('Adagio', placement='above')
        # chords[2].metronome = Metronome(per_minute=None, beat_unit=1.5, second_beat_unit=3)
        # chords[3].metronome = Metronome(per_minute=None, beat_unit=1.5, second_beat_unit=3, parenthesis=True)
        # chords[0].metronome = Metronome(per_minute=77, beat_unit=1.5, parenthesis=True)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
