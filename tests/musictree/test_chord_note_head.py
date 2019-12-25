from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat, TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
import os

from musicscore.musicxml.elements.note import Notehead
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(durations=[1, 2, 3, 2, 1])
        sf.chords[1].add_child(Notehead('square'))
        sf.chords[2].add_child(Notehead('diamond'))
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_2(self):
        sf = SimpleFormat(midis=[(60, 62, 63)], durations=[4])
        sf.chords[0].add_child(Notehead('diamond'))
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_3(self):
        sf = SimpleFormat(midis=[(60, 62, 63)], durations=[4])
        sf.chords[0].midis[0].notehead = Notehead('diamond')
        sf.chords[0].midis[1].notehead = Notehead('square')
        sf.chords[0].midis[2].notehead = Notehead('normal')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_3.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)
