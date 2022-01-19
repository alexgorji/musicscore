from unittest import TestCase

from musicxml.xmlelement.xmlelement import XMLPitch


class TestMusicXml(TestCase):
    def test_pitch(self):
        pitch = XMLPitch()
        pitch.to_string()