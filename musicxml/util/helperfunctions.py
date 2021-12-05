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


def check_value_type(value, types):
    if isinstance(types, str):
        raise TypeError
    if types == str or not hasattr(types, '__iter__'):
        raise TypeError

    if True in [isinstance(value, type_) for type_ in types]:
        pass
    else:
        raise TypeError(f"value {value} can only be of types {[type_.__name__ for type_ in types]} "
                        f"not {type(value).__name__}.")


def get_cleaned_token(string_value):
    output = ' '.join(partial.strip() for partial in string_value.split('\n'))
    output = ' '.join(partial.strip() for partial in output.split('\t'))
    output = ' '.join(partial.strip() for partial in output.split('\r'))
    output = ' '.join([partial.strip() for partial in output.split(' ') if partial != ''])
    return output
