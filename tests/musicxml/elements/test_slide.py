from unittest import TestCase
from musicscore.musicxml.types.complextypes.notations import Slide


class Test(TestCase):
    def test_1(self):
        slide = Slide(type='start')
        result = '''<slide number="1" type="start"/>
'''
        self.assertEqual(slide.to_string(), result)
