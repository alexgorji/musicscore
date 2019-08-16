from unittest import TestCase

from musicscore.musicxml.elements.note import Notations
from musicscore.musicxml.types.complextypes.notations import Ornaments
from musicscore.musicxml.types.complextypes.ornaments import Tremolo, Turn
from musicscore.musicxml.types.complextypes.scorepart import PartAbbreviation


class Test(TestCase):
    def test_1(self):
        pa = PartAbbreviation('bla')
        pa.font_size = 10
        result = """<part-abbreviation font-size="10">bla</part-abbreviation>
"""
        self.assertEqual(pa.to_string(), result)
