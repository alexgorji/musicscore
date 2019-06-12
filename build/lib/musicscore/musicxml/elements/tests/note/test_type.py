from unittest import TestCase

from musicscore.musicxml.elements.note import Type


class TestNoteType(TestCase):
    def setUp(self):
        self.type = Type('quarter')

    def test_type(self):
        result = '''<type>quarter</type>
'''
        self.assertEqual(self.type.to_string(), result)

        with self.assertRaises(ValueError):
            Type('bla')
