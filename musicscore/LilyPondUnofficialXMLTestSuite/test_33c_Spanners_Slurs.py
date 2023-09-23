"""
A note can be the end of one slur and the start of a new slur. Also, in MusicXML, nested slurs are possible like
in the second measure where one slur goes over all four notes, and another slur goes from the second to the third
note."""
from pathlib import Path

from musicscore import Score, A, C, G, Chord
from musicscore.tests.util import IdTestCase
from musicscore.util import slur_chords


class TestLily33c(IdTestCase):
    def test_lily_33c_Spanners_Slurs(self):
        score = Score()
        part = score.add_part('p1')
        midis = [G(4), C(5), A(4), G(4), G(4), C(5), A(4), G(4)]
        chords = [Chord(m, 1) for m in midis]
        slur_chords(chords[:2])
        slur_chords(chords[1:3])
        slur_chords(chords[2:4])

        slur_chords(chords[4:])
        slur_chords(chords[5:7], number=2)
        [part.add_chord(ch) for ch in chords]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
