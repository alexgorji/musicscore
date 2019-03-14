from musicscore.dtd.dtd import ChildOccurrenceDTDConflict
from musicscore.musicxml.elements.xml_example import XMLExample, XMLExampleChild1, XMLExampleChild2

from unittest import TestCase


class TestExample(TestCase):
    def setUp(self):
        self.example = XMLExample()

    def test_example(self):
        with self.assertRaises(ValueError):
            self.example.attribute_example = 2
        self.example.attribute_example = 'one'
        self.example.value = 2
        result = '''<example attribute-example="one">2</example>
'''
        self.assertEqual(self.example.to_string(), result)
        self.example.value = None
        self.example.add_child(XMLExampleChild2())
        self.example.add_child(XMLExampleChild1())
        self.example.add_child(XMLExampleChild2())
        result = '''<example attribute-example="one">
  <example-child-1/>
  <example-child-2/>
  <example-child-2/>
</example>
'''
        self.assertEqual(self.example.to_string(), result)
        with self.assertRaises(ChildOccurrenceDTDConflict):
            self.example.add_child(XMLExampleChild1())
