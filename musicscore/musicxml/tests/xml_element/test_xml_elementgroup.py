from unittest import TestCase
from musicscore.musicxml.elements.xml_element import XMLElementGroup, XMLElement


class TestXMLElementGroup(TestCase):

    def setUp(self):
        self.xml_group = XMLElementGroup('lyric')

    def test_append_sibling(self):
        self.xml_group.append_sibling(XMLElement('lyric'))
        self.xml_group.append_sibling(XMLElement('lyric'))
        self.xml_group.append_sibling()
        self.xml_group.get_siblings()[1].text = 'test_1'
        self.assertEqual(self.xml_group.get_siblings()[1].text, 'test_1')
        self.xml_group.get_siblings()[2].text = 'test_2'
        self.assertEqual(self.xml_group.get_siblings()[2].to_string(), '<lyric>test_2</lyric>\n')
        with self.assertRaises(IndexError):
            print(self.xml_group.get_siblings()[3])
        with self.assertRaises(ValueError):
            self.xml_group.append_sibling(XMLElement('non-lyric'))

        for lyric in self.xml_group:
            lyric




