from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[0, 4])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        result_path = path + '_test_1'
        self.score.write(path=result_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[1, 0, 3])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        result_path = path + '_test_2'
        self.score.write(path=result_path)

    def test_3(self):
        sf = SimpleFormat(quarter_durations=[4, 0])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        result_path = path + '_test_3'
        self.score.write(path=result_path)

    def test_4(self):
        sf = SimpleFormat(quarter_durations=[1.5, 0, 2.5])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        result_path = path + '_test_4'
        self.score.write(path=result_path)

    def test_5(self):
        sf = SimpleFormat(quarter_durations=[1.75, 0, 2.25])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        result_path = path + '_test_5'
        self.score.write(path=result_path)

    def test_6(self):
        sf = SimpleFormat(quarter_durations=[1.75, 0, 2, 0, 4.25])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        result_path = path + '_test_6'
        self.score.write(path=result_path)

    def test_7(self):
        sf = SimpleFormat(quarter_durations=[1.3, 0, 2, 0, 0.7])
        for index, chord in enumerate(sf.chords):
            chord.add_lyric(index + 1)
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        # self.score.fill_with_rest()
        # self.score.add_beats()
        # self.score.quantize()
        # self.score.split_not_notatable()
        # self.score.update_tuplets()
        # self.score.substitute_sextoles()
        # self.score.update_types()
        # self.score.update_dots()
        # self.score.chord_to_notes()
        # self.score.update_divisions()
        # self.score.update_accidentals(mode='normal')
        # self.score.update_durations()
        # self.score.finish()
        result_path = path + '_test_7'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
