from unittest import TestCase

from musicscore.musicxml.elements.note import Type


class Test(TestCase):
    def test_1(self):
        type = Type('quarter', size='full')
        result = """<type size="full">quarter</type>
"""
        self.assertEqual(type.to_string(), result)