from unittest import TestCase

from musicscore.musictree.midi import midi_to_frequency, frequency_to_midi


class Test(TestCase):
    def test_1(self):
        midi = 60
        self.assertEqual(midi_to_frequency(midi), 261.6255653005986)

    def test_2(self):
        midi = 69
        self.assertEqual(midi_to_frequency(midi, a4=430), 430)

    def test_3(self):
        frequency = 220
        self.assertEqual(frequency_to_midi(frequency), 57)
