from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test(self):
        simpleformat = SimpleFormat(quarter_durations=4)
        voice = simpleformat.to_stream_voice(1)
        voice.add_to_score(self.score)
        # print(voice.chords)
        # print(self.score.to_string())