import os
import random
from unittest import TestCase

from musicscore.musicstream.equations import AGCos, AGLinear
from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class CosDelta(AGCos):

    def __init__(self, frequency, b=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frequency = frequency
        self.b = b

    @AGCos.b.setter
    def b(self, value):
        self._b = value

    def get_b(self, x):
        if self.b is None:
            return AGLinear(0, 1 / (2 * self.get_frequency(x)))(x)
        elif callable(self.b):
            return self.b(x)
        else:
            return self.b


class Test(TestCase):
    # def test_1(self):
    #     cd1 = AGCos(frequency=0.3, a=1, c=0)
    #     cd2 = AGCos(frequency=0.2, a=0.5, c=0)
    #     cd3 = AGCos(frequency=0.1, a=0.25, c=0)
    #     fr1 = AGCos(frequency=0.03, a=0.125, c=0)
    #     cd4 = AGCos(frequency=fr1, a=2, c=0)
    #
    #     number_of_dots = 8000
    #     delta = 1 / 100
    #
    #     xs = [x * delta for x in range(number_of_dots)]
    #
    #     # plt.plot(xs, [cd1(x) for x in xs])
    #     # plt.plot(xs, [cd2(x) for x in xs])
    #     # plt.plot(xs, [cd3(x) for x in xs])
    #     # plt.plot(xs, [cd4(x) for x in xs])
    #     plt.plot(xs, [fr1(x) for x in xs])
    #     plt.plot(xs, [cd1(x)+cd2(x)+cd3(x)+cd4(x) for x in xs], 'black')
    #     # plt.plot(xs, [frequency(x) for x in xs])
    #
    #     plt.show()

    # def test_2(self):
    #     duration = 20
    #     number_of_dots = duration * 100
    #     delta = 1 / 100
    #
    #     period = 10
    #     cd1 = CosDelta(frequency=1/period, a=6, b=None, c=6)
    #
    #     period = 2
    #     cd2 = CosDelta(frequency=1/period, a=0.5, b=3, c=0)
    #
    #     xs = [x * delta for x in range(number_of_dots)]
    #     plt.plot(xs, [cd1(x) for x in xs])
    #     plt.plot(xs, [cd2(x) for x in xs])
    #
    #     plt.plot(xs, [cd1(x)*cd2(x) for x in xs], 'black')
    #
    #     plt.show()

    def test_3(self):
        score = TreeScoreTimewise()
        score.max_division = 6

        random.seed(101)
        durations = [random.random() * 3 for i in range(20)]

        midis = [round(55 + random.random() * 12) for i in range(20)]
        sf = SimpleFormat(durations=durations, midis=midis)

        v = sf.to_voice(1)
        v.add_to_score(score, 1, 1)

        sf = SimpleFormat(durations=durations, midis=midis)
        period = sum(durations) / 3
        cd1 = CosDelta(frequency=1 / period, a=3, b=None, c=3)

        period = sum(durations) / 2
        cd2 = CosDelta(frequency=1 / period, a=3, b=None, c=3)

        chord_position = 0
        for chord in sf.chords:
            if chord.midis[0].value <= 60:
                chord.midis[0].value += round(cd1(chord_position))
            else:
                chord.midis[0].value -= round(cd2(chord_position))
            chord_position += chord.quarter_duration

        v = sf.to_voice(1)
        v.add_to_score(score, 1, 2)

        result_path = path + '_test_3'
        score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
