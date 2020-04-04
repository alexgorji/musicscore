import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def make_t(self, *args):
        sf = SimpleFormat(quarter_durations=[1, 1, 1, 1], midis=[0, 0, 0, 0])
        for i in range(3):
            sf.chords[i].is_adjoinable = args[i]
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        self.score.add_subtitle(str([chord.is_adjoinable for chord in sf.chords]))

    def test_1(self):
        self.make_t(False, False, False)
        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        self.make_t(False, False, True)
        result_path = path + '_test_2'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_3(self):
        self.make_t(False, True, False)
        result_path = path + '_test_3'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_4(self):
        self.make_t(False, True, True)
        result_path = path + '_test_4'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_5(self):
        self.make_t(True, False, False)
        result_path = path + '_test_5'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_6(self):
        self.make_t(True, False, True)
        result_path = path + '_test_6'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_7(self):
        self.make_t(True, True, False)
        result_path = path + '_test_7'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_8(self):
        self.make_t(True, True, True)
        result_path = path + '_test_8'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_9(self):
        sf = SimpleFormat(quarter_durations=[0.2, 0.8, 1, 1], midis=[0, 0, 0, 60])
        sf.to_stream_voice().add_to_score(self.score)
        result_path = path + '_test_9'
        self.score.write(path=result_path)
        # TestScore().assert_template(result_path=result_path)

    def test_10(self):
        sf = SimpleFormat(quarter_durations=[0.5, 2.5], midis=[60, 0])
        self.score.set_time_signatures(quarter_durations=[3])
        sf.to_stream_voice().add_to_score(self.score)
        result_path = path + '_test_10'
        self.score.write(path=result_path)
