from unittest import TestCase
import musicscore.musicxml.elements.timewise as timewise
from musicscore.musicxml.elements.note import Note, Beam


class Test(TestCase):
    def setUp(self):
        self.measure = timewise.Measure('1')

    def test_number(self):
        self.assertTrue(isinstance(self.measure.number, str))
        with self.assertRaises(TypeError):
            self.measure.number = 3

    def test_non_controlling(self):
        with self.assertRaises(ValueError):
            self.measure.non_controlling = 2

        self.measure.non_controlling = 'yes'
        self.assertTrue(self.measure.non_controlling == 'yes')

    def test_add_note(self):
        part = self.measure.add_child(timewise.Part(id='bla'))
        note = part.add_child(Note())
        note.add_child(Beam('end'))
        with self.assertRaises(TypeError):
            self.measure.number = 3
