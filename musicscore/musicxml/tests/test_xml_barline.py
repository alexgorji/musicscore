from musicscore.musicxml.elements.xml_barline import XMLBarline
from unittest import TestCase


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

