import os
from unittest import TestCase

from musicscore.musictree.treechord import TreeChord

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):

    def test_1(self):
        chord = TreeChord(quarter_duration=4, midis=[60])
        self.assertIsNone(chord.staff_number)

    def test_2(self):
        chord = TreeChord(quarter_duration=4, midis=[60])
        chord.staff_number = 1
        expected = 1
        actual = chord.staff_number
        self.assertEqual(expected, actual)

    def test_3(self):
        chord = TreeChord(quarter_duration=4, midis=[60])
        chord.staff_number = 1
        chord.staff_number = 2
        expected = 2
        actual = chord.staff_number
        self.assertEqual(expected, actual)
