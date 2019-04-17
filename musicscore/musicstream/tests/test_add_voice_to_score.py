from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescore_timewise import TreeScoreTimewise


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()


    def test_1(self):
        simpleformat = SimpleFormat(midis=list(range(60, 68)))
        voice = simpleformat.to_voice(2)
        self.score.add_part()
        self.score.add_measure()
        voice.add_to_score(self.score, 1)
        print(self.score.to_string())

    def test_2(self):
        simpleformat = SimpleFormat(midis=list(range(60, 68)), durations=[1.2]*8)
        voice = simpleformat.to_voice(2)
        self.score.add_part()
        self.score.add_measure()
        voice.add_to_score(self.score, 1)
        p = self.score.get_measure(1).get_part(1)
        print([chord.quarter_duration for chord in p.chords])
        # print(self.score.to_string())


    def test_voice_1(self):
        sf = SimpleFormat(midis=[(60, 61, 67)], durations=7)
        voice = sf.to_voice(1)
        voice.add_to_score(self.score, 1)
        print(self.score.to_string())

    def test_voice_2(self):
        midis = list(range(60, 80))
        # midis = [60, 61, 62, 63]
        sf = SimpleFormat(midis=midis)
        voice = sf.to_voice(1)
        voice.add_to_score(self.score, 1)
        print(self.score.to_string())
        # print(self.score.get_measure(1).get_part(1).chords)
