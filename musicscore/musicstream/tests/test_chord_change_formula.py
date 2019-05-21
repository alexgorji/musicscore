import math
from unittest import TestCase
import os

from musicscore.musicstream.equations import AGCos, AGLinear
from musicscore.musicstream.streamvoice import SimpleFormat, StreamChordFormula
from musicscore.musictree.midi import Midi
from musicscore.musictree.treescore_timewise import TreeScoreTimewise
from musicscore.musicxml.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class CosChord(AGCos, StreamChordFormula):
    @staticmethod
    def condition(chord):
        return True

    def __init__(self, frequency, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chord_position = 0
        self.a = 6
        self.c = 6
        self.b = None
        self.frequency = frequency

    def change_chord(self, chord):
        if self.condition(chord):
            if callable(self.frequency):
                frequency = self.frequency(self._chord_position)
            else:
                frequency = self.frequency

            self.b = 1 / (2 * frequency)
            cos = self.get_y(self._chord_position)
            self._chord_position += chord.quarter_duration
            value = 60 + cos
            value = round(value * 2) / 2
            chord.midis = [Midi(value)]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(durations=20 * [0.5])
        sf.change_chord(CosChord(1 / 10))
        for chord in sf.chords:
            chord.add_lyric(chord.midis[0].value)

        v = sf.to_voice(1)

        v.add_to_score(self.score, 1, 1)

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        sf = SimpleFormat(durations=20 * [0.5])
        cos = CosChord(frequency=AGLinear(a=0, b=1 / 10).get_y)
        sf.change_chord(cos)
        for chord in sf.chords:
            chord.add_lyric(chord.midis[0].value)

        v = sf.to_voice(1)

        v.add_to_score(self.score, 1, 1)

        result_path = path + '_test_2'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
