from unittest import TestCase

from musicxml.xmlelement.xmlelement import *


class TestChoice(TestCase):
    def test_xml_element_with_choice(self):
        xml_encoding = XMLEncoding()
        xml_encoding.add_child(XMLEncoder('bla'))
        xml_encoding.add_child(XMLEncoder('blue'))

        assert len(xml_encoding.get_children()) == 2
