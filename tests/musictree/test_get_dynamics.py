import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.elements.note import Notations, Duration
from musicscore.musicxml.types.complextypes.dynamics import FF, Dynamics
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):

    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        chord = TreeChord()
        chord.add_dynamics('ff')
        self.assertEqual(chord.get_dynamics(), 'ff')


