from unittest import skip

from musictree import Part, Chord
from musictree.exceptions import AlreadyFinalized
from musictree.tests.util import IdTestCase


class TestAddExceptions(IdTestCase):
    def test_add_chord_to_part(self):
        p = Part(id='part-1')
        p.add_chord(Chord(60, 4))
        p.finalize()
        with self.assertRaises(AlreadyFinalized):
            self.fail()

    @skip
    def test_add_child_to_part(self):
        self.fail()

    @skip
    def test_add_measure_to_part(self):
        self.fail()

    @skip
    def test_add_child_to_chord(self):
        self.fail()

    @skip
    def test_add_direction_type_to_chord(self):
        self.fail()

    @skip
    def test_add_midi_to_chord(self):
        self.fail()

    @skip
    def test_add_dynamics_to_chord(self):
        self.fail()

    @skip
    def test_add_tie_to_chord(self):
        self.fail()

    @skip
    def test_add_lyric_to_chord(self):
        self.fail()

    @skip
    def test_add_wedge_to_chord(self):
        self.fail()

    @skip
    def test_add_x_to_chord(self):
        self.fail()

    @skip
    def test_add_child_to_measure(self):
        self.fail()

    @skip
    def test_add_staff_to_measure(self):
        self.fail()

    @skip
    def test_add_voice_to_measure(self):
        self.fail()

    @skip
    def test_add_child_to_beat(self):
        self.fail()

    @skip
    def test_add_chord_to_beat(self):
        self.fail()

    @skip
    def test_add_child_to_midi(self):
        self.fail()

    @skip
    def test_add_tie_to_midi(self):
        self.fail()

    @skip
    def test_add_child_note(self):
        self.fail()

    @skip
    def test_add_child_to_score(self):
        self.fail()

    @skip
    def test_add_part_to_score(self):
        self.fail()

    @skip
    def test_add_child_to_staff(self):
        self.fail()

    @skip
    def test_add_voice_to_staff(self):
        self.fail()

    @skip
    def test_add_child_to_voice(self):
        self.fail()

    @skip
    def test_add_chord_to_voice(self):
        self.fail()

    @skip
    def test_add_beat_to_voice(self):
        self.fail()
