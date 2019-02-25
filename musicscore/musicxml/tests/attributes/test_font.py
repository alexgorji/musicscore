from musicscore.musicxml.attributes.print_style import Font
from musicscore.musicxml.elements.xml_note import XMLPitch

from unittest import TestCase


class XMLWithFont(XMLPitch, Font):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TestFont(TestCase):
    def setUp(self):
        self.font = XMLWithFont()

    def test_font(self):
        self.font.font_weight = 'normal'
        self.font.font_size = 10
        result = '''<pitch font-size="10" font-weight="normal">
  <step>C</step>
  <octave>4</octave>
</pitch>
'''
        self.assertEqual(self.font.to_string(), result)
        with self.assertRaises(TypeError):
            self.font.font_size = 'b'
