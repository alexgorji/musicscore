from musicscore.musicxml.types.simple_type import CommaSeparatedText
from unittest import TestCase


class TestComma(TestCase):
    def test_comma(self):
        comma = CommaSeparatedText('bla,  bla, bla')
        with self.assertRaises(ValueError):
            comma = CommaSeparatedText(', bla, bla')
        with self.assertRaises(ValueError):
            comma = CommaSeparatedText('bla, bla,')

