"""
Different kinds of grace notes: acciaccatura, appoggiatura; beamed grace notes; grace notes with
accidentals; different durations of the grace notes.
"""
from pathlib import Path

from musicscore import Score, C, Chord, F, E, D, A
from musicscore.chord import GraceChord
from musicscore.tests.util import IdTestCase
from musicxml.xmlelement.xmlelement import XMLSlur


class TestLily24a(IdTestCase):
    def test_lily_24a_GraceNote(self):
        score = Score()
        p = score.add_part('p1')
        measure_1_chords = [Chord(C(5), qd) for qd in [1, 1, 1, 1]]

        measure_1_chords[0].add_grace_chord(D(5), '16th')

        measure_1_chords[1].add_grace_chord(E(5), '16th')
        measure_1_chords[1].add_grace_chord(D(5), '16th')

        measure_1_chords[2].add_grace_chord(D(5), '16th')

        measure_1_chords[3].add_grace_chord(D(5), 'eighth')

        measure_2_chords = [Chord(C(5), qd) for qd in [1, 2, 0.5, 0.5]]

        measure_2_chords[0].add_grace_chord(D(5), '16th').add_x(XMLSlur(type='start'))
        measure_2_chords[0].add_x(XMLSlur(type='stop'))

        measure_2_chords[1].add_grace_chord(E(5), '16th')
        measure_2_chords[1].add_grace_chord(D(5), '16th')

        measure_2_chords[2].add_grace_chord(D(5), '16th').add_x(XMLSlur(type='start'))
        measure_2_chords[2].add_x(XMLSlur(type='stop'))

        measure_2_chords[3].add_grace_chord(D(5), '16th').add_x(XMLSlur(type='start'))
        measure_2_chords[3].add_x(XMLSlur(type='stop'))
        measure_2_chords[3].add_grace_chord(E(5), '16th', position='after')

        measure_3_chords = [Chord([F(4), C(5)], 1), Chord(C(5), 1), Chord(C(5), 1), Chord(C(5), 1)]

        measure_3_chords[0].add_grace_chord(E(5), '16th')

        measure_3_chords[1].add_grace_chord(GraceChord(D(5, '#'), type='quarter'))

        measure_3_chords[2].add_grace_chord(GraceChord(D(5, 'b'), type='quarter'))
        measure_3_chords[2].add_grace_chord(GraceChord(A(4, 'b'), type='quarter'))

        for chord in measure_1_chords + measure_2_chords + measure_3_chords:
            p.add_chord(chord)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
