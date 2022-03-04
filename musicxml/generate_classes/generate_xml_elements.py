import copy
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from pathlib import Path
from string import Template

from musicxml.generate_classes.utils import musicxml_xsd_et_root, ns
from musicxml.util.core import convert_to_xml_class_name, convert_to_xsd_class_name
from musicxml.xmlelement.containers import containers
from musicxml.xsd.xsdtree import XSDTree
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdcomplextype import __all__ as all_complex_types
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdsimpletype import __all__ as all_simple_types

default_path = Path(__file__).parent / 'defaults' / 'xmlelement.py'
target_path = Path(__file__).parent.parent / 'xmlelement' / 'xmlelement.py'

template_string = """
class $class_name($base_classes):
    \"\"\"
    $doc
    \"\"\"
    
    TYPE = $xsd_type
    _SEARCH_FOR_ELEMENT = "$search_for"
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
    def get_doc():
        def get_attributes_doc():
            output = ""
            try:
                possible_attributes = eval(xsd_type).get_xsd_attributes()
                string_possible_attributes = []
                for att in possible_attributes:
                    repr_ = ''
                    if att.name:
                        repr_ += f"``{'_'.join(att.name.split('-'))}``"
                    if att.type_:
                        try:
                            repr_ += f"\@ :obj:`~musicxml.xsd.xsdsimpletype.{att.type_.__name__}`"
                        except AttributeError:
                            breakpoint()
                            pass
                    if att.is_required:
                        repr_ += '\@required'

                    if repr_ != '':
                        string_possible_attributes.append(repr_)

                if string_possible_attributes:
                    output += '    ``Possible attributes``: '
                    output += f"{', '.join(sorted(string_possible_attributes))}"

            except (AttributeError, KeyError, NameError):
                pass
            return output

        def get_possible_children(container):
            possible_children = ", ".join(sorted(set(f":obj:`~{convert_to_xml_class_name(l.content.name)}`" for l in
                                                     container.iterate_leaves())))

            output = '    ``Possible children``:'
            output += f"    {possible_children}"
            return output

        output = xsd_tree.get_doc()
        if xsd_type in all_complex_types:
            complex_type_doc = eval(xsd_type).__doc__

            if complex_type_doc:
                if complex_type_doc and output and output != "":
                    output += '\n'
                    output += '\n'
                output += '``complexType``: '
                output += complex_type_doc
                if output.count('\n') > 1:
                    output = output.replace('\n', '\n    ')
                if get_attributes_doc() != '':
                    output += '\n'
                    output += '\n'
                    output += get_attributes_doc()
                try:
                    container = containers[xsd_type]
                    container_tree_representation = copy.copy(container).tree_representation(tab=lambda x: (x.level * '    ') + '       ')
                    container_tree_representation = container_tree_representation[:-1]
                    if output != "":
                        output += '\n'
                        output += '\n'

                    output += get_possible_children(container)

                    output += '\n'
                    output += '\n'
                    output += "    ``XSD structure:``\n"
                    output += '\n'
                    output += "    .. code-block::\n"
                    output += '\n'
                    output += container_tree_representation

                except KeyError:
                    pass
        elif xsd_type in all_simple_types:
            simple_type_doc = eval(xsd_type).__doc__
            if simple_type_doc:
                if simple_type_doc and output and output != "":
                    output += '\n'
                    output += '\n'
                output += '``simpleType``: '
                output += simple_type_doc
                if output.count('\n') > 1:
                    output = output.replace('\n', '\n    ')
        else:
            pass
        if output is None:
            output = ""
        return output

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
    search_for = f".//{{*}}element[@name='{element_[0]}'][@type='{element_[1]}']"

    t = Template(template_string).substitute(class_name=class_name, base_classes=', '.join(base_classes), xsd_type=xsd_type,
                                             search_for=search_for, doc=get_doc())
    return t


with open(target_path, 'w+') as f:
    with open(default_path, 'r') as default:
        with redirect_stdout(f):
            print(default.read())
    with redirect_stdout(f):
        for element in typed_elements:
            print(element_class_as_string(element))
        print(f'__all__={xml_element_class_names}')
