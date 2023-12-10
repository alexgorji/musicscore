from musicscore.chord import Chord
from musicscore.exceptions import AlreadyFinalizedError
from musicscore.midi import Midi
from musicscore.part import Part
from musicscore.quarterduration import QuarterDuration
from musicscore.score import Score
from musicscore.tests.util import IdTestCase


def assert_chord_note_values(chord, expected_values):
    assert [(note.midi.value, note.quarter_duration) for note in chord.get_children()] == expected_values


class TestFinalUpdates(IdTestCase):
    def setUp(self):
        super().setUp()
        self.score = Score()
        self.part = self.score.add_child(Part('p1'))
        self.measure = self.part.add_measure()
        self.staff = self.measure.add_staff()
        self.voice = self.staff.add_voice()
        self.voice.update_beats()
        self.beats = self.voice.get_children()
        self.chord_1 = self.voice._add_chord(Chord(60, QuarterDuration(1, 3)))[0]
        self.chords_2 = self.voice._add_chord(Chord(61, QuarterDuration(2, 3) + QuarterDuration(3)))

    @staticmethod
    def check_note_values(chords, indices=None):
        if indices is None:
            indices = range(len(chords))

        for i, chord in zip(indices, chords):
            if i == 0:
                assert_chord_note_values(chord, [(60, 1 / 3)])
            elif i == 1:
                assert_chord_note_values(chord, [(61, 2 / 3)])
            elif i == 2:
                assert_chord_note_values(chord, [(61, 3)])

    def test_chord_finalize(self):
        self.measure._update_divisions()
        assert self.chord_1.get_children() == []
        self.chord_1.add_midi(Midi(70))
        self.chord_1.finalize()
        assert len(self.chord_1.get_children()) == 2
        assert_chord_note_values(self.chord_1, [(60, 1 / 3), (70, 1 / 3)])
        with self.assertRaises(AlreadyFinalizedError):
            self.chord_1.finalize()

        self.chords_2[0].finalize()
        assert_chord_note_values(self.chords_2[0], [(61, 2 / 3)])

    def test_beat_finalize(self):
        self.measure._update_divisions()
        self.beats[0].finalize()
        self.check_note_values(self.beats[0].get_chords(), [0, 1])

        self.beats[1].finalize()
        self.check_note_values(self.beats[1].get_chords(), [2])

        with self.assertRaises(AlreadyFinalizedError):
            self.beats[0].finalize()
        with self.assertRaises(AlreadyFinalizedError):
            self.beats[1].finalize()

    def test_voice_finalize(self):
        self.measure._update_divisions()
        self.voice.finalize()
        self.check_note_values(self.voice.get_chords())
        with self.assertRaises(AlreadyFinalizedError):
            self.voice.finalize()

    def test_staff_finalize(self):
        self.measure._update_divisions()
        self.staff.finalize()
        self.check_note_values(self.staff.get_chords())
        with self.assertRaises(AlreadyFinalizedError):
            self.staff.finalize()
        self.staff.to_string()

    def test_measure_finalize(self):
        self.measure.finalize()
        self.check_note_values(self.voice.get_chords())
        with self.assertRaises(AlreadyFinalizedError):
            self.measure.finalize()

    def test_part_finalize(self):
        self.part.finalize()
        self.check_note_values(self.voice.get_chords())
        with self.assertRaises(AlreadyFinalizedError):
            self.part.finalize()

    def test_score_finalize(self):
        self.score.finalize()
        self.check_note_values(self.voice.get_chords())
        with self.assertRaises(AlreadyFinalizedError):
            self.score.finalize()

    def test_to_string_calls_finalize_voice(self):
        self.measure._update_divisions()
        assert self.voice._finalized is False
        self.voice.to_string()
        assert self.voice._finalized is True

    def test_to_string_calls_finalize_staff(self):
        self.measure._update_divisions()
        assert self.staff._finalized is False
        self.staff.to_string()
        assert self.staff._finalized is True

    def test_to_string_calls_finalize_part(self):
        assert self.part._finalized is False
        self.part.to_string()
        assert self.part._finalized is True

    def test_to_string_calls_finalize_score(self):
        assert self.score._finalized is False
        self.score.to_string()
        assert self.score._finalized is True
