"""
All types of octave shifts (15ma, 15mb, 8va, 8vb)
"""
from pathlib import Path

from musicscore import Score, Chord, C, A, B
from musicscore.tests.util import IdTestCase
from musicscore.util import octave_chords


class TestLily33d(IdTestCase):
    def test_lily_33d_Spanners_OctaveShifts(self):
        score = Score()
        part = score.add_part('p1')
        midis = [A(4), C(5), A(6), C(3), B(2), A(5), A(5), B(3), C(4)]
        quarter_durations = 7 * [0.5] + 2 * [0.25]
        chords = [Chord(m, d) for m, d in zip(midis, quarter_durations)]

        octave_chords(chords[2], size=15)
        octave_chords(chords[3:5], type='up', size=15)
        octave_chords(chords[5:7], type='down', size=8)
        octave_chords(chords[7:], type='up', size=8)


        [part.add_chord(ch) for ch in chords]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
