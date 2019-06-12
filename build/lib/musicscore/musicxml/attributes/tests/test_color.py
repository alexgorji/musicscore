from musicscore.musicxml.attributes.printstyle import Color
from musicscore.musicxml.elements.xml_element import XMLElement
from unittest import TestCase


class Colored(XMLElement, Color):
    """"""
    # _ATTRIBUTES = ['color']

    def __init__(self, *args, **kwargs):
        super().__init__(tag='color_test', *args, **kwargs)


class TestColor(TestCase):
    def setUp(self):
        self.colored = Colored()

    def test_color(self):
        self.colored.color = '#800080'
        result = '''<color_test color="#800080"/>
'''
        self.assertEqual(self.colored.to_string(), result)
        self.colored.color = '#40800080'
        self.colored.text = 'bla'
        result = '''<color_test color="#40800080">bla</color_test>
'''
        self.assertEqual(self.colored.to_string(), result)
        with self.assertRaises(ValueError):
            self.colored.color = 'b0l0a080'
