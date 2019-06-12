import os
from unittest import TestCase

from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.groups.common import Voice

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        chord = TreeChord()
        chord.add_child(Voice('1'))
        chord.remove_voice()
        self.assertEqual(chord.get_children(), [])
