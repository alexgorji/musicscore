import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from pathlib import Path

from musicxml.tests.util import MusicXmlTestCase
from musicxml.xmlelement.xmlelement import XMLType, XMLNote
from musicxml.xsd.xsdtree import XSDTree


class TestXSDTree(MusicXmlTestCase):
    """
    XSDTree is a representation of all needed information for creating an XSD Class.
    """

    def test_write_all_tags(self):
        """
        Write the summary of all music xml nodes in a files (musicxml_4_0_summary.txt)
        """

        def get_all_tags():
            output = []
            for node in tree.traverse():
                if node.tag not in output:
                    output.append(node.tag)
            return output

        with open(Path(__file__).parent / 'musicxml_4_0_summary.txt', 'w+') as f:
            tree = XSDTree(self.root)
            with redirect_stdout(f):
                print('All tags: ' + str(get_all_tags()))
                for child in tree.get_children():
                    print('============')
                    print(child.tree_representation())

    def test_xsd_property(self):
        """
        Test that an XSDTree element must get an xsd tree element while initiating.
        Example:
        with open(xsd_path) as file:
            xsdtree = ET.parse(file)
        root = xsdtree.getroot()
        ns = '{http://www.w3.org/2001/XMLSchema}'
        XSDTree(root.find(f"{ns}simpleType["f"@name='above-below']"))
        """""
        with self.assertRaises(TypeError):
            XSDTree()
        with self.assertRaises(TypeError):
            XSDTree('Naja')

        assert isinstance(self.above_below_simple_type_xsd_element.xml_element_tree_element, ET.Element)

    def test_xml_element_tag(self):
        """
        Test that the tag attribute of an XSDTree element represents th tag name in musicxml xsd structure.
        """
        assert self.above_below_simple_type_xsd_element.tag == 'simpleType'

    def test_music_xml_class_name(self):
        """
        Test that an XSDTree element has a xsd_element_class_name attribute. This class name is generated automatically and is used as the
        name of the XSDTreeElement to be created.
        """
        assert self.above_below_simple_type_xsd_element.xsd_element_class_name == 'XSDSimpleTypeAboveBelow'

    def test_name(self):
        """
        Test that an XSDTree element has a name attribute representing the corresponding name attribute in musicxml xsd structure.
        Example:
        <xs:simpleType name="above-below">
    <xs:annotation>
        <xs:documentation>The above-below type is used to indicate whether one element appears above or below another element.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="above"/>
        <xs:enumeration value="below"/>
    </xs:restriction>
        </xs:simpleType>
        """
        assert self.above_below_simple_type_xsd_element.name == 'above-below'

    def test_traverse(self):
        """
        Test the traverse method of an XSDTree element traverses over all existing nodes.
        """
        """
        <xs:complexType name="fingering">
            <xs:annotation>
                <xs:documentation>Fingering is typically indicated 1,2,3,4,5. Multiple fingerings may be given, typically to substitute fingerings in the middle of a note. The substitution and alternate values are "no" if the attribute is not present. For guitar and other fretted instruments, the fingering element represents the fretting finger; the pluck element represents the plucking finger.</xs:documentation>
            </xs:annotation>
            <xs:simpleContent>
                <xs:extension base="xs:string">
                    <xs:attribute name="substitution" type="yes-no"/>
                    <xs:attribute name="alternate" type="yes-no"/>
                    <xs:attributeGroup ref="print-style"/>
                    <xs:attributeGroup ref="placement"/>
                </xs:extension>
            </xs:simpleContent>
        </xs:complexType>
        """
        expected = ['complexType', 'annotation', 'documentation', 'simpleContent', 'extension', 'attribute',
                    'attribute', 'attributeGroup', 'attributeGroup']
        assert [node.tag for node in self.complex_type_xsd_element.traverse()] == expected

    def test_get_children(self):
        xml = """<xs:extension xmlns:xs="http://www.w3.org/2001/XMLSchema" 
                    base="xs:string">
                        <xs:attribute name="substitution" type="yes-no"/>
                        <xs:attribute name="alternate" type="yes-no"/>
                        <xs:attributeGroup ref="print-style"/>
                        <xs:attributeGroup ref="placement"/>
                </xs:extension>"""
        el = XSDTree(ET.fromstring(xml))
        assert [child.tag for child in el.get_children()] == ['attribute', 'attribute', 'attributeGroup',
                                                              'attributeGroup']

    def test_iterate_leaves(self):
        assert [child.tag for child in self.complex_type_xsd_element.iterate_leaves()] == ['documentation', 'attribute',
                                                                                           'attribute',
                                                                                           'attributeGroup',
                                                                                           'attributeGroup']

    def test_compact_repr(self):
        """
        Test the compact representation of an XSDTree Element. It consists of node name and its attribute if exists.
        """
        assert [node.compact_repr for node in self.complex_type_xsd_element.traverse()] == ['complexType@name=fingering',
                                                                                            'annotation',
                                                                                            'documentation',
                                                                                            'simpleContent',
                                                                                            'extension@base=xs:string',
                                                                                            'attribute@name=substitution@type=yes-no',
                                                                                            'attribute@name=alternate@type=yes-no',
                                                                                            'attributeGroup@ref=print-style',
                                                                                            'attributeGroup@ref=placement']

    def test_str(self):
        """
        Test __str__ magic method. It returns class name + compact representation
        """
        assert str(self.complex_type_xsd_element) == "XSDTree complexType@name=fingering"

    def test_repr(self):
        """
        Test __repr__ magic method. It returns a comprehensive representation of the XSDTree element.
        """
        assert [repr(node) for node in self.complex_type_xsd_element.traverse()] == [
            'XSDTree(tag=complexType, name=fingering)',
            'XSDTree(tag=annotation)',
            'XSDTree(tag=documentation)',
            'XSDTree(tag=simpleContent)',
            'XSDTree(tag=extension, base=xs:string)',
            'XSDTree(tag=attribute, name=substitution type=yes-no)',
            'XSDTree(tag=attribute, name=alternate type=yes-no)',
            'XSDTree(tag=attributeGroup, ref=print-style)',
            'XSDTree(tag=attributeGroup, ref=placement)']

    def test_get_attributes(self):
        """
        Test get_attribute method: returns a dictionary consisting of all attributes, incl. name.
        """
        assert [{}, {'name': 'substitution', 'type': 'yes-no'}, {'name': 'alternate', 'type': 'yes-no'},
                {'ref': 'print-style'}, {'ref': 'placement'}] == [leaf.get_attributes() for leaf in
                                                                  self.complex_type_xsd_element.iterate_leaves()]

    def test_get_parent(self):
        grandparent = self.complex_type_xsd_element
        parent = grandparent.get_children()[1]
        child = parent.get_children()[0]
        grandchild = child.get_children()[0]

        assert grandchild.get_parent() == child
        assert child.get_parent() == parent
        assert parent.get_parent() == grandparent
        assert grandparent.get_parent() is None

    def test_get_xsd(self):
        """
        Test that each XSDTree Element has a get_xsd method which returns the xsd representation as it is given in the musicxml.xsd file.
        :return:
        """
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
        assert self.above_below_simple_type_xsd_element.get_xsd() == expected_1
        assert self.complex_type_xsd_element.get_xsd() == expected_2

    def test_get_restriction(self):
        assert self.above_below_simple_type_xsd_element.get_restriction().tag == 'restriction'
        assert self.complex_type_xsd_element.get_restriction() is None

    def test_get_union(self):
        """
        <xs:simpleType name="yes-no-number">
            <xs:annotation>
                <xs:documentation>The yes-no-number type is used for attributes that can be either boolean or numeric values.</xs:documentation>
            </xs:annotation>
            <xs:union memberTypes="yes-no xs:decimal"/>
        </xs:simpleType>
        """
        assert self.above_below_simple_type_xsd_element.get_union() is None
        assert self.yes_no_number_simple_type_xsd_element.get_union().tag == 'union'

    def test_get_union_member_types(self):
        assert self.above_below_simple_type_xsd_element.get_union_member_types() is None
        assert self.yes_no_number_simple_type_xsd_element.get_union_member_types() == ['yes-no',
                                                                                       'xs:decimal']

    def test_is_simple_type_property(self):
        """
        Test if is_simple_type returns true if xsd is a simple type element
        """
        assert self.yes_no_number_simple_type_xsd_element.is_simple_type is True
        assert self.above_below_simple_type_xsd_element.is_simple_type is True
        assert self.complex_type_xsd_element.is_simple_type is False

    def test_is_complex_type_property(self):
        """
        Test if is_complex_type returns true if xsd is a complex type element
        """
        assert self.yes_no_number_simple_type_xsd_element.is_complex_type is False
        assert self.above_below_simple_type_xsd_element.is_complex_type is False
        assert self.complex_type_xsd_element.is_complex_type is True
