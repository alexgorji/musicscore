from fractions import Fraction
from pathlib import Path

from musicscore.chord import Chord
from musicscore.lyrics import Lyrics
from musicscore.score import Score
from musicscore.tests.util import XMLTestCase


qds = [
    Fraction(16, 45),
    Fraction(4, 9),
    Fraction(4, 9),
    Fraction(16, 45),
    Fraction(4, 15),
    Fraction(4, 3),
    Fraction(16, 15),
    Fraction(32, 63),
    Fraction(128, 315),
    Fraction(32, 105),
    Fraction(128, 315),
    Fraction(32, 63),
    Fraction(32, 21),
    Fraction(64, 105),
    Fraction(16, 27),
    Fraction(64, 135),
    Fraction(16, 45),
    Fraction(16, 45),
    Fraction(64, 135),
    Fraction(16, 27),
    Fraction(16, 9),
    Fraction(32, 45),
    Fraction(32, 27),
    Fraction(32, 81),
    Fraction(32, 135),
    Fraction(128, 405),
]

words = [
    ("die", None),
    ("wil", None, None, "de"),
    ("Kla", "ge", None, None),
    ("ih", None, "rer"),
    None,
    ("zer", None, "bro", "che", None, None, "nen"),
    None,
    ("Mün", "der", None, None),
]

path = Path(__file__)


class LyricsTestCase(XMLTestCase):
    def setUp(self):
        self.score = Score()
        self.part = self.score.add_part("P1")

    def test_add_words(self):
        lyric = Lyrics(words)
        chords = [
            Chord(0, qd) if index in [13, 21] else Chord(60, qd)
            for index, qd in enumerate(qds)
        ]
        lyric.add_to_chords(chords)
        for chord in chords:
            self.part.add_chord(chord)
        self.score.get_quantized = True
        self.score.simplified_sextuplets = True
        self.score.set_possible_subdivisions([2, 3, 4, 6])

        with self.file_path(path, "add_words") as xml_path:
            self.score.export_xml(xml_path)
