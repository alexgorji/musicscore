from unittest import TestCase
from musicscore.musicxml.types.complextypes.notations import Slur


class Test(TestCase):
    def test_1(self):
        slur = Slur(type='start')
        result = '''<slur number="1" type="start"/>
'''
        self.assertEqual(slur.to_string(), result)
