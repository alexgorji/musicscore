"""
Some notes with simple lyrics: Syllables, notes without a syllable, syllable spanners.
"""
from pathlib import Path

from musictree import Score, Chord, A
from musictree.lyrics import Lyrics
from musictree.tests.util import IdTestCase


class TestLily61a(IdTestCase):
    def test_lily_61a_Lyrics(self):
        score = Score()
        part = score.add_part('p1')

        chords = [Chord(A(4), 1) for _ in range(6)]
        chords.append(Chord(A(4), 2))

        lyrics = Lyrics([('Tra', 'la', 'la'), 'Ja!', ('Tra', 'ra!'), 'Bah'])
        lyrics.add_to_chords(chords)

        [part.add_chord(ch) for ch in chords]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
