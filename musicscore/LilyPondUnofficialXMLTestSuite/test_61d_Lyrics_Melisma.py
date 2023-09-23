"""How to treat lyrics and slurred notes. Normally, a slurred group of notes is assigned only one lyrics syllable."""
from pathlib import Path

from musicscore import Score, A, Chord, Lyrics, C, E
from musicscore.tests.util import IdTestCase
from musicscore.util import slur_chords


class TestLily61d(IdTestCase):
    def test_lily_61d_Lyrics_Melisma(self):
        score = Score()
        part = score.add_part('p1')

        midis = [C(5), (A(4), E(5)), C(5), (C(5), E(5)), C(5), C(5), C(5), E(5)]
        chords = [Chord(m, 1) for m in midis]

        [part.add_chord(ch) for ch in chords]

        slur_chords(chords[:4])
        slur_chords(chords[4:6])
        slur_chords(chords[6:])

        lyrics = [('Me', None, None, None, 'lis', None, 'ma.', None)]
        Lyrics(lyrics).add_to_chords(chords)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
