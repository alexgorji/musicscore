from musictree.chord import Chord
from musictree.exceptions import ChordAlreadyFinalUpdated, ScoreAlreadyFinalUpdated, PartAlreadyFinalUpdated
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
        self.beat = self.voice.get_children()[0]
        self.chord_1 = self.voice.add_chord(Chord(60, QuarterDuration(1, 3)))[0]
        self.chords_2 = self.voice.add_chord(Chord(61, QuarterDuration(2, 3) + QuarterDuration(3)))

    @staticmethod
    def check_note_values(chords):
        for i, chord in enumerate(chords):
            if i == 0:
                assert_chord_note_values(chord, [(60, 1 / 3)])
            elif i == 1:
                assert_chord_note_values(chord, [(61, 2 / 3)])
            elif i == 2:
                assert_chord_note_values(chord, [(61, 3)])

    def test_chord_final_updates(self):
        assert self.chord_1.get_children() == []
        self.chord_1.midis.append(Midi(70))
        self.chord_1.final_updates()
        assert len(self.chord_1.get_children()) == 2
        assert_chord_note_values(self.chord_1, [(60, 1 / 3), (70, 1 / 3)])
        with self.assertRaises(ChordAlreadyFinalUpdated):
            self.chord_1.final_updates()

        self.chords_2[0].final_updates()
        assert_chord_note_values(self.chords_2[0], [(61, 2 / 3)])

    def test_beat_final_updates(self):
        self.fail('Incomplete')

    def test_voice_final_updates(self):
        self.fail('Incomplete')

    def test_staff_final_updates(self):
        self.fail('Incomplete')

    def test_measure_final_updates(self):
        self.fail('Incomplete')

    def test_part_final_updates(self):
        self.part.final_updates()
        self.check_note_values(self.part.get_chords())
        with self.assertRaises(PartAlreadyFinalUpdated):
            self.score.final_updates()

    def test_update_score(self):
        self.score.final_updates()
        self.check_note_values(self.score.get_chords())
        with self.assertRaises(ScoreAlreadyFinalUpdated):
            self.score.final_updates()
