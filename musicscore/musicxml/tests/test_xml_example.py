from musicscore.musicxml.xml_example import XMLExample
from unittest import TestCase


class TestExample(TestCase):
    def setUp(self):
        self.example = XMLExample()

    def test_example(self):
        with self.assertRaises(ValueError):
            self.example.attribute_example = 2
        self.example.attribute_example = 'one'
        self.example.value = 2
        result = '''<example attribute-example="one">2</example>
'''
        self.assertEqual(self.example.to_string(), result)