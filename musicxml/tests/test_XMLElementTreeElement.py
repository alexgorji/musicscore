from contextlib import redirect_stdout
from pathlib import Path
from unittest import TestCase
import xml.etree.ElementTree as ET

from musicxml.util.helperclasses import MusicXmlTestCase
from musicxml.xmlelement import XMLElementTreeElement


class TestXMLElementTreeElement(MusicXmlTestCase):
    # def setUp(self) -> None:
    #     with open(xsd_path) as file:
    #         xmltree = ET.parse(file)
    #     self.root = xmltree.getroot()
    #     ns = '{http://www.w3.org/2001/XMLSchema}'
    #     self.above_below_simple_type_element = self.root.find(f"{ns}simpleType[@name='above-below']")
    #     self.yes_no_number_simple_type_element = self.root.find(f"{ns}simpleType[@name='yes-no-number']")
    #     self.complex_type_element = self.root.find(f"{ns}complexType[@name='fingering']")
    #     self.all_simple_type_elements = [XMLElementTreeElement(simpletype) for simpletype in
    #                                      self.root.findall(f"{ns}simpleType")]

    def test_write_all_tags(self):
        def get_all_tags():
            output = []
            for node in tree.traverse():
                if node.tag not in output:
                    output.append(node.tag)
            return output

        with open(Path(__file__).parent / 'musicxml_4_0_summary.txt', 'w+') as f:
            tree = XMLElementTreeElement(self.root)
            with redirect_stdout(f):
                print('All tags: ' + str(get_all_tags()))
                for child in tree.get_children():
                    print('============')
                    print(child.tree_repr())

    def test_xml_property(self):
        """
        Test that a XMLElementGenerator must get an xml element
        :return: 
        """""
        with self.assertRaises(TypeError):
            XMLElementTreeElement()
        with self.assertRaises(TypeError):
            XMLElementTreeElement('Naja')

        assert isinstance(self.above_below_simple_type_element.xml_element_tree_element, ET.Element)

    def test_xml_element_tag(self):
        assert self.above_below_simple_type_element.tag == 'simpleType'

    def test_xml_element_class_name(self):
        assert self.above_below_simple_type_element.class_name == 'XMLSimpleTypeAboveBelow'

    def test_get_doc(self):
        assert self.above_below_simple_type_element.get_doc() == 'The above-below type is used to indicate whether one element appears above or below another element.'

    def test_name(self):
        assert self.above_below_simple_type_element.name == 'above-below'

    def test_traverse(self):
        expected = ['complexType', 'annotation', 'documentation', 'simpleContent', 'extension', 'attribute',
                    'attribute', 'attributeGroup', 'attributeGroup']
        assert [node.tag for node in self.complex_type_element.traverse()] == expected

    def test_get_children(self):
        xml = """<xs:extension xmlns:xs="http://www.w3.org/2001/XMLSchema" 
                    base="xs:string">
        				<xs:attribute name="substitution" type="yes-no"/>
        				<xs:attribute name="alternate" type="yes-no"/>
        				<xs:attributeGroup ref="print-style"/>
        				<xs:attributeGroup ref="placement"/>
        		</xs:extension>"""
        el = XMLElementTreeElement(ET.fromstring(xml))
        assert [child.tag for child in el.get_children()] == ['attribute', 'attribute', 'attributeGroup',
                                                              'attributeGroup']

    def test_iterate_leaves(self):
        assert [child.tag for child in self.complex_type_element.iterate_leaves()] == ['documentation', 'attribute',
                                                                                       'attribute',
                                                                                       'attributeGroup',
                                                                                       'attributeGroup']

    def test_compact_repr(self):
        assert [node.compact_repr for node in self.complex_type_element.traverse()] == ['complexType@name=fingering',
                                                                                        'annotation',
                                                                                        'documentation',
                                                                                        'simpleContent',
                                                                                        'extension@base=xs:string',
                                                                                        'attribute@name=substitution@type=yes-no',
                                                                                        'attribute@name=alternate@type=yes-no',
                                                                                        'attributeGroup@ref=print-style',
                                                                                        'attributeGroup@ref=placement']

    def test_str(self):
        assert str(self.complex_type_element) == "XMLElementTreeElement complexType@name=fingering"

    def test_repr(self):
        assert [repr(node) for node in self.complex_type_element.traverse()] == [
            'XMLElementTreeElement(tag=complexType, name=fingering)',
            'XMLElementTreeElement(tag=annotation)',
            'XMLElementTreeElement(tag=documentation)',
            'XMLElementTreeElement(tag=simpleContent)',
            'XMLElementTreeElement(tag=extension, base=xs:string)',
            'XMLElementTreeElement(tag=attribute, name=substitution type=yes-no)',
            'XMLElementTreeElement(tag=attribute, name=alternate type=yes-no)',
            'XMLElementTreeElement(tag=attributeGroup, ref=print-style)',
            'XMLElementTreeElement(tag=attributeGroup, ref=placement)']

    def test_get_attributes(self):
        assert [{}, {'name': 'substitution', 'type': 'yes-no'}, {'name': 'alternate', 'type': 'yes-no'},
                {'ref': 'print-style'}, {'ref': 'placement'}] == [leaf.get_attributes() for leaf in
                                                                  self.complex_type_element.iterate_leaves()]

    def test_get_parent(self):
        grandparent = self.complex_type_element
        parent = grandparent.get_children()[1]
        child = parent.get_children()[0]
        grandchild = child.get_children()[0]

        assert grandchild.get_parent() == child
        assert child.get_parent() == parent
        assert parent.get_parent() == grandparent
        assert grandparent.get_parent() is None

    def test_get_xsd(self):
        expected_1 = """<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="above-below">
		<xs:annotation>
			<xs:documentation>The above-below type is used to indicate whether one element appears above or below another element.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="above" />
			<xs:enumeration value="below" />
		</xs:restriction>
	</xs:simpleType>
"""
        expected_2 = """<xs:complexType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="fingering">
		<xs:annotation>
			<xs:documentation>Fingering is typically indicated 1,2,3,4,5. Multiple fingerings may be given, typically to substitute fingerings in the middle of a note. The substitution and alternate values are "no" if the attribute is not present. For guitar and other fretted instruments, the fingering element represents the fretting finger; the pluck element represents the plucking finger.</xs:documentation>
		</xs:annotation>
		<xs:simpleContent>
			<xs:extension base="xs:string">
				<xs:attribute name="substitution" type="yes-no" />
				<xs:attribute name="alternate" type="yes-no" />
				<xs:attributeGroup ref="print-style" />
				<xs:attributeGroup ref="placement" />
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
"""
        assert self.above_below_simple_type_element.get_xsd() == expected_1
        assert self.complex_type_element.get_xsd() == expected_2

    def test_get_restriction(self):
        assert self.above_below_simple_type_element.get_restriction().tag == 'restriction'
        assert self.complex_type_element.get_restriction() is None

    def test_get_union(self):
        assert self.above_below_simple_type_element.get_union_member_types() is None
        assert self.yes_no_number_simple_type_element.get_union_member_types() == ['yes-no',
                                                                                   'xs:decimal']

    def test_base_class_names(self):
        all_restriction_bases = []
        for simpletype in self.all_simple_type_elements:
            if simpletype.base_class_names not in all_restriction_bases:
                all_restriction_bases.append(simpletype.base_class_names)

        assert all_restriction_bases == [['XsToken'], ['XsPositiveInteger'], ['XsDecimal'], ['XsString'],
                                         ['XMLSimpleTypeCommaSeparatedText'], ['XsDecimal', 'XMLSimpleTypeCssFontSize'],
                                         ['XsNonNegativeInteger'], ['XMLSimpleTypeDivisions'], ['XsNMTOKEN'],
                                         ['XMLSimpleTypeSmuflGlyphName'], ['XMLSimpleTypeYesNo', 'XsDecimal'],
                                         ['XsDate'], ['XsInteger'],
                                         ['XMLSimpleTypeSystemRelationNumber'], ['XMLSimpleTypeNoteTypeValue']]
