from py_musicxml.elements.xml_note import *
from unittest import TestCase

class XMLTest(TestCase):
    def setUp(self):
        self.n = XMLNote(XMLRest(), 2)

    def test_xml(self):
        print(self.n.to_string())




