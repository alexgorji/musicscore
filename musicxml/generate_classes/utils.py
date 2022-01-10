import xml.etree.ElementTree as ET
from pathlib import Path

ns = '{http://www.w3.org/2001/XMLSchema}'
xml_xsd_path = Path(__file__).parent / 'xml.xsd'
musicxml_xsd_path = Path(__file__).parent / 'musicxml_4_0.xsd'

with open(xml_xsd_path) as file:
    xml_et_tree = ET.parse(file)
with open(musicxml_xsd_path) as file:
    musicxml_et_tree = ET.parse(file)
# -------------------------------------
xml_xsd_et_root = xml_et_tree.getroot()
musicxml_xsd_et_root = musicxml_et_tree.getroot()


def get_all_et_elements(source_path, tag):
    with open(source_path) as file:
        xsd_tree = ET.parse(file)
    root = xsd_tree.getroot()
    return root.findall(f"{{*}}{tag}")


def get_simple_type_all_base_classes(xml_element_tree_element):
    base_class_names = xml_element_tree_element.xsd_tree_base_class_names
    if [name for name in base_class_names if name.startswith('XSDSimpleType')]:
        pass
    else:
        base_class_names.insert(0, 'XSDSimpleType')
    return base_class_names


def get_complex_type_all_base_classes(xsd_element_tree_element):
    base_class_names = xsd_element_tree_element.xsd_tree_base_class_names
    if [name for name in base_class_names if name.startswith('XSDComplexType')]:
        pass
    else:
        base_class_names.insert(0, 'XSDComplexType')
    return base_class_names
