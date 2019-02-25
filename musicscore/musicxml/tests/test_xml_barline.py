from musicscore.musicxml.elements.xml_barline import XMLBarline, XMLBarStyle
from unittest import TestCase
from musicscore.musicxml.types.simple_type import BarStyleType


class TestBarline(TestCase):
    def setUp(self):
        self.barline = XMLBarline()

    def test_barline(self):
        self.barline.location = 'left'
        result = '''<barline location="left"/>
'''
        self.assertEqual(self.barline.to_string(), result)
        with self.assertRaises(ValueError):
            self.barline.location = 'bla'

        barsytle = self.barline.add_child(XMLBarStyle('bla'))
        print(self.barline.to_string())
        barsytle.value = 'none'



