from unittest import TestCase

from musicscore.musicstream import SimpleFormat, TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
import os

from musicscore.musicxml.elements.note import Notehead
from tests.score_templates.xml_test_score import TestScore

xml_path = os.path.abspath(__file__).split('.')[0] + '.xml'


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(durations=[1, 2, 3, 2, 1])
        TreeChord()
        sf.chords[1].add_child(Notehead('square'))
        sf.chords[2].add_child(Notehead('diamond'))
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)
