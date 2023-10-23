"""
A trill spanner that spans a grace note and ends on an after-grace note at the end of the measure.
"""
from pathlib import Path

from musicscore import Score, SimpleFormat, E, F, G, A, B
from musicscore.tests.util import IdTestCase
from musicscore.util import trill_chords


class TestLily33a(IdTestCase):
    def test_lily_33a_Spanners(self):
        score = Score()
        part = score.add_part('p1')
        part.add_measure(time=(6, 8))
        simple_format = SimpleFormat(quarter_durations=[1, 1 / 4, 1 / 4, 1.5], midis=[E(5), F(5, '#'), G(5), A(5)])
        chord = simple_format.chords[-1]
        chord.add_grace_chord(B(5), type='16th')
        g = chord.add_grace_chord(G(5), type='16th', position='after')
        chord.add_grace_chord(A(5), type='16th', position='after')
        trill_chords(chords=[chord, g], relative_y=15)
        for ch in simple_format.chords:
            part.add_chord(ch)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
