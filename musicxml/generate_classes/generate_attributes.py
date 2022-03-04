from contextlib import redirect_stdout
from pathlib import Path
from string import Template
import xml.etree.ElementTree as ET

from musicxml.generate_classes.utils import get_all_et_elements
from musicxml.xsd.xsdtree import XSDTree

sources_path = Path(__file__).parent / 'musicxml_4_0.xsd'
default_path = Path(__file__).parent / 'defaults' / 'xsdattribute.py'
target_path = Path(__file__).parent.parent / 'xsd' / 'xsdattribute.py'


template_string = """
class $class_name($base_classes):
    \"\"\"
    $doc
    \"\"\"
    
    XSD_TREE = XSDTree(ET.fromstring(\"\"\"
$xsd_string
\"\"\"
                                     ))
"""

xsd_attribute_class_names = ['XSDAttribute', 'XSDAttributeGroup']


def complex_type_class_as_string(complex_type_):
    xsd_tree = XSDTree(complex_type_)
    class_name = xsd_tree.xsd_element_class_name
    xsd_attribute_class_names.append(class_name)
    base_classes = ('XSDAttributeGroup',)
    doc = xsd_tree.get_doc()
    ET.indent(complex_type_, space='    '),
    xsd_string = ET.tostring(complex_type_, encoding='unicode').strip()
    if not doc:
        doc = ""
    t = Template(template_string).substitute(class_name=class_name, base_classes=', '.join(base_classes), doc=doc, xsd_string=xsd_string)
    return t


all_attribute_group_et_elements = get_all_et_elements(sources_path, 'attributeGroup')

with open(target_path, 'w+') as f:
    with open(default_path, 'r') as default:
        with redirect_stdout(f):
            print(default.read())
    with redirect_stdout(f):
        for attribute_group in all_attribute_group_et_elements:
            print(complex_type_class_as_string(attribute_group))
        print(f'__all__={xsd_attribute_class_names}')