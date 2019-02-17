from musicscore.musicxml.elements.xml_note import *
from unittest import TestCase


class XMLTest(TestCase):
    def setUp(self):
        self.n = XMLNote(XMLRest(), 2)

    def test_xml(self):
        result = '''<note>
  <rest/>
  <duration>2</duration>
</note>
'''
        self.assertEqual(self.n.to_string(), result)
