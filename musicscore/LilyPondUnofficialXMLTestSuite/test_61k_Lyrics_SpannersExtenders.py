"""Lyrics spanners: continued syllables and extenders, possibly spanning multiple notes. The intermediate notes do
not have any <lyric> element."""

from pathlib import Path

from musicscore import Score, Chord
from musicscore.lyrics import Lyrics
from musicscore.tests.util import IdTestCase


class TestLily61k(IdTestCase):
    def test_lily_61h_Lyrics_SprannersExtenders(self):
        score = Score()
        part = score.add_part('p1')

        chords = [Chord(72, 1) for _ in range(11)]
        chords.append(Chord(0, 1))

        Lyrics([('A', None), ('b', None, None, 'CC', None, None), ('e', None, None)]).add_to_chords(chords[:-1])

        [part.add_chord(ch) for ch in chords]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
