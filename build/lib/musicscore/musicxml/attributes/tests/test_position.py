from unittest import TestCase
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.elements.xml_element import XMLElement


class Positioned(XMLElement, Position):
    _ATTRIBUTES = ['default-x', 'default-y', 'relative-x', 'relative-y']

    def __init__(self, *args, **kwargs):
        super().__init__(tag='positioned', *args, **kwargs)


class PositionTest(TestCase):
    def setUp(self):
        self.positioned = Positioned()

    def test_position(self):
        result = '''<positioned/>
'''
        self.assertEqual(self.positioned.to_string(), result)

        self.positioned.default_x = 2
        result = '''<positioned default-x="2"/>
'''
        self.assertEqual(self.positioned.to_string(), result)

        self.positioned.default_y = 3
        result = '''<positioned default-x="2" default-y="3"/>
'''
        self.assertEqual(self.positioned.to_string(), result)

        self.positioned.default_x = None
        result = '''<positioned default-y="3"/>
'''
        self.assertEqual(self.positioned.to_string(), result)

        self.positioned.relative_y = 2
        result = '''<positioned default-y="3" relative-y="2"/>
'''
        self.assertEqual(self.positioned.to_string(), result)

        self.positioned.default_x = 5
        result = '''<positioned default-x="5" default-y="3" relative-y="2"/>
'''
        self.assertEqual(self.positioned.to_string(), result)
