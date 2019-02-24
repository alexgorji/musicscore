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
        print(self.font.to_string())
        self.font.font_weight = 'normal'
        self.font.font_size = 10
        print(self.font.to_string())
