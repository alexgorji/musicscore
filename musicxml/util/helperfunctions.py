from pathlib import Path

import xml.etree.ElementTree as ET

xsd_path = Path(__file__).parent.parent / 'musicxml_4_0.xsd'
with open(xsd_path) as file:
    xsd_tree = ET.parse(file)
ns = '{http://www.w3.org/2001/XMLSchema}'
root = xsd_tree.getroot()


def get_simple_format_all_base_classes(xml_element_tree_element):
    base_class_names = xml_element_tree_element.base_class_names
    if [name for name in base_class_names if name.startswith('XMLSimpleType')]:
        pass
    else:
        base_class_names.insert(0, 'XMLSimpleType')
    return base_class_names


def cap_first(s):
    return s[0].upper() + s[1:]


def find_all_xsd_children(tag):
    return root.findall(f"{ns}{tag}")
