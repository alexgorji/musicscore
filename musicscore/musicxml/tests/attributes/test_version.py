from unittest import TestCase

from musicscore.musicxml.attributes.document_attributes import Version
from musicscore.musicxml.elements.xml_element import XMLElement


class TestTimewise(TestCase):
    def setUp(self):
        class Bla(XMLElement, Version):
            def __init__(self, *args, **kwargs):
                super().__init__(tag='bal', *args, **kwargs)
        self.bla = Bla()

    def test_version(self):

        self.bla.version = '10'
        result = '''<bal version="10"/>
'''
        self.assertEqual(self.bla.to_string(), result)
