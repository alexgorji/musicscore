from unittest import TestCase
import xml.etree.ElementTree as ET

from musicxml.generate_classes.utils import musicxml_xsd_path, ns
from musicxml.xsd.xsdtree import XSDTree


class MusicXmlTestCase(TestCase):
    def setUp(self) -> None:
        with open(musicxml_xsd_path) as file:
            xmltree = ET.parse(file)
        self.root = xmltree.getroot()
        self.all_simple_type_xsd_elements = [XSDTree(simpletype) for simpletype in
                                             self.root.findall(f"{ns}simpleType")]
        self.all_complex_type_xsd_elements = [XSDTree(complextype) for complextype in
                                              self.root.findall(f"{ns}complexType")]
        self.above_below_simple_type_xsd_element = XSDTree(self.root.find(f"{ns}simpleType["
                                                                          f"@name='above-below']"))
        self.yes_no_number_simple_type_xsd_element = XSDTree(self.root.find(f"{ns}simpleType["
                                                                            f"@name='yes-no-number']"))
        self.complex_type_xsd_element = XSDTree(self.root.find(f"{ns}complexType[@name='fingering']"))
        self.attribute_group_position = XSDTree(self.root.find(f"{ns}attributeGroup[@name='position']"))
        super().setUp()
