from musictree.chord import Chord
from musictree.exceptions import AlreadyFinalUpdated
from musictree.midi import Midi
from musictree.part import Part
from musictree.quarterduration import QuarterDuration
from musictree.score import Score
from musictree.tests.util import IdTestCase


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
        self.chord_1 = self.voice.add_chord(Chord(60, QuarterDuration(1, 3)))[0]
        self.chords_2 = self.voice.add_chord(Chord(61, QuarterDuration(2, 3) + QuarterDuration(3)))

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

    def test_chord_final_updates(self):
        self.measure.update_divisions()
        assert self.chord_1.get_children() == []
        self.chord_1.midis.append(Midi(70))
        self.chord_1.final_updates()
        assert len(self.chord_1.get_children()) == 2
        assert_chord_note_values(self.chord_1, [(60, 1 / 3), (70, 1 / 3)])
        with self.assertRaises(AlreadyFinalUpdated):
            self.chord_1.final_updates()

        self.chords_2[0].final_updates()
        assert_chord_note_values(self.chords_2[0], [(61, 2 / 3)])

    def test_beat_final_updates(self):
        self.measure.update_divisions()
        self.beats[0].final_updates()
        self.check_note_values(self.beats[0].get_chords(), [0, 1])

        self.beats[1].final_updates()
        self.check_note_values(self.beats[1].get_chords(), [2])

        with self.assertRaises(AlreadyFinalUpdated):
            self.beats[0].final_updates()
        with self.assertRaises(AlreadyFinalUpdated):
            self.beats[1].final_updates()

    def test_voice_final_updates(self):
        self.measure.update_divisions()
        self.voice.final_updates()
        self.check_note_values(self.voice.get_chords())
        with self.assertRaises(AlreadyFinalUpdated):
            self.voice.final_updates()

    def test_staff_final_updates(self):
        self.measure.update_divisions()
        self.staff.final_updates()
        self.check_note_values(self.staff.get_chords())
        with self.assertRaises(AlreadyFinalUpdated):
            self.staff.final_updates()
        self.staff.to_string()

    def test_measure_final_updates(self):
        self.measure.final_updates()
        self.check_note_values(self.measure.get_chords())
        with self.assertRaises(AlreadyFinalUpdated):
            self.measure.final_updates()

    def test_part_final_updates(self):
        self.part.final_updates()
        self.check_note_values(self.part.get_chords())
        with self.assertRaises(AlreadyFinalUpdated):
            self.part.final_updates()

    def test_score_final_updates(self):
        self.score.final_updates()
        self.check_note_values(self.score.get_chords())
        with self.assertRaises(AlreadyFinalUpdated):
            self.score.final_updates()

    def test_to_string_calls_final_updates_voice(self):
        self.measure.update_divisions()
        assert self.voice._final_updated is False
        self.voice.to_string()
        assert self.voice._final_updated is True

    def test_to_string_calls_final_updates_staff(self):
        self.measure.update_divisions()
        assert self.staff._final_updated is False
        self.staff.to_string()
        assert self.staff._final_updated is True

    def test_to_string_calls_final_updates_part(self):
        assert self.part._final_updated is False
        self.part.to_string()
        assert self.part._final_updated is True

    def test_to_string_calls_final_updates_score(self):
        assert self.score._final_updated is False
        self.score.to_string()
        assert self.score._final_updated is True
