"""
Different kinds of grace notes: acciaccatura, appoggiatura; beamed grace notes; grace notes with
accidentals; different durations of the grace notes.
"""
from pathlib import Path

from musictree import Score, C, Chord, F, E, D, A
from musictree.chord import GraceChord
from musicxml.xmlelement.xmlelement import XMLSlur

score = Score()
p = score.add_part('p1')
measure_1_chords = [GraceChord(C(5), type='16th'), Chord(C(5), 1),
                    GraceChord(C(5), type='16th'), GraceChord(C(5), type='16th'), Chord(C(5), 1),
                    GraceChord(C(5), type='16th'), Chord(C(5), 1),
                    GraceChord(C(5), type='eighth'), Chord(C(5), 1)]
measure_2_chords = [GraceChord(C(5), type='16th'), Chord(C(5), 1),
                    GraceChord(C(5), type='16th'), GraceChord(C(5), type='16th'), Chord(C(5), 2),
                    GraceChord(C(5), type='16th'), Chord(C(5), 0.5),
                    GraceChord(C(5), type='16th'), Chord(C(5), 0.5),
                    GraceChord(C(5), type='16th')]
measure_3_chords = [GraceChord(E(5), type='16th'), Chord([F(4), C(5)], 1),
                    GraceChord(D(5, '#'), type='quarter'), Chord(C(5), 1),
                    GraceChord(D(5, 'b'), type='quarter'), GraceChord(A(4, 'b'), type='quarter'), Chord(C(5), 1),
                    Chord(C(5), 1)]
measure_2_chords[0].add_x(XMLSlur(type='start'))
measure_2_chords[1].add_x(XMLSlur(type='stop'))
measure_2_chords[-5].add_x(XMLSlur(type='start'))
measure_2_chords[-4].add_x(XMLSlur(type='stop'))
measure_2_chords[-3].add_x(XMLSlur(type='start'))
measure_2_chords[-2].add_x(XMLSlur(type='stop'))

for chord in measure_1_chords + measure_2_chords:
    p.add_chord(chord)
for chord in measure_3_chords:
    p.add_chord(chord)

xml_path = Path(__file__).with_suffix('.xml')
score.export_xml(xml_path)
