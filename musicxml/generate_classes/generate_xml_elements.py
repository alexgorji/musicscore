import copy
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from pathlib import Path
from string import Template

from musicxml.generate_classes.utils import musicxml_xsd_et_root, ns
from musicxml.util.core import convert_to_xml_class_name, convert_to_xsd_class_name
from musicxml.xsd.xsdtree import XSDTree
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdcomplextype import __all__ as all_complex_types
from musicxml.xsd.xsdsimpletype import *

default_path = Path(__file__).parent / 'defaults' / 'xmlelement.py'
target_path = Path(__file__).parent.parent / 'xmlelement' / 'xmlelement.py'

template_string = """
class $class_name($base_classes):
    
    TYPE = $xsd_type
    XSD_TREE = XSDTree(ET.fromstring(\"\"\"
$xsd_string
\"\"\"
                                     ))

    @property
    def __doc__(self):
        if self.TYPE.XSD_TREE.is_complex_type:
            return self.TYPE.__doc__
        else:
            return self.XSD_TREE.get_doc()
"""

typed_elements = list(
    dict.fromkeys(
        [
            (node.attrib['name'], node.attrib['type']) for node in musicxml_xsd_et_root.iter() if node.tag == f'{ns}element' and
                                                                                                  node.attrib.get('type') is not None
        ]
    )
)

xml_element_class_names = ['XMLScorePartwise', 'XMLPart', 'XMLMeasure', 'XMLDirective']


def element_class_as_string(element_):
    found_et_xml = musicxml_xsd_et_root.find(f".//{{*}}element[@name='{element_[0]}'][@type='{element_[1]}']")
    copied_el = copy.deepcopy(found_et_xml)
    if copied_el.attrib.get('minOccurs'):
        copied_el.attrib.pop('minOccurs')
    if copied_el.attrib.get('maxOccurs'):
        copied_el.attrib.pop('maxOccurs')
    xsd_tree = XSDTree(copied_el)
    class_name = convert_to_xml_class_name(xsd_tree.name)
    xml_element_class_names.append(class_name)
    try:
        xsd_type = convert_to_xsd_class_name(xsd_tree.get_attributes()['type'], 'complex_type')
        assert xsd_type in all_complex_types
    except (ValueError, AssertionError):
        xsd_type = convert_to_xsd_class_name(xsd_tree.get_attributes()['type'], 'simple_type')
    base_classes = ('XMLElement',)
    ET.indent(found_et_xml, space='    '),
    xsd_string = ET.tostring(found_et_xml, encoding='unicode').strip()
    t = Template(template_string).substitute(class_name=class_name, base_classes=', '.join(base_classes), xsd_type=xsd_type,
                                             xsd_string=xsd_string)
    return t


with open(target_path, 'w+') as f:
    with open(default_path, 'r') as default:
        with redirect_stdout(f):
            print(default.read())
    with redirect_stdout(f):
        for element in typed_elements:
            print(element_class_as_string(element))
        print(f'__all__={xml_element_class_names}')
