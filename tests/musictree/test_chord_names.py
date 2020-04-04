from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        sf = SimpleFormat(quarter_durations=[1, 1])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, part_number=1, first_measure=1)

        sf = SimpleFormat(quarter_durations=[1, 1])
        v = sf.to_stream_voice(2)
        v.add_to_score(self.score, part_number=1, first_measure=1)

        sf = SimpleFormat(quarter_durations=[1, 1])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, part_number=2, first_measure=2)

    def test_1(self):
        chord = self.score.get_measure(1).get_part(1).get_staff(1).get_voice(1).chords[1]
        self.assertEqual(chord.__name__, '1.1.1.2')
        chord = self.score.get_measure(1).get_part(1).get_staff(1).get_voice(2).chords[0]
        self.assertEqual(chord.__name__, '1.1.2.1')
        chord = self.score.get_measure(2).get_part(2).get_staff(1).get_voice(1).chords[1]
        self.assertEqual(chord.__name__, '2.2.1.2')
