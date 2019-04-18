from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescore_timewise import TreeScoreTimewise


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        midis = [(60,63,65), 80]
        sf = SimpleFormat(midis=midis)
        voice = sf.to_voice(1)
        l = voice.chords[0].add_lyric('bla')

        voice.add_to_score(self.score, 1, 1)
        print(self.score.to_string())


