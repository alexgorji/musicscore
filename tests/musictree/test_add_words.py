import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.groups.musicdata import Direction
from musicscore.musicxml.types.complextypes.direction import DirectionType
from musicscore.musicxml.types.complextypes.directiontype import Words
from tests.score_templates.xml_test_score import TestScore
from musicscore.musictree.wordsymbols import SALTANDO

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[1, 1])

        sf.chords[0].add_words('first word')
        sf.chords[1].add_words('second word', font_family='DejaVu Sans', font_size=14, font_weight='bold',
                               font_style='italic')

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[1, 1])

        sf.chords[0].add_words('a')
        sf.chords[1].add_words('b')
        sf.chords[0].add_words('aa', relative_y=-15)

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_2'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_3(self):
        sf = SimpleFormat(quarter_durations=[1.95, 2.05])

        sf.chords[0].add_words('a')
        sf.chords[1].add_words('b')
        sf.chords[0].add_words('aa', relative_y=-15)

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_3'
        self.score.write(path=result_path)
        # TestScore().assert_template(result_path=result_path)

    def test_4(self):
        sf = SimpleFormat(quarter_durations=[2])

        chord = sf.chords[0]
        d = chord.add_child(Direction(placement='above'))
        dt = d.add_child(DirectionType())
        dt.add_child(Words('A', font_size=10))
        dt.add_child(Words('B', font_size=20))

        v = sf.to_stream_voice().add_to_score(self.score)

        result_path = path + '_test_4'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_5(self):
        sf = SimpleFormat(quarter_durations=[2])
        sf.chords[0].add_words(SALTANDO)

        sf.to_stream_voice().add_to_score(self.score)

        result_path = path + '_test_5'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
