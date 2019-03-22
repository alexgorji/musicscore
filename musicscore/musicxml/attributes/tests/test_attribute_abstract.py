from unittest import TestCase
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.elements.xml_element import XMLElement


class AttributeSub(XMLElement, AttributeAbstract):
    def __init__(self):
        super().__init__(tag='attribute-sub')
        self._ATTRIBUTES.append('print-object')


class TestAttributeAbstract(TestCase):
    def setUp(self):
        self.attribute_sub = AttributeSub()

    def test_attribute_abstract(self):
        self.attribute_sub.generate_attribute(attribute_name='print-object', attribute_value=2, type_string='TypeTenths')
        self.assertEqual(self.attribute_sub.print_object, 2)
        with self.assertRaises(TypeError):
            self.attribute_sub.print_object = 'b'
