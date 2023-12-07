from unittest import TestCase
from unittest.mock import Mock, patch

from musicscore.beat import Beat
from musicscore.chord import Chord
from musicscore.exceptions import VoiceHasNoBeatsError, AddChordError, VoiceIsFullError
from musicscore.voice import Voice


class TestVoice(TestCase):
    @patch('musicscore.voice.Voice.up', new=Mock())
    def test_voice_add_beat(self):
        v = Voice()
        quarter_durations = [1 / 64, 3 / 64, 1 / 32, 3 / 32, 1 / 16, 3 / 16, 1 / 8, 3 / 8, 1 / 4, 3 / 4, 1 / 2, 1, 2, 3]
        for quarter_duration in quarter_durations:
            v.add_child(Beat(quarter_duration))
        assert [child.quarter_duration for child in v.get_children()] == quarter_durations

    @patch('musicscore.voice.Voice.up')
    def test_update_beats(self, mock_beat):
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

    @patch('musicscore.voice.Voice.up', new=Mock())
    def test_update_beats_with_old_beats(self):
        v = Voice()
        v.update_beats(1 / 4, 1 / 4, 1 / 4, 1 / 4)
        v.update_beats(1 / 4, 1 / 2)

        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 4), (1, 2)]

    @patch('musicscore.voice.Voice.up', new=Mock())
    def test_get_current_beat(self):
        v = Voice()
        beats = v.update_beats(1 / 4, 1 / 4, 1 / 4, 1 / 4)
        assert v.get_current_beat() == beats[0]
        v.get_children()[0]._filled_quarter_duration = 1 / 8
        assert v.get_current_beat() == beats[0]
        v.get_children()[0]._filled_quarter_duration = 1 / 4
        assert v.get_current_beat() == beats[1]
        v.get_children()[1]._filled_quarter_duration = 1 / 8
        assert v.get_current_beat() == beats[1]
        v.get_children()[1]._filled_quarter_duration = 1 / 4
        assert v.get_current_beat() == beats[2]
        v.get_children()[2]._filled_quarter_duration = 1 / 4
        assert v.get_current_beat() == beats[3]
        v.get_children()[3]._filled_quarter_duration = 1 / 8
        assert v.get_current_beat() == beats[3]
        v.get_children()[3]._filled_quarter_duration = 1 / 4
        with self.assertRaises(VoiceIsFullError):
            assert v.get_current_beat() is None

    @patch('musicscore.staff.Staff')
    def test_add_chord(self, mock_staff):
        v = Voice()
        v._parent = mock_staff

        with self.assertRaises(VoiceHasNoBeatsError):
            v._add_chord(Chord(60, 1))
        v.update_beats(1, 1, 1, 1)
        v._add_chord(Chord(quarter_duration=1.5, midis=60))
        v._add_chord(Chord(quarter_duration=2, midis=60))
        v._add_chord(Chord(quarter_duration=0.5, midis=60))
        assert v.leftover_chord is None
        assert [ch.quarter_duration for ch in v.get_chords()] == [1.5, 0.5, 1.5, 0.5]
        assert v.get_chords()[1].midis[0].is_tied_to_next
        assert v.get_chords()[2].midis[0].is_tied_to_previous

        v = Voice()
        v._parent = mock_staff
        v.update_beats(1, 1)
        v._add_chord(Chord(quarter_duration=3, midis=60))
        assert isinstance(v.leftover_chord, Chord)
        assert v.leftover_chord.quarter_duration == 1

    def test_add_chord_exception(self):
        v = Voice()
        with self.assertRaises(AddChordError):
            v.add_chord()
