from unittest import TestCase, skip
from unittest.mock import Mock

from musicscore import Chord, Beat, Part
from musicscore.exceptions import ChordTypeNotSetError, ChordTestError
from musicscore.tests.util import IdTestCase


class TestTestChordNumberOfBeams(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.chord = Chord(60, 1 / 8)

    def test_chord_has_no_type(self):
        with self.assertRaises(ChordTypeNotSetError):
            self.chord.check_number_of_beams()

    def test_chord_without_beam(self):
        self.chord.type = 'quarter'
        assert self.chord.check_number_of_beams()
        self.chord.type = '32nd'
        assert self.chord.check_number_of_beams()
        self.chord.beams = {}
        assert self.chord.check_number_of_beams()
        self.chord.beams = {1: 'begin'}
        with self.assertRaises(ChordTestError):
            self.chord.check_number_of_beams()
        self.chord.beams = {1: 'begin', 3: 'forward'}
        with self.assertRaises(ChordTestError):
            self.chord.check_number_of_beams()
        self.chord.beams = {1: 'begin', 2: 'begin', 3: 'forward'}
        assert self.chord.check_number_of_beams()
        self.chord.beams = {1: 'begin', 2: 'begin', 3: 'begin', 4: 'forward'}
        with self.assertRaises(ChordTestError):
            self.chord.check_number_of_beams()


class TestBeams16th(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.beat = Beat()
        self.measure = Mock()
        self.beat._parent = self.measure
        [self.beat._add_chord(Chord(60, qd)) for qd in 4 * [1 / 4]]
        self.chords = self.beat.get_chords()

    def test_all_non_rest(self):
        assert [ch.beams for ch in self.chords] == [{}, {}, {}, {}]
        self.beat._update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'begin'}, {1: 'continue', 2: 'continue'},
                                                    {1: 'continue', 2: 'continue'}, {1: 'end', 2: 'end'}]

    def test_all_two_rests_middle(self):
        for ch in self.chords[1:3]:
            ch.midis = 0
        assert [ch.is_rest for ch in self.chords] == [False, True, True, False]
        self.beat._update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'forward'}, {},
                                                    {}, {1: 'end', 2: 'backward'}]

    def test_one_rest_second(self):
        self.chords[1].midis = 0
        assert [ch.is_rest for ch in self.chords] == [False, True, False, False]
        self.beat._update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'forward'}, {},
                                                    {1: 'continue', 2: 'begin'}, {1: 'end', 2: 'end'}]

    def test_one_rest_third(self):
        self.chords[2].midis = 0
        assert [ch.is_rest for ch in self.chords] == [False, False, True, False]
        self.beat._update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'begin'},
                                                    {1: 'continue', 2: 'end'}, {}, {1: 'end', 2: 'backward'}]

    def test_one_rest_start(self):
        self.chords[0].midis = 0
        assert [ch.is_rest for ch in self.chords] == [True, False, False, False]
        self.beat._update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{}, {1: 'begin', 2: 'begin'},
                                                    {1: 'continue', 2: 'continue'}, {1: 'end', 2: 'end'}]

    def test_two_rests_start_end(self):
        self.chords[0].midis = 0
        self.chords[-1].midis = 0
        assert [ch.is_rest for ch in self.chords] == [True, False, False, True]
        self.beat._update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{}, {1: 'begin', 2: 'begin'},
                                                    {1: 'end', 2: 'end'}, {}]

    def test_all_rests(self):
        for ch in self.chords:
            ch.midis = 0
        self.beat._update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{}, {}, {}, {}]

    def test_break_all_beams(self):
        for ch in self.chords:
            ch.break_beam()
        self.beat._update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{}, {}, {}, {}]


    def test_break_last_beam(self):
        self.chords[-1].break_beam()
        self.beat._update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'begin'}, {1: 'continue', 2: 'continue'},
                                                    {1: 'end', 2: 'end'}, {}]

    def test_break_third_beam(self):
        self.chords[2].break_beam()
        self.beat._update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'begin'}, {1: 'end', 2: 'end'},
                                                    {1: 'begin', 2: 'begin'}, {1: 'end', 2: 'end'}]

    def test_break_third_and_fourth_beam(self):
        self.chords[2].break_beam()
        self.chords[3].break_beam()
        self.beat._update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'begin'}, {1: 'end', 2: 'end'},
                                                    {}, {}]

    def test_manually_set_beams_to_None(self):
        for ch in self.chords:
            ch.beams = None
        self.beat._update_chord_beams()
        # assert [ch.beams for ch in self.chords] == [{}, {}, {}, {}]
        ch = self.chords[0]
        ch.get_parent_measure().get_divisions.return_value = 4
        ch.up.up.up.number = 1
        self.chords[0].finalize()


class TestBeams32th(IdTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.beat = Beat()
        self.beat._parent = Mock()
        [self.beat._add_chord(Chord(60, qd)) for qd in 8 * [1 / 8]]
        self.chords = self.beat.get_chords()

    def test_second_and_third(self):
        self.chords[1].midis = 0
        self.chords[2].midis = 0
        self.beat._update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'forward', 3: 'forward'}, {}, {},
                                                    {1: 'continue', 2: 'backward', 3: 'backward'},
                                                    {1: 'continue', 2: 'begin', 3: 'begin'},
                                                    {1: 'continue', 2: 'continue', 3: 'continue'},
                                                    {1: 'continue', 2: 'continue', 3: 'continue'},
                                                    {1: 'end', 2: 'end', 3: 'end'}]

    def test_32nd_two_chords(self):
        p = Part('p1')
        p.add_measure([1, 8])
        qds = [1 / 8, 3 / 8]
        [p.add_chord(Chord(71, qd)) for qd in qds]
        p.finalize()
        chords = p.get_chords()
        assert [ch.beams for ch in chords] == [{1: 'begin', 2: 'begin', 3: 'forward'}, {1: 'end', 2: 'end'}]

    def test_32nd_problem_1(self):
        p = Part('p2')
        p.add_measure([1, 4])
        qds = [1 / 8, 3 / 8, 1 / 2]
        [p.add_chord(Chord(71, qd)) for qd in qds]
        p.finalize()
        chords = p.get_chords()
        for ch in chords:
            ch.check_number_of_beams()
        assert [ch.beams for ch in chords] == [{1: 'begin', 2: 'begin', 3: 'forward'}, {1: 'continue', 2: 'end'},
                                               {1: 'end'}]

    def test_32nd_problem_2(self):
        p = Part('p1')
        p.add_measure([1, 8])
        qds = [3 / 8, 1 / 8]
        [p.add_chord(Chord(71, qd)) for qd in qds]
        p.finalize()
        chords = p.get_chords()
        assert [ch.beams for ch in chords] == [{1: 'begin', 2: 'begin'}, {1: 'end', 2: 'end', 3: 'backward'}]

    def test_32nd_problem_3(self):
        p = Part('p2')
        p.add_measure([1, 4])
        qds = [3 / 8, 1 / 8, 1 / 2]
        [p.add_chord(Chord(71, qd)) for qd in qds]
        p.finalize()
        chords = p.get_chords()
        for ch in chords:
            ch.check_number_of_beams()
        assert [ch.beams for ch in chords] == [{1: 'begin', 2: 'begin'}, {1: 'continue', 2: 'end', 3: 'backward'},
                                               {1: 'end'}]

    def test_32nd_problem_4(self):
        p = Part('p2')
        p.add_measure([1, 4])
        qds = [1 / 2, 1 / 8, 3 / 8]
        [p.add_chord(Chord(71, qd)) for qd in qds]
        p.finalize()
        chords = p.get_chords()
        for ch in chords:
            ch.check_number_of_beams()
        assert [ch.beams for ch in chords] == [{1: 'begin'}, {1: 'continue', 2: 'begin', 3: 'forward'},
                                               {1: 'end', 2: 'end'}]
