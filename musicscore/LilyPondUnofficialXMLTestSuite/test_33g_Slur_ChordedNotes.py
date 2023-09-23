"""
Slurs on chorded notes: Only the first note of the chord should get the slur notation. Some applications print out
the slur for all notes – these should be ignored.
"""
from pathlib import Path

from musicscore import Score, Chord, G, C, A, D
from musicscore.tests.util import IdTestCase
from musicscore.util import slur_chords


class TestLily33g(IdTestCase):
    def test_lily_33g_Slur_ChordedNotes(self):
        score = Score()
        part = score.add_part('p1')

        chords = [Chord(m, 1) for m in [[G(4), C(5), G(5)], [A(4), D(5)], [G(4), D(5)], C(5)]]

        slur_chords(chords[:3], number=1)
        slur_chords(chords[2:], number=2)

        [part.add_chord(ch) for ch in chords]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
