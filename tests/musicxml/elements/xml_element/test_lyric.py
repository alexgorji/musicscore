from unittest import TestCase

from musicscore.musicxml.groups.common import FootNote
from musicscore.musicxml.types.complextypes.lyric import ComplexTypeLyric, Extend, Syllabic, Text, EndLine


class Test(TestCase):
    def setUp(self):
        self.lyric = ComplexTypeLyric()
        self.lyric.add_child(Extend())
        self.lyric.add_child(Syllabic('begin'))
        self.lyric.add_child(Text('bla'))
        # self.lyric.add_child(Elision('00A0'))
        # self.lyric.add_child(Elision('00A0'))
        self.lyric.add_child(EndLine())
        self.lyric.add_child(FootNote('foot'))

    def test_1(self):
        result = self.lyric.to_string()
        expected = '''<lyric number="1">
  <syllabic>begin</syllabic>
  <text>bla</text>
  <extend/>
  <end-line/>
  <footnote>foot</footnote>
</lyric>
'''
        self.assertEqual(expected, result)