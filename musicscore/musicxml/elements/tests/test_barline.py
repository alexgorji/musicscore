from unittest import TestCase
# from musicscore.musicxml.elements.barline import Barline, BarStyle
from musicscore.musicxml.elements.barline import Barline, BarStyle


class TestBarline(TestCase):
    def setUp(self):
        self.barline = Barline()

    def test_barline(self):
        self.barline.location = 'left'
        result = '''<barline location="left"/>
'''
        self.assertEqual(self.barline.to_string(), result)

        with self.assertRaises(ValueError):
            self.barline.location = 'bla'

        with self.assertRaises(ValueError):
            self.barline.add_child(BarStyle('bla'))



