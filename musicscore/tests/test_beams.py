from unittest import TestCase, skip
from unittest.mock import Mock

from musicscore import Chord, Beat


class TestBeams16th(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.beat = Beat()
        self.beat._parent = Mock()
        [self.beat._add_chord(Chord(60, qd)) for qd in 4 * [1 / 4]]
        self.chords = self.beat.get_chords()

    def test_all_non_rest(self):
        assert [ch.beams for ch in self.chords] == [{}, {}, {}, {}]
        self.beat.update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'begin'}, {1: 'continue', 2: 'continue'},
                                                    {1: 'continue', 2: 'continue'}, {1: 'end', 2: 'end'}]

    def test_all_two_rests_middle(self):
        for ch in self.chords[1:3]:
            ch.midis = 0
        assert [ch.is_rest for ch in self.chords] == [False, True, True, False]
        self.beat.update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'forward'}, {},
                                                    {}, {1: 'end', 2: 'backward'}]

    def test_one_rest_second(self):
        self.chords[1].midis = 0
        assert [ch.is_rest for ch in self.chords] == [False, True, False, False]
        self.beat.update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'forward'}, {},
                                                    {1: 'continue', 2: 'begin'}, {1: 'end', 2: 'end'}]

    def test_one_rest_third(self):
        self.chords[2].midis = 0
        assert [ch.is_rest for ch in self.chords] == [False, False, True, False]
        self.beat.update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'begin'},
                                                    {1: 'continue', 2: 'end'}, {}, {1: 'end', 2: 'backward'}]

    def test_one_rest_start(self):
        self.chords[0].midis = 0
        assert [ch.is_rest for ch in self.chords] == [True, False, False, False]
        self.beat.update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{}, {1: 'begin', 2: 'begin'},
                                                    {1: 'continue', 2: 'continue'}, {1: 'end', 2: 'end'}]

    def test_two_rests_start_end(self):
        self.chords[0].midis = 0
        self.chords[-1].midis = 0
        assert [ch.is_rest for ch in self.chords] == [True, False, False, True]
        self.beat.update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{}, {1: 'begin', 2: 'begin'},
                                                    {1: 'end', 2: 'end'}, {}]

    def test_all_rests(self):
        for ch in self.chords:
            ch.midis = 0
        self.beat.update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{}, {}, {}, {}]

    @skip
    def test_break_all_beams(self):
        for ch in self.chords:
            ch.break_beam()
        self.beat.update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{}, {}, {}, {}]

    @skip
    def test_break_last_beam(self):
        self.chords[-1].break_beam()
        self.beat.update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'begin'}, {1: 'continue', 2: 'continue'},
                                                    {1: 'end', 2: 'end'}, {}]

    @skip
    def test_break_third_beam(self):
        self.chords[2].break_beam()
        self.beat.update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'begin'}, {1: 'end', 2: 'end'},
                                                    {1: 'begin', 2: 'begin'}, {1: 'end', 2: 'end'}]

    @skip
    def test_break_third_and_fourth_beam(self):
        self.chords[2].break_beam()
        self.chords[3].break_beam()
        self.beat.update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'begin'}, {1: 'end', 2: 'end'},
                                                    {}, {}]


class TestBeams32th(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.beat = Beat()
        self.beat._parent = Mock()
        [self.beat._add_chord(Chord(60, qd)) for qd in 8 * [1 / 8]]
        self.chords = self.beat.get_chords()

    def test_second_and_third(self):
        self.chords[1].midis = 0
        self.chords[2].midis = 0
        self.beat.update_chord_beams()
        assert [ch.beams for ch in self.chords] == [{1: 'begin', 2: 'forward', 3: 'forward'}, {}, {},
                                                    {1: 'continue', 2: 'backward', 3: 'backward'},
                                                    {1: 'continue', 2: 'begin', 3: 'begin'},
                                                    {1: 'continue', 2: 'continue', 3: 'continue'},
                                                    {1: 'continue', 2: 'continue', 3: 'continue'},
                                                    {1: 'end', 2: 'end', 3: 'end'}]
