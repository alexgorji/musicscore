from unittest import TestCase
import os

from quicktions import Fraction

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[1, 1, 1, 1], midis=[60, (61, 62, 63), (64, 65), (67)])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, 1, 1)
        voice = self.score.get_measure(1).get_part(1).get_voice(1)
        self.score.finish()
        result = [0, Fraction(1, 1), Fraction(1, 1), Fraction(1, 1), Fraction(2, 1), Fraction(2, 1), Fraction(3, 1)]
        self.assertEqual([note.offset for xml_chord in voice.xml_chords for note in xml_chord.notes], result)
