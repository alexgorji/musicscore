import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from pathlib import Path
from string import Template

from musicxml.generate_classes.utils import musicxml_xsd_et_root
from musicxml.util.core import convert_to_xsd_class_name
from musicxml.xsd.xsdtree import XSDTree

default_path = Path(__file__).parent / 'defaults' / 'xsdindicator.py'
target_path = Path(__file__).parent.parent / 'xsd' / 'xsdindicator.py'

template_string = """
class $class_name($base_classes):
    \"\"\"$doc\"\"\"
    
    XSD_TREE = XSDTree(ET.fromstring(\"\"\"
$xsd_string
\"\"\"
                                     ))
"""

xsd_indicator_class_names = ['XSDSequence', 'XSDChoice', 'XSDGroup']


def group_indicator_class_as_string(group_indicator):
    xsd_tree = XSDTree(group_indicator)
    class_name = convert_to_xsd_class_name(xsd_tree.name, 'group')
    xsd_indicator_class_names.append(class_name)
    base_classes = ('XSDGroup',)
    doc = xsd_tree.get_doc()
    ET.indent(group_indicator, space='    '),
    xsd_string = ET.tostring(group_indicator, encoding='unicode').strip()
    if not doc:
        doc = ""
    t = Template(template_string).substitute(class_name=class_name, base_classes=', '.join(base_classes), doc=doc, xsd_string=xsd_string)
    return t


all_xsd_group_et_elements = musicxml_xsd_et_root.findall(f"{{*}}{'group'}")

with open(target_path, 'w+') as f:
    with open(default_path, 'r') as default:
        with redirect_stdout(f):
            print(default.read())
    with redirect_stdout(f):
        for group in all_xsd_group_et_elements:
            print(group_indicator_class_as_string(group))
        print(f'__all__={xsd_indicator_class_names}')
