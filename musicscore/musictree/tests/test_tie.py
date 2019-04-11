from unittest import TestCase

from musicscore.musictree.midi import Midi
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treenote import TreeNote
from musicscore.musictree.treescore_timewise import TreeScoreTimewise


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.score.add_part('one')
        self.score.add_measure(TreeMeasure(time=(2, 4)))

    def test_tie(self):
        note_1 = TreeNote(event=Midi(60).get_pitch_rest(), quarter_duration=0.5)
        note_2 = TreeNote(event=Midi(60).get_pitch_rest(), quarter_duration=0.5, is_tied=True)
        note_3 = TreeNote(event=Midi(60).get_pitch_rest(), quarter_duration=1)
        self.score.add_note(1, 1, note_1)
        self.score.add_note(1, 1, note_2)
        self.score.add_note(1, 1, note_3)

        self.score.finish()
        print(self.score.to_string())
