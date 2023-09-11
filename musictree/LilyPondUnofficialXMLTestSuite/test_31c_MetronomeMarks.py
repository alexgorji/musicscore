"""
Tempo Markings: note=bpm, text (note=bpm), note=note, (note=note), (note=bpm)
"""
from pathlib import Path

from musictree import Score, Chord
from musictree.tests.util import IdTestCase


class TestLily31c(IdTestCase):
    def test_lily_31c_MetronomeMarks(self):
        score = Score()
        part = score.add_part('p1')
        [part.add_chord(Chord(72, 2)) for _ in range(5)]
        chords = part.get_chords()
        chords[0].add_metronome(beat_unit=1.5, per_minute=100)

        chords[0].add_metronome(beat_unit=16, per_minute=100, paranthesis=True, text='Adagio')
        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
