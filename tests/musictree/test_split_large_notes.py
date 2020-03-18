from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechordflags1 import BeatwiseFlag1
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        durations = [5]
        self.score.set_time_signatures(times={1: (5, 4)})
        sf = SimpleFormat(quarter_durations=durations)

        sf.to_stream_voice().add_to_score(self.score, part_number=1)
        sf.chords[0].add_flag(BeatwiseFlag1())
        sf.to_stream_voice().add_to_score(self.score, part_number=2)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_2(self):
        # todo
        xml_path = path + '_test_2.xml'
        durations = [4, 5, 6, 7, 8, 9, 10]
        self.score.set_time_signatures(
            times={1: (4, 4), 2: (5, 4), 3: (6, 4), 4: (7, 4), 5: (8, 4), 6: (9, 4), 7: (10, 4)})
        sf = SimpleFormat(quarter_durations=durations)

        sf.to_stream_voice().add_to_score(self.score, part_number=1)
        for chord in sf.chords:
            chord.add_flag(BeatwiseFlag1())
        sf.to_stream_voice().add_to_score(self.score, part_number=2)

        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)

    def test_3(self):
        xml_path = path + '_test_3.xml'
        durations = [0.5, 1.5]
        self.score.set_time_signatures(quarter_durations=2)
        sf = SimpleFormat(quarter_durations=durations)
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_4(self):
        xml_path = path + '_test_4.xml'
        durations = [0.5, 1.5]
        self.score.set_time_signatures(quarter_durations=2)
        sf = SimpleFormat(quarter_durations=durations, midis=[60, 0])
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_5(self):
        xml_path = path + '_test_5.xml'
        durations = [0.5, 3.5]
        sf = SimpleFormat(quarter_durations=durations, midis=[60, 0])
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)

    def test_6(self):
        xml_path = path + '_test_6.xml'
        durations = [0.5, 1.5, 2]
        sf = SimpleFormat(quarter_durations=durations, midis=[60, 0, 60])
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
