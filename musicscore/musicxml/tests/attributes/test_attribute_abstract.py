from unittest import TestCase
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.elements.xml_element import XMLElement2


class AttributeSub(XMLElement2, AttributeAbstract):
    def __init__(self):
        super().__init__(tag='attribute-sub')


class TestAttributeAbstract(TestCase):
    def setUp(self):
        self.attribute_sub = AttributeSub()

    def test_attribute_abstract(self):
        AttributeSub._ATTRIBUTES = ['print-object']
        self.attribute_sub.generate_attribute(attribute_name='print-object', attribute_value=2, type_string='Tenths')
        self.assertEqual(self.attribute_sub.print_object, 2)
        with self.assertRaises(TypeError):
            self.attribute_sub.print_object = 'b'
