from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescore_timewise import TreeScoreTimewise

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        midis = [(60, 63, 65), 80]
        sf = SimpleFormat(midis=midis)
        voice = sf.to_voice(1)
        l = voice.chords[0].add_lyric('bla')

        voice.add_to_score(self.score, 1, 1)
        self.score.write(path=path + '_test_1')
        # print(self.score.to_string())

    def test_2(self):
        midis = [(60, 63, 65), 80]
        sf = SimpleFormat(midis=midis)
        voice = sf.to_voice(1)
        voice.chords[0].add_lyric('bla')
        voice.chords[0].add_lyric('bb', number=2)

        voice.add_to_score(self.score, 1, 1)
        self.score.write(path=path + '_test_2')
        # print(self.score.to_string())

    def test_3(self):
        midis = [(60, 63, 65), 80]
        sf = SimpleFormat(midis=midis)
        voice1 = sf.to_voice(1)
        voice1.chords[0].add_lyric('bla')
        voice1.chords[0].add_lyric('bb', number=2)
        voice1.add_to_score(self.score, 1, 1)

        midis = [90, (91, 92)]
        sf = SimpleFormat(midis=midis)
        voice2 = sf.to_voice(2)
        voice2.chords[1].add_lyric('sh')
        voice2.chords[1].add_lyric('th', number=2)
        voice2.add_to_score(self.score, 1, 1)

        self.score.write(path=path + '_test_3')
        # print(self.score.to_string())
