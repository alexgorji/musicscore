from unittest import TestCase

from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescore_timewise import TreeScoreTimewise


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        ch = TreeChord(quarter_duration=0)
        print(ch.get_children())


    def test_2(self):
        self.score.add_measure()
        self.score.add_part()
        self.score.add_chord(1, 1, TreeChord())
        self.score.add_chord(1, 1, TreeChord(quarter_duration=0))


        # p.quantize()
        # print([chord.quarter_duration for chord in p.chords])
        # print(self.score.get_measure(1).get_part(1).chords[1].get_children())

        print(self.score.to_string())
