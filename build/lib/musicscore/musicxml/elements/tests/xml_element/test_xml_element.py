from unittest import TestCase

from musicscore.dtd.dtd import DTDError, Sequence, Element
from musicscore.musicxml.elements.xml_element import XMLElement
from lxml import etree as et


class TestXMLElement(TestCase):

    def setUp(self):
        self.xml = XMLElement('root')

    def test_tag(self):
        self.assertEqual(self.xml.tag, 'root')

    def test_text(self):
        self.xml.text = 2
        self.assertEqual(self.xml.text, 2)

    def test_add_child(self):
        child = 'child'
        with self.assertRaises(DTDError):
            self.xml.add_child(child)
        #
        # child = XMLElement('child')
        # self.xml.add_child(child)
        # self.assertEqual(self.xml.get_children(), [child])

    # def test_remove_old_child_by_tag(self):
    #     children = [XMLElement('child-1'), XMLElement('child-2')]
    #     for child in children:
    #         self.xml.add_child(child)
    #     self.xml.remove_old_child_by_tag(children[0].tag)
    #     self.assertEqual(self.xml.get_children(), [children[1]])

    # def test_to_xml(self):
    #     children = [XMLElement('child-1'), XMLElement('child-2')]
    #     for child in children:
    #         self.xml.add_child(child)
    #     xml = self.xml._to_xml()
    #     self.assertIsInstance(xml, et._Element)

    # def test_to_string(self):
    #     class Child1(XMLElement):
    #         def __init__(self):
    #             super().__init__('child-1')
    #
    #     class Child2(XMLElementGroup):
    #         def __init__(self):
    #             super().__init__('child-2')
    #
    #     class Sibling(XMLElement):
    #         def __init__(self):
    #             super().__init__('child-2')
    #
    #     children = [Child1(), Child2()]
    #     children[1].add_sibling(Sibling())
    #     children[1].add_sibling(Sibling())
    #
    #     for child in children:
    #         self.xml.add_child(child)
    #     self.assertEqual(self.xml.to_string(), '<root>\n  <child-1/>\n  <child-2/>\n  <child-2/>\n</root>\n')
    #
    # def test_text_to_string(self):
    #     self.xml.text = 'test'
    #     self.assertEqual(self.xml.to_string(), '<root>test</root>\n')

    # def test_find_child_by_tag(self):
    #     children = [XMLElement('child-1'), XMLElement('child-2'), XMLElement('child-3')]
    #     for child in children:
    #         self.xml.add_child(child)
    #     self.assertEqual(self.xml.find_child_by_tag('child-3').tag, 'child-3')

    # def test_sort_children(self):
    #
    #     class Child1(XMLElement):
    #         def __init__(self):
    #             super().__init__('child1')
    #
    #     class Child2(XMLElement):
    #         def __init__(self):
    #             super().__init__('child2')
    #
    #     class Child3(XMLElementGroup):
    #         def __init__(self):
    #             super().__init__('child3')
    #
    #     children = [Child1(), Child2(), Child3(), Child2()]
    #     for child in children:
    #         self.xml.add_child(child)
    #
    #     self.xml._CHILDREN_ORDERED = True
    #     self.xml._CHILDREN_TYPES = [Child2, Child3, Child1]
    #
    #     self.xml._sort_children()
    #     self.assertEqual([child.tag for child in self.xml.get_children()], ['child2', 'child3', 'child1', 'child2'])

    # def test_attributes(self):
    #     self.xml.set_attribute('att1', 2)
    #     self.xml.set_attribute('att2', 'a')
    #     self.xml.set_attribute('att3', None)
    #     result = '<root att1="2" att2="a" att3="None"/>\n'
    #     self.assertEqual(self.xml.to_string(), result)
