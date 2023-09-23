"""Beaming or slurs can indicate melismata for lyrics. Also make sure that notes without an explicit syllable are
treated as if they were part of a melisma."""

"""
Chord.break_beam() will be needed. Otherwise breaking the beams like in this test will effect all staves and voices
"""

from pathlib import Path

from musicscore import Score, Chord, A, Time
from musicscore.lyrics import Lyrics
from musicscore.tests.util import IdTestCase
from musicscore.util import slur_chords


class TestLily61h(IdTestCase):
    def test_lily_61h_BeamsMelismata(self):
        score = Score()
        part = score.add_part('p1')
        t = Time(4, 4)
        t.actual_signatures = (3, 8, 1, 8, 3, 8, 1, 8)
        part.add_measure(time=t)
        t = Time(4, 4)
        t.actual_signatures = 8 * [1, 8]
        part.add_measure(time=t)

        midi_pattern = [72, 69, 72, 69, 72, 67, 71, 0]
        chords = []
        for _ in range(4):
            chords += [Chord(m, 0.5) for m in midi_pattern]

        [part.add_chord(ch) for ch in chords]

        third_measure_chords = part.get_measure(measure_number=3).get_chords()
        slur_chords(third_measure_chords[:3])
        slur_chords(third_measure_chords[4:7])

        fourth_measure_chords = part.get_measure(measure_number=4).get_chords()
        slur_chords(fourth_measure_chords[:7])

        lyrics_pattern = [('Me', None, None, 'lis', 'ma', None, None)]
        for m in part.get_children():
            Lyrics(lyrics_pattern).add_to_chords(m.get_chords()[:-1])

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
