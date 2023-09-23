"""
Multiple (simple) lyrics. The order of the exported stanzas is relevant (identified by the
number attribute in this test case)
"""
from pathlib import Path

from musicscore import Score, G, Chord, Lyrics
from musicscore.tests.util import IdTestCase


class TestLily61b(IdTestCase):
    def test_lily_61b_Lyrics(self):
        score = Score()
        part = score.add_part('p1')
        chords = [Chord(G(4), 1) for _ in range(8)]
        lyrics_1 = [('Tra', 'la', 'la,',), ('ja!', None), ('Tra', 'ra'), '...']
        lyrics_2 = [('Tra', 'la', 'la,',), ('ja!', None), ('Tra', 'ra'), '...']
        lyrics_3 = [('TRA', 'LA', 'LA,',), ('JA!', None), ('TRA', 'Ra'), '...']
        Lyrics(lyrics_1, number=1, show_number=True).add_to_chords(chords)
        Lyrics(lyrics_2, number=2, show_number=True).add_to_chords(chords)
        Lyrics(lyrics_3, number=3, show_number=True).add_to_chords(chords)
        [part.add_chord(ch) for ch in chords]
        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
