import os
import warnings
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescore_timewise import TreeScoreTimewise
from musicscore.musicxml.groups.common import Voice
from musicscore.musicxml.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        chord = TreeChord()
        chord.add_child(Voice('1'))
        chord.remove_voice()
        self.assertEqual(chord.get_children(), [])
