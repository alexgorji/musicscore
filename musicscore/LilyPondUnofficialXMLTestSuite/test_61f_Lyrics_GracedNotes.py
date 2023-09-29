"""
Grace notes shall not mess up the lyrics, and they shall not be assigned a syllable.
"""

from pathlib import Path

from musicscore import Score, Chord, G, D, C, E, Lyrics
from musicscore.tests.util import IdTestCase
from musicscore.util import slur_chords


class TestLily61f(IdTestCase):
    def test_lily_61f_Lyrics_GraceNotes(self):
        score = Score()
        part = score.add_part('p1')
        chords = [Chord(G(4), 1), Chord(C(5), 1), Chord(C(5), 1), Chord(C(5), 1),
                  Chord(C(5), 1), Chord(C(5), 1), Chord(C(5), 1), Chord(C(5), 1)]
        chords[1].add_grace_chord(D(5))
        chords[3].add_grace_chord(D(5))
        chords[5].add_grace_chord(E(5))
        chords[5].add_grace_chord(D(5))
        chords[6].add_grace_chord(D(5))

        slur_chords([chords[0], chords[1]])
        slur_chords([chords[4], chords[5]])
        slur_chords([chords[1].get_grace_chords()[0], chords[1]], number=2)
        slur_chords([chords[3].get_grace_chords()[0], chords[3]], number=1)
        [part.add_chord(ch) for ch in chords]

        Lyrics([('Ly', None, None, 'rics'), None, 'on', ('Notes', None)]).add_to_chords(chords)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
