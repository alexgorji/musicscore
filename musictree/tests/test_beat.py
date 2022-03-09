from unittest import TestCase

from musictree.beat import Beat
from musictree.chord import Chord
from musictree.measure import Measure
from musictree.quarterduration import QuarterDuration
from musictree.staff import Staff
from musictree.voice import Voice


def create_voice():
    voice = Voice()
    st = Staff()
    m = Measure(1)
    m.add_child(st)
    st.add_child(voice)
    return voice


class TestBeat(TestCase):

    def test_beat_quarter_duration(self):
        b = Beat()
        assert b.quarter_duration == 1
        b.quarter_duration = 4
        assert b.quarter_duration == 4

    def test_beat_previous(self):
        b = Beat()
        assert b.previous is None
        v = create_voice()
        v.update_beats(1 / 4, 1 / 8, 1 / 2, 1)
        assert v.get_children()[0].previous is None
        assert v.get_children()[1].previous.quarter_duration == 1 / 4
        assert v.get_children()[2].previous.quarter_duration == 1 / 8
        assert v.get_children()[3].previous.quarter_duration == 1 / 2

    def test_beat_next(self):
        b = Beat()
        assert b.next is None
        v = create_voice()

        v.update_beats(1 / 4, 1 / 8, 1 / 2, 1)
        assert v.get_children()[0].next.quarter_duration == 1 / 8
        assert v.get_children()[1].next.quarter_duration == 1 / 2
        assert v.get_children()[2].next.quarter_duration == 1
        assert v.get_children()[3].next is None

    def test_beat_offset(self):
        b = Beat()
        assert b.offset is None
        v = create_voice()
        v.update_beats(1 / 4, 1 / 8, 1 / 2, 1)
        assert v.get_children()[0].offset == 0
        assert v.get_children()[1].offset == 1 / 4
        assert v.get_children()[2].offset == 1 / 4 + 1 / 8
        assert v.get_children()[3].offset == 1 / 4 + 1 / 8 + 1 / 2


class TestBeatAddChild(TestCase):
    def test_beat_add_child(self):
        v = create_voice()
        beats = v.update_beats(1 / 4, 1 / 4, 1 / 4, 1 / 4)
        assert v.get_current_beat() == beats[0]
        chord1 = v.get_current_beat().add_child(Chord(60, quarter_duration=1 / 8))[0]
        assert chord1.up == beats[0]
        assert v.get_current_beat() == beats[0]
        chord2 = v.get_current_beat().add_child(Chord(60, quarter_duration=1 / 8))[0]
        assert chord2.up == beats[0]
        assert v.get_current_beat() == beats[1]
        chord3 = v.get_current_beat().add_child(Chord(60, quarter_duration=1 / 4))[0]
        assert chord3.up == beats[1]
        assert v.get_current_beat() == beats[2]
        chord4 = v.get_current_beat().add_child(Chord(60, quarter_duration=1 / 2))[0]
        assert chord4.up == beats[2]
        assert v.get_current_beat() is None
        assert beats[3].is_filled
        assert v.leftover_chord is None

        v = create_voice()
        beats = v.update_beats(1 / 4, 1 / 4, 1 / 4, 1 / 4)
        assert v.get_current_beat() == beats[0]
        v.get_current_beat().add_child(Chord(midis=60, quarter_duration=1 / 8))
        v.get_current_beat().add_child(Chord(midis=61, quarter_duration=1 / 4))
        assert v.get_current_beat() == beats[1]
        assert [ch.quarter_duration for ch in beats[0].get_children()] == [1 / 8, 1 / 8]
        assert [ch.midis[0].value for ch in beats[0].get_children()] == [60, 61]
        assert [ch.quarter_duration for ch in beats[1].get_children()] == [1 / 8]
        assert [ch.midis[0].value for ch in beats[1].get_children()] == [61]

    def test_beat_add_child_4_no_split(self):
        v = create_voice()
        beats = v.update_beats(1, 1, 1, 1)
        chord = v.get_current_beat().add_child(Chord(60, quarter_duration=4))
        assert v.leftover_chord is None
        for index, beat in enumerate(beats):
            if index == 0:
                assert beat.get_children() == chord
                assert beat.get_children()[0].quarter_duration == 4
                assert beat.is_filled
            else:
                assert beat.is_filled

    def test_beat_add_child_1_3_no_split(self):
        v = create_voice()
        beats = v.update_beats(1, 1, 1, 1)
        v.get_current_beat().add_child(Chord(midis=60, quarter_duration=1))
        v.get_current_beat().add_child(Chord(midis=61, quarter_duration=3))
        assert v.leftover_chord is None
        for index, beat in enumerate(beats):
            if index == 0:
                assert [ch.quarter_duration for ch in beat.get_children()] == [1]
                assert [ch.midis[0].value for ch in beat.get_children()] == [60]
                assert beat.is_filled
            elif index == 1:
                assert [ch.quarter_duration for ch in beat.get_children()] == [3]
                assert [ch.midis[0].value for ch in beat.get_children()] == [61]
                assert beat.is_filled
            else:
                assert beat.get_children() == []
                assert beat.is_filled

    def test_add_child_5_leftover(self):
        v = create_voice()
        beats = v.update_beats(1, 1, 1, 1)
        split_children = v.get_current_beat().add_child(Chord(midis=61, quarter_duration=5))
        for index, beat in enumerate(beats):
            if index == 0:
                assert [ch.quarter_duration for ch in beat.get_children()] == [4]
                assert [ch.midis[0].value for ch in beat.get_children()] == [61]
                assert beat.is_filled
            else:
                assert beat.get_children() == []
                assert beat.is_filled
        assert split_children[0]._ties == ['start']
        assert v.leftover_chord.quarter_duration == 1
        assert not v.leftover_chord.split
        assert v.leftover_chord.midis[0].value == 61
        assert v.leftover_chord._ties == ['stop']

    def test_add_child_with_fractional_quarter_duration_1(self):
        v = create_voice()
        beats = v.update_beats(1, 1, 1, 1)
        v.get_current_beat().add_child(Chord(midis=61, quarter_duration=0.5))
        v.get_current_beat().add_child(Chord(midis=62, quarter_duration=3.5))
        for index, beat in enumerate(beats):
            if index == 0:
                assert [ch.quarter_duration for ch in beat.get_children()] == [0.5, 0.5]
                assert [ch.midis[0].value for ch in beat.get_children()] == [61, 62]
                assert beat.is_filled
            elif index == 1:
                assert [ch.quarter_duration for ch in beat.get_children()] == [3]
                assert [ch.midis[0].value for ch in beat.get_children()] == [62]
                assert beat.is_filled
            else:
                assert beat.get_children() == []
                assert beat.is_filled

    def test_add_child_with_fractional_quarter_duration_2(self):
        v = create_voice()
        beats = v.update_beats(1, 1.5, 1)
        v.get_current_beat().add_child(Chord(midis=61, quarter_duration=QuarterDuration(2, 5)))
        v.get_current_beat().add_child(Chord(midis=62, quarter_duration=4))
        for index, beat in enumerate(beats):
            if index == 0:
                assert [ch.quarter_duration for ch in beat.get_children()] == [QuarterDuration(2, 5), QuarterDuration(3, 5)]
                assert [ch.midis[0].value for ch in beat.get_children()] == [61, 62]
                assert beat.is_filled
            elif index == 1:
                assert [ch.quarter_duration for ch in beat.get_children()] == [1.5]
                assert [ch.midis[0].value for ch in beat.get_children()] == [62]
                assert beat.is_filled
            elif index == 2:
                assert [ch.quarter_duration for ch in beat.get_children()] == [1]
                assert [ch.midis[0].value for ch in beat.get_children()] == [62]
                assert beat.is_filled
        assert v.leftover_chord.quarter_duration == 4 - 2.5 - 0.6

    def test_split_chord_different_accidental_instances(self):
        v1 = create_voice()
        v1.update_beats(1, 1.5)
        chord = Chord(midis=61, quarter_duration=2.5)
        v1.get_current_beat().add_child(chord)
        ch1, ch2 = v1.get_chords()

        assert ch1.midis[0].accidental != ch2.midis[0].accidental

    def test_split_chord_accidentals(self):
        v1 = create_voice()
        v1.update_beats(1, 1.5, 1)
        chord = Chord(midis=61, quarter_duration=7)
        chord.midis[0].accidental.show = True
        assert chord.midis[0].accidental.xml_object.value_ == 'sharp'
        v1.get_current_beat().add_child(chord)
        v2 = create_voice()
        v2.update_beats(1, 1, 1)
        v2.get_current_beat().add_child(v1.leftover_chord)
        all_chords = v1.get_chords() + v2.get_chords()
        v1.up.up.update_divisions()
        v2.up.up.update_divisions()
        for b in v1.get_children() + v2.get_children():
            b.final_updates()

        assert [ch.midis[0].accidental.xml_object.value_ if ch.midis[0].accidental.xml_object else None for ch in all_chords] == ['sharp',
                                                                                                                                  None,
                                                                                                                                  None,
                                                                                                                                  None]
        all_chords[1].midis[0].accidental.show = True

        assert [ch.midis[0].accidental.xml_object.value_ if ch.midis[0].accidental.xml_object else None for ch in all_chords] == ['sharp',
                                                                                                                                  'sharp',
                                                                                                                                  None,
                                                                                                                                  None]

    def test_split_not_writable_chords(self):
        v = create_voice()
        v.update_beats(1)
        v.add_chord(Chord(60, 5 / 6))
        v.add_chord(Chord(60, 1 / 6))
        assert [ch.quarter_duration for ch in v.get_chords()] == [5 / 6, 1 / 6]
        v.get_beat(1).split_not_writable_chords()
        assert [ch.quarter_duration for ch in v.get_chords()] == [1 / 2, 1 / 3, 1 / 6]
