from unittest import TestCase

from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.simple_type import TypeBarStyle


class Bared(XMLElement, TypeBarStyle):

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag='test_bar', value=value, *args, **kwargs)


class TestBarstyleType(TestCase):
    def test_barstyle(self):
        bst = TypeBarStyle('regular')
        with self.assertRaises(ValueError):
            bst = TypeBarStyle('bla')


class TestBaredXML(TestCase):
    def test_barstyled_xml(self):
        bared = Bared('light-light')
        # bared.value = 'regular'
        with self.assertRaises(ValueError):
            bared.value = 'bla'
        result = '''<test_bar>light-light</test_bar>
'''
        self.assertEqual(bared.to_string(), result)
