from unittest import TestCase

from musictree.beat import Beat
from musictree.chord import Chord
from musictree.exceptions import VoiceHasNoBeatsError
from musictree.measure import Measure
from musictree.staff import Staff
from musictree.time import Time
from musictree.voice import Voice


class TestVoice(TestCase):
    def test_voice_add_beat(self):
        v = Voice()
        quarter_durations = [1 / 64, 3 / 64, 1 / 32, 3 / 32, 1 / 16, 3 / 16, 1 / 8, 3 / 8, 1 / 4, 3 / 4, 1 / 2, 1, 2, 3]
        for quarter_duration in quarter_durations:
            v.add_child(Beat(quarter_duration))
        assert [child.quarter_duration for child in v.get_children()] == quarter_durations

    def test_update_beats(self):
        v = Voice()
        assert not v.get_children()
        v.update_beats()
        assert not v.get_children()
        v.update_beats(1 / 4, 1 / 4, 1 / 4, 1 / 4)
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 4)] * 4
        v.update_beats([1 / 6] * 6)
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 6)] * 6
        v.update_beats([1 / 4] * 3)
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 4)] * 3

    def test_update_beats_from_parent_measure(self):
        v = Voice()
        m = Measure(1)
        st = m.add_child(Staff())
        st.add_child(v)
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 4)] * 4

        m = Measure(1, time=Time(3, 4, 1, 8))
        st = m.add_child(Staff())
        st.add_child(v)
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 4)] * 3 + [(1, 8)]

        m.time = Time(2, 8)
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 8)] * 2

        m.time.signatures = [3, 4, 1, 8]
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 4)] * 3 + [(1, 8)]

        m.time.actual_signatures = [1, 8, 1, 8]
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 8)] * 2

    def test_add_chord(self):
        v = Voice()
        with self.assertRaises(VoiceHasNoBeatsError):
            v.add_chord(Chord())
        v.update_beats(1 / 4, 1 / 4, 1 / 4, 1 / 4)
        v.add_chord(Chord(quarter_duration=2))
        v.add_chord(Chord(quarter_duration=1.5))
        remaining = v.add_chord(Chord(quarter_duration=0.5))
        assert remaining is None

        v = Voice()
        v.update_beats(1, 4, 1, 4)
        remaining = v.add_child(Chord(quarter_duration=3))
        assert isinstance(remaining, Chord)
        assert remaining.quarter_duration == 1
