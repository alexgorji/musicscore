from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.elements.note import Lyric
from tests.score_templates.xml_test_score import TestScore
from musicscore.musicxml.types.complextypes.lyric import Text

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):

    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        simpleformat = SimpleFormat(midis=list(range(60, 68)))
        voice = simpleformat.to_stream_voice(2)
        self.score.add_part()
        self.score.add_measure()
        voice.add_to_score(self.score, 1)
        result_path = path + '_test_1'
        # self.score.accidental_mode = 'modern'
        self.score.write(result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        simpleformat = SimpleFormat(midis=list(range(60, 68)), quarter_durations=[1.2] * 8)
        voice = simpleformat.to_stream_voice(1)
        self.score.add_part()
        self.score.add_measure()
        voice.add_to_score(self.score, 1)
        result_path = path + '_test_2'
        self.score.write(result_path)
        TestScore().assert_template(result_path=result_path)

    def test_3(self):
        sf = SimpleFormat(midis=[(60, 61, 67)], quarter_durations=7)
        voice = sf.to_stream_voice(1)
        voice.add_to_score(self.score, 1)
        result_path = path + '_test_3'
        self.score.write(result_path)
        TestScore().assert_template(result_path=result_path)

    def test_4(self):
        midis = list(range(60, 80))
        sf = SimpleFormat(midis=midis)
        for chord in sf.chords:
            l = chord.add_child(Lyric())
            l.add_child(Text(str(chord.midis[0].value)))
        voice = sf.to_stream_voice(1)
        voice.add_to_score(self.score, 1)
        result_path = path + '_test_4'
        self.score.write(result_path)
        TestScore().assert_template(result_path=result_path)
