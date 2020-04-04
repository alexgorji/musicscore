from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.elements.note import Notations
from musicscore.musicxml.types.complextypes.notations import Arpeggiate
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[1], midis=[(60, 64, 67, 70, 72)])
        n = sf.chords[0].add_child(Notations())
        n.add_child(Arpeggiate())

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
