from pathlib import Path

import xml.etree.ElementTree as ET

xsd_path = Path(__file__).parent.parent / 'musicxml_4_0.xsd'
with open(xsd_path) as file:
    xsd_tree = ET.parse(file)

ns = '{http://www.w3.org/2001/XMLSchema}'
root1 = xsd_tree.getroot()



xsd_path = Path(__file__).parent.parent / 'xml.xsd'
with open(xsd_path) as file:
    xsd_tree = ET.parse(file)

root2 = xsd_tree.getroot()


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


def cap_first(s):
    return s[0].upper() + s[1:]


def find_all_xsd_children(tag, root=None):
    if not root:
        root = '1'
    if root == '1':
        return root1.findall(f"{ns}{tag}")
    elif root == '2':
        return root2.findall(f"{ns}{tag}")
    else:
        raise ValueError


def get_cleaned_token(string_value):
    output = ' '.join(partial.strip() for partial in string_value.split('\n'))
    output = ' '.join(partial.strip() for partial in output.split('\t'))
    output = ' '.join(partial.strip() for partial in output.split('\r'))
    output = ' '.join([partial.strip() for partial in output.split(' ') if partial != ''])
    return output


def convert_to_xsd_class_name(name, type_='simple_type'):
    try:
        name = name.split(':')[1]
    except IndexError:
        pass
    name = cap_first(name)
    name = ''.join([cap_first(partial) for partial in name.split('-')])
    if type_ == 'simple_type':
        name = 'XSDSimpleType' + name
    elif type_ == 'complex_type':
        name = 'XSDComplexType' + name
    else:
        raise ValueError
    return name