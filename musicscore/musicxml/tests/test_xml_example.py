from musicscore.musicxml.xml_example import XMLExample
from unittest import TestCase


class TestExample(TestCase):
    def setUp(self):
        self.example = XMLExample()

    def test_example(self):
        print(self.example.to_string())
