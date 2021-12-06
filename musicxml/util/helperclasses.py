from pathlib import Path
from unittest import TestCase
import xml.etree.ElementTree as ET

from musicxml.xsdtree import XSDTree

xsd_path = Path(__file__).parent.parent / 'musicxml_4_0.xsd'


class MusicXmlTestCase(TestCase):
    def setUp(self) -> None:
        with open(xsd_path) as file:
            xmltree = ET.parse(file)
        self.root = xmltree.getroot()
        ns = '{http://www.w3.org/2001/XMLSchema}'
        self.all_simple_type_elements = [XSDTree(simpletype) for simpletype in
                                         self.root.findall(f"{ns}simpleType")]
        self.above_below_simple_type_element = XSDTree(self.root.find(f"{ns}simpleType["
                                                                                    f"@name='above-below']"))
        self.yes_no_number_simple_type_element = XSDTree(self.root.find(f"{ns}simpleType["
        f"@name='yes-no-number']"))
        self.complex_type_element = XSDTree(self.root.find(f"{ns}complexType[@name='fingering']"))
        super().setUp()
