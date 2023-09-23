"""Lyrics assigned to the voices of a piano staff containing two simple staves. Each staff is assigned exactly one
lyrics line."""
from pathlib import Path

from musicscore import Score, A, Chord, F, Lyrics
from musicscore.tests.util import IdTestCase


class TestLily61c(IdTestCase):
    def test_lily_61c_Lyrics_Pianostaff(self):
        score = Score()
        part = score.add_part('p1')
        chords_1 = [Chord(A(4), 1) for _ in range(4)]
        chords_2 = [Chord(F(3), 1) for _ in range(4)]
        Lyrics([('tra', 'la', 'li'), 'ja!']).add_to_chords(chords_1)
        Lyrics([('TRA', 'LA', 'LI'), 'JA!']).add_to_chords(chords_2)

        [part.add_chord(ch, staff_number=1) for ch in chords_1]
        [part.add_chord(ch, staff_number=2) for ch in chords_2]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
