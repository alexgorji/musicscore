import uuid
from unittest import TestCase

from musicscore import Part
from musicscore.beat import Beat, _convert_to_quarter_duration_splittables_dictionary, get_chord_group_subdivision
from musicscore.chord import Chord
from musicscore.config import SPLITTABLES
from musicscore.exceptions import AddChordError, VoiceIsFullError, BeatNotFullError, QuarterDurationIsNotWritable
from musicscore.measure import Measure
from musicscore.quarterduration import QuarterDuration
from musicscore.staff import Staff
from musicscore.tests.util import IdTestCase
from musicscore.tuplet import Tuplet
from musicscore.voice import Voice


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

    def test_beat_fill_with_rest(self):
        b = Beat()
        b._parent = Voice()
        assert not b.is_filled
        b.fill_with_rests()
        assert b.is_filled

    def test_get_chord_groups_subdivision(self):
        assert get_chord_group_subdivision([Chord(60, qd) for qd in [2 / 5, 2 / 5, 1 / 5]]) == 5
        assert get_chord_group_subdivision([Chord(60, qd) for qd in [4 / 5, 4 / 5, 2 / 5]]) == 5
        assert get_chord_group_subdivision([Chord(60, qd) for qd in [1 / 5, 1 / 5, 1 / 10]]) == 5
        assert get_chord_group_subdivision(
            [Chord(60, qd) for qd in [1 / 6, 1 / 6, 1 / 6, 1 / 10, 3 / 10, 1 / 10]]) is None


class TestBeatUpdateChords(IdTestCase):
    def test_beat_update_chord_types(self):
        p = Part('p1')
        [p.add_chord(ch) for ch in [Chord(60, 0.5), Chord(70, 0.5)]]
        beat = p.get_beat(measure_number=1, staff_number=1, voice_number=1, beat_number=1)
        assert {ch.type for ch in beat.get_chords()} == {None}
        beat._update_chord_types()
        assert {ch.type for ch in beat.get_chords()} == {'eighth'}
        [p.add_chord(ch) for ch in [Chord(60, 0.5), Chord(70, 0.5)]]
        beat = p.get_beat(measure_number=1, staff_number=1, voice_number=1, beat_number=2)
        beat.get_chords()[0].type = 'quarter'
        beat._update_chord_types()
        assert [ch.type for ch in beat.get_chords()] == ['quarter', 'eighth']

    def test_beat_update_chord_number_of_dots(self):
        p = Part('p1')
        [p.add_chord(Chord([60, 61], qd)) for qd in [1, 0.75, 0.25, 0.875, 0.125]]
        assert {ch.number_of_dots for ch in p.get_chords()} == {None}
        for b in p.get_beats():
            try:
                b._update_chord_number_of_dots()
            except BeatNotFullError:
                pass
        assert [ch.number_of_dots for ch in p.get_chords()] == [0, 1, 0, 2, 0]
        p = Part('p2')
        ch = Chord(60, 1)
        ch.number_of_dots = 3
        p.add_chord(ch)
        beat = p.get_beats()[0]
        beat._update_chord_number_of_dots()
        assert beat.get_chords()[0].number_of_dots == 3

    # def test_beat_update_chord_tuplets(self):
    #     self.fail()


class TestBeatUpdateChordBeams(TestCase):
    pass


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
        with self.assertRaises(VoiceIsFullError):
            v.get_current_beat()
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
                assert [ch.quarter_duration for ch in beat.get_children()] == [QuarterDuration(2, 5),
                                                                               QuarterDuration(3, 5)]
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


class TestBeatSplitChord(TestCase):
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
        v1.up.up._update_divisions()
        v2.up.up._update_divisions()
        for b in v1.get_children() + v2.get_children():
            b.finalize()

        assert [ch.midis[0].accidental.xml_object.value_ if ch.midis[0].accidental.xml_object else None for ch in
                all_chords] == ['sharp',
                                None,
                                None,
                                None]
        all_chords[1].midis[0].accidental.show = True

        assert [ch.midis[0].accidental.xml_object.value_ if ch.midis[0].accidental.xml_object else None for ch in
                all_chords] == ['sharp',
                                'sharp',
                                None,
                                None]

    def test_split_not_writable_chords(self):
        v = create_voice()
        v.update_beats(1)
        v._add_chord(Chord(60, 5 / 6))
        v._add_chord(Chord(60, 1 / 6))
        assert [ch.quarter_duration for ch in v.get_chords()] == [5 / 6, 1 / 6]
        v.get_beat(1)._split_not_writable_chords()
        assert [ch.quarter_duration for ch in v.get_chords()] == [1 / 2, 1 / 3, 1 / 6]

    def test_add_child_5_leftover(self):
        v = create_voice()
        beats = v.update_beats(1, 1, 1, 1)
        split_children = v.get_current_beat().add_child(Chord(midis=61, quarter_duration=6))
        for index, beat in enumerate(beats):
            if index == 0:
                assert [ch.quarter_duration for ch in beat.get_children()] == [4]
                assert [ch.midis[0].value for ch in beat.get_children()] == [61]
                assert beat.is_filled
            else:
                assert beat.get_children() == []
                assert beat.is_filled
        assert split_children[0].midis[0].is_tied_to_next
        assert v.leftover_chord.quarter_duration == 2
        assert not v.leftover_chord.split
        assert v.leftover_chord.midis[0].value == 61
        assert v.leftover_chord.midis[0].is_tied_to_previous

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

    def test_split_tied_chords(self):
        v = create_voice()
        v.update_beats(1, 1, 1, 1)
        ch1 = Chord(60, quarter_duration=1.5)
        ch1.add_tie('start')
        split_chords_1 = v.get_current_beat().add_child(ch1)
        assert split_chords_1[-1].midis[0].is_tied_to_next

        ch2 = Chord([60, 63], quarter_duration=2)
        ch2.midis[1].add_tie('start')
        split_chords_2 = v.get_current_beat().add_child(ch2)
        assert not split_chords_2[-1].midis[0].is_tied_to_next
        assert split_chords_2[-1].midis[1].is_tied_to_next

    def test_add_chord_exception(self):
        b = Beat()
        with self.assertRaises(AddChordError):
            b.add_chord()

    def test_convert_splittables_dictionary(self):
        SPLITTABLES = {
            (0, 1): {
                (5, 6): [(3, 6), (2, 6)],
            },
            (1, 6): {
                (4, 6): [(2, 6), (2, 6)],
                (5, 6): [(2, 6), (3, 6)],
            },
            (2, 6): {
                (3, 6): [(2, 6), (1, 6)],
                (5, 6): [(2, 6), (3, 6)],
            }
        }

        expected = {
            QuarterDuration(0, 1): {
                QuarterDuration(5, 6): [QuarterDuration(3, 6), QuarterDuration(2, 6)],
            },
            QuarterDuration(1, 6): {
                QuarterDuration(4, 6): [QuarterDuration(2, 6), QuarterDuration(2, 6)],
                QuarterDuration(5, 6): [QuarterDuration(2, 6), QuarterDuration(3, 6)],
            },
            QuarterDuration(2, 6): {
                QuarterDuration(3, 6): [QuarterDuration(2, 6), QuarterDuration(1, 6)],
                QuarterDuration(5, 6): [QuarterDuration(2, 6), QuarterDuration(3, 6)],
            }
        }
        assert expected == _convert_to_quarter_duration_splittables_dictionary(SPLITTABLES)

    def test_all_splits(self):
        for key, value in SPLITTABLES.items():
            for k, v in value.items():
                p = Part(f'p{uuid.uuid4()}')
                qds = [QuarterDuration(*key), QuarterDuration(*k)]
                remaining_qd = QuarterDuration(1 - sum(qds))
                if remaining_qd < 0:
                    remaining_qd += 1
                if remaining_qd > 0:
                    qds.append(remaining_qd)
                for qd in qds:
                    if qd:
                        p.add_chord(Chord(70, qd))
                p.finalize()
                assert sum([ch.quarter_duration for ch in p.get_beats()[0].get_chords() if not ch.is_rest]) == 1


class TestNotImplementedTuplets(IdTestCase):
    def test_writing_subdivision_17(self):
        factors = [1, 2, 3, 4, 4, 3]
        qds = [QuarterDuration(x, 17) for x in factors]
        chords = [Chord(60, qd) for qd in qds]
        [ch.add_lyric(x) for ch, x in zip(chords, factors)]
        p = Part('p1')
        [p.add_chord(ch) for ch in chords]
        with self.assertRaises(QuarterDurationIsNotWritable):
            p.finalize()
        for ch in chords:
            if ch.quarter_duration == QuarterDuration(1, 17):
                ch.type = '64th'
                ch.number_of_dots = 0
            elif ch.quarter_duration == QuarterDuration(2, 17):
                ch.type = '32nd'
                ch.number_of_dots = 0
            elif ch.quarter_duration == QuarterDuration(3, 17):
                ch.type = '32nd'
                ch.number_of_dots = 1
            elif ch.quarter_duration == QuarterDuration(4, 17):
                ch.type = '16th'
                ch.number_of_dots = 0

            ch.tuplet = Tuplet(17, 16, '64th')

        p = Part('p2')
        [p.add_chord(ch) for ch in chords]
        p.finalize()
        beat = p.get_beats()[0]
        for ch in beat.get_chords():
            ch.check_printed_duration()
            ch.check_number_of_beams()
