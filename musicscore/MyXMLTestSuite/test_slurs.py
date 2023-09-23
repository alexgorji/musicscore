import inspect

from musicscore import Chord, Score
from musicscore.tests.util import IdTestCase, generate_path
from musicxml.xmlelement.xmlelement import XMLSlur


class TestSlurs(IdTestCase):
    def setUp(self):
        super().setUp()
        self.score = Score()
        self.part = self.score.add_part('p1')

    def test_slurs_chords(self):
        ch1 = Chord([60, 62], 2)
        ch2 = Chord([70, 65], 2)
        ch3 = Chord(60, 4)
        ch1.add_x(XMLSlur(type='start'))
        ch2.add_x(XMLSlur(type='stop'))
        ch2.add_x(XMLSlur(type='start'))
        ch3.add_x(XMLSlur(type='stop'))
        self.part.add_chord(ch1)
        self.part.add_chord(ch2)
        self.part.add_chord(ch3)
        path = generate_path(inspect.currentframe())
        self.score.export_xml(path)

    def test_slurs_different_line_types(self):
        line_types = ['dashed', 'dotted', 'solid', 'wavy']
        for lt in line_types:
            ch1 = Chord(72, 2)
            ch1.add_lyric(lt)
            ch2 = Chord(72, 2)
            ch1.add_x(XMLSlur(type='start', line_type=lt))
            ch2.add_x(XMLSlur(type='stop'))
            self.part.add_chord(ch1)
            self.part.add_chord(ch2)
        path = generate_path(inspect.currentframe())
        self.score.export_xml(path)
