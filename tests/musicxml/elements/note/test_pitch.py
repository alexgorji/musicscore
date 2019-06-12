from unittest import TestCase
from musicscore.musicxml.elements.fullnote import Step, Alter, Octave, Pitch


class TestPitch(TestCase):
    def setUp(self):
        self.pitch = Pitch()

    def test_to_string(self):
        result = '<pitch>\n  <step>C</step>\n  <octave>4</octave>\n</pitch>\n'
        self.assertEqual(self.pitch.to_string(), result)

    def test_arguments(self):
        pitch = Pitch(Step('D'), octave=Octave(7), alter=Alter(1.5))
        result = '<pitch>\n  <step>D</step>\n  <alter>1.5</alter>\n  <octave>7</octave>\n</pitch>\n'
        self.assertEqual(pitch.to_string(), result)

    def test_change_alter_1(self):
        self.pitch.alter = Alter(-1)
        result = '<pitch>\n  <step>C</step>\n  <alter>-1</alter>\n  <octave>4</octave>\n</pitch>\n'
        self.assertEqual(self.pitch.to_string(), result)

    def test_change_alter_2(self):
        self.pitch.alter = Alter(-1)
        self.pitch.alter = Alter(1)
        result = '<pitch>\n  <step>C</step>\n  <alter>1</alter>\n  <octave>4</octave>\n</pitch>\n'
        self.assertEqual(self.pitch.to_string(), result)

    def test_set_children(self):
        pitch = Pitch(step='E')
        result = '<pitch>\n  <step>E</step>\n  <octave>4</octave>\n</pitch>\n'
        self.assertEqual(pitch.to_string(), result)
