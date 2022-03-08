from musictree.chord import Chord
from musictree.exceptions import ChordAlreadyFinalUpdated
from musictree.midi import Midi
from musictree.part import Part
from musictree.quarterduration import QuarterDuration
from musictree.score import Score
from musictree.tests.util import IdTestCase


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

    def test_chord_final_updates(self):
        assert self.chord_1.get_children() == []
        self.chord_1.midis.append(Midi(70))
        self.chord_1.final_updates()
        assert len(self.chord_1.get_children()) == 2
        assert [(note.midi.value, note.quarter_duration) for note in self.chord_1.get_children()] == [(60, 1 / 3), (70, 1 / 3)]
        with self.assertRaises(ChordAlreadyFinalUpdated):
            self.chord_1.final_updates()

        self.chords_2[0].final_updates()
        assert [(note.midi.value, note.quarter_duration) for note in self.chords_2[0].get_children()] == [(61, 2 / 3)]

    def test_beat_final_updates(self):
        self.fail('Incomplete')

    def test_update_voice(self):
        self.fail('Incomplete')

    def test_update_staff(self):
        self.fail('Incomplete')

    def test_update_measure(self):
        self.fail('Incomplete')

    def test_update_part(self):
        self.fail('Incomplete')

    def test_update_score(self):
        self.fail('Incomplete')
