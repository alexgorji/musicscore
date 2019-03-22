from unittest import TestCase

from musicscore.musictree.midi import Midi
from musicscore.musictree.treenote import TreeNote
from musicscore.musictree.treetimewise import TreeScoreTimewise
import os

path = os.path.abspath(__file__).split('.')[0]


class TestGrouping(TestCase):
    def setUp(self):
        self.score = TreeScoreTimewise()
        self.score.add_part('one')

    def test_grouping(self):
        for i in range(2):
            self.make_measure()
        self.score.finish()
        print(self.score.to_string())
        self.score.write(path=path)

    def make_measure(self):
        self.score.add_measure()
        for i in range(8):
            self.score.add_note(1, 1, TreeNote(event=Midi(60).get_pitch_rest(), quarter_duration=0.5))
