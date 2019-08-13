from unittest import TestCase
from musicscore.musicxml.elements.barline import Barline, BarStyle
from musicscore.musicxml.elements.timewise import Part


class Test(TestCase):
    def setUp(self):
        self.barline = Barline()

    def test_1(self):
        self.barline.location = 'left'
        result = '''<barline location="left"/>
'''
        self.assertEqual(self.barline.to_string(), result)

        with self.assertRaises(ValueError):
            self.barline.location = 'bla'

        with self.assertRaises(ValueError):
            self.barline.add_child(BarStyle('bla'))

    def test_2(self):
        part = Part(id='1')
        bl = part.add_child(Barline())
        bl.add_child(BarStyle('light-light'))

        result = '''<part id="1">
  <barline>
    <bar-style>light-light</bar-style>
  </barline>
</part>
'''

        self.assertEqual(part.to_string(), result)
