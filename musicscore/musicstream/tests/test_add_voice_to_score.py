from unittest import TestCase

from musicscore.musicstream.streamvoice import StreamVoice, SimpleFormat
from musicscore.musictree.treescore_timewise import TreeScoreTimewise


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        for i in range(40):
            self.score.add_measure()

    def test_voice(self):
        # midis = list(range(60, 80))
        midis = [60, 61, 62, 63]
        sf = SimpleFormat(midis=midis)
        print(sf.midis)
        print(sf.durations)
        # voice = sf.to_voice(1)
        # voice.add_to_score(self.score, 1)
        # self.score.to_string()
        # print(self.score.get_measure(1).get_part(1).chords)

