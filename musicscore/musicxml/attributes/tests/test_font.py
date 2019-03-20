from musicscore.musicxml.attributes.font import Font
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.elements.fullnote import Pitch


from unittest import TestCase


class XMLWithFont(Pitch, Font, Position):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TestFont(TestCase):
    def setUp(self):
        self.font = XMLWithFont()

    def test_font(self):

        self.font.font_weight = 'bold'
        self.font.font_size = 8

        with self.assertRaises(TypeError):
            self.font.font_size = 'b'

        self.font.font_style = 'italic'
        self.font.font_family = 'Arial, Times'

        result = '''<pitch font-family="Arial, Times" font-style="italic" font-size="8" font-weight="bold">
  <step>C</step>
  <octave>4</octave>
</pitch>
'''
        self.assertEqual(self.font.to_string(), result)
