from unittest import TestCase
from musicscore.musicxml.elements.xml_note import XMLPitch, XMLStep, XMLAlter, XMLOctave


class TestPitch(TestCase):
    def setUp(self):
        self.pitch = XMLPitch()

    def test_to_string(self):
        result = '<pitch>\n  <step>C</step>\n  <octave>4</octave>\n</pitch>\n'
        self.assertEqual(self.pitch.to_string(), result)

    def test_arguments(self):
        pitch = XMLPitch(XMLStep('D'), octave=XMLOctave(7), alter=XMLAlter(1.5))
        result = '<pitch>\n  <step>D</step>\n  <alter>1.5</alter>\n  <octave>7</octave>\n</pitch>\n'
        self.assertEqual(pitch.to_string(), result)

    def test_change_alter(self):
        self.pitch.alter = XMLAlter(-1)
        result = '<pitch>\n  <step>C</step>\n  <alter>-1</alter>\n  <octave>4</octave>\n</pitch>\n'
        self.assertEqual(self.pitch.to_string(), result)
        self.pitch.alter = XMLAlter(1)
        result = '<pitch>\n  <step>C</step>\n  <alter>1</alter>\n  <octave>4</octave>\n</pitch>\n'
        self.assertEqual(self.pitch.to_string(), result)

    def test_set_children(self):
        pitch = XMLPitch(step='E')
        result = '<pitch>\n  <step>E</step>\n  <octave>4</octave>\n</pitch>\n'
        self.assertEqual(pitch.to_string(), result)
