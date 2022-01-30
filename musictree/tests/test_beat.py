from unittest import TestCase

from musictree.beat import Beat
from musictree.chord import Chord
from musictree.exceptions import BeatException, BeatWrongDurationError, BeatIsFullError
from musictree.voice import Voice


class TestBeat(TestCase):
    def test_beat_quarter_duration(self):
        b = Beat()
        assert b.quarter_duration == 1
        b.quarter_duration = 4
        assert b.quarter_duration == 4
        # quarter_durations = [1 / 64, 3 / 64, 1 / 32, 3 / 32, 1 / 16, 3 / 16, 1 / 8, 3 / 8, 1 / 4, 3 / 4, 1 / 2, 1, 2, 3]
        # for quarter_duration in quarter_durations:
        #     b.quarter_duration = quarter_duration
        # wrong_quarter_durations = [1/3, 2/5, ]
        # with self.assertRaises(ValueError):
        #     b.quarter_duration = 3
        # with self.assertRaises(BeatException):
        #     b.quarter_duration = 3
        # with self.assertRaises(BeatWrongDurationError):
        #     b.quarter_duration = 3

    # def test_beat_add_chord(self):
    #     b = Beat()
    #     assert b.filled_quarter_duration == 0
    #     b.add_child(Chord(quarter_duration=0.5))
    #     assert b.filled_quarter_duration == 0.5
    #     b.add_child(Chord(quarter_duration=0.5))
    #     assert b.filled_quarter_duration == 1
    #     with self.assertRaises(BeatIsFullError):
    #         b.add_child(Chord(quarter_duration=1))
    #
    #     b = Beat()
    #     b.add_child(Chord(quarter_duration=2))
    #     with self.assertRaises(BeatIsFullError):
    #         b.add_child(Chord(quarter_duration=1))

    def test_beat_previous(self):
        b = Beat()
        assert b.previous is None
        v = Voice()
        v.update_beats(1 / 4, 1 / 8, 1 / 2, 1)
        assert v.get_children()[0].previous is None
        assert v.get_children()[1].previous.quarter_duration == 1 / 4
        assert v.get_children()[2].previous.quarter_duration == 1 / 8
        assert v.get_children()[3].previous.quarter_duration == 1 / 2

    def test_beat_next(self):
        b = Beat()
        assert b.next is None
        v = Voice()
        v.update_beats(1 / 4, 1 / 8, 1 / 2, 1)
        assert v.get_children()[0].next.quarter_duration == 1 / 8
        assert v.get_children()[1].next.quarter_duration == 1 / 2
        assert v.get_children()[2].next.quarter_duration == 1
        assert v.get_children()[3].next is None

    def test_beat_offset(self):
        b = Beat()
        assert b.offset is None
        v = Voice()
        v.update_beats(1 / 4, 1 / 8, 1 / 2, 1)
        assert v.get_children()[0].offset == 0
        assert v.get_children()[1].offset == 1 / 4
        assert v.get_children()[2].offset == 1 / 4 + 1 / 8
        assert v.get_children()[3].offset == 1 / 4 + 1 / 8 + 1 / 2
