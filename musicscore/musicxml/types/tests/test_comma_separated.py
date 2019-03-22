from musicscore.musicxml.types.simple_type import TypeCommaSeparatedText
from unittest import TestCase


class TestComma(TestCase):
    def test_comma(self):
        comma = TypeCommaSeparatedText('bla,  bla, bla')
        with self.assertRaises(ValueError):
            comma = TypeCommaSeparatedText(', bla, bla')
        with self.assertRaises(ValueError):
            comma = TypeCommaSeparatedText('bla, bla,')

