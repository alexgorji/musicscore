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

typed_elements = set(
    (node.attrib['name'], node.attrib['type']) for node in musicxml_xsd_et_root.iter() if node.tag == f'{ns}element' and
    node.attrib.get('type') is not None
)
typed_elements.add(('score-partwise', 'score-partwise'))
typed_elements.add(('part', 'part'))
typed_elements.add(('measure', 'measure'))
typed_elements.add(('directive', 'directive'))

typed_elements = sorted(typed_elements)


def generate_child_parent_dict() -> dict:
    """
    :return: a dictionary with name of a child XMLElement as key assiciated with a tuple of possible XMLElement parent names.

    >>> child_parent_dict = generate_child_parent_dict()
    >>> child_parent_dict['XMLStaccato']
    {'XMLArticulations'}
    """
    output = {}
    for name, type_ in typed_elements:
        try:
            class_name = convert_to_xml_class_name(name)
            type_name = convert_to_xsd_class_name(type_, type_='complex_type')
            container = containers[type_name]
            elements = sorted(set(convert_to_xml_class_name(l.content.name) for l in container.iterate_leaves()))
            for el in elements:
                if output.get(el):
                    output[el].add(class_name)
                else:
                    output[el] = {class_name}
        except (KeyError, ValueError):
            pass
    return output


child_parent_dict = generate_child_parent_dict()

extra_classes = {
    'score-partwise':
        {'search_for': ".//{*}element[@name='score-partwise']",
         'xsd_type': 'XSDComplexTypeScorePartwise',
         },
    'part':
        {'search_for': ".//{*}element[@name='score-partwise']//{*}element[@name='part']",
         'xsd_type': 'XSDComplexTypePart'
         },
    'measure':
        {'search_for': ".//{*}element[@name='score-partwise']//{*}element[@name='measure']",
         'xsd_type': 'XSDComplexTypeMeasure'
         },
    'directive':
        {'search_for': ".//{*}complexType[@name='attributes']//{*}element[@name='directive']",
         'xsd_type': 'XSDComplexTypeDirective'

         }
}

xml_element_class_names = ['XMLSenzaMisura']


def element_class_as_string(element_name_type):
    def get_doc():
        def get_external_doc_link():

            return f"`external documentation <https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/{element_name_type[0]}/>`_"

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

        def get_possible_parents():
            parent_names = child_parent_dict.get(class_name)
            if parent_names is None:
                return """
    .. todo::         
       Possible parents
"""
            possible_parents = ", ".join(sorted(set(f":obj:`~{parent_name}`" for parent_name in parent_names)))
            output = "``Possible parents``:"
            output += f"{possible_parents}"
            return output

        def get_possible_children(container):
            possible_children = ", ".join(sorted(set(f":obj:`~{convert_to_xml_class_name(l.content.name)}`" for l in
                                                     container.iterate_leaves())))

            output = '    ``Possible children``:'
            output += f"    {possible_children}"
            return output

        output = get_external_doc_link()
        if xsd_tree.get_doc():
            output += '\n'
            output += '\n'
            output += xsd_tree.get_doc()
        output += '\n'
        output += '\n'
        if xsd_type in all_complex_types:
            complex_type_doc = eval(xsd_type).__doc__

            if complex_type_doc:
                if complex_type_doc:
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
        if element_name_type[0] != 'score-partwise':
            output += '\n'
            output += '\n'
            output += get_possible_parents()
        return output

    search_for = extra_classes[element_name_type[0]]['search_for'] if extra_classes.get(
        element_name_type[0]) else f".//{{*}}element[@name='{element_name_type[0]}'][@type='{element_name_type[1]}']"

    found_et_xml = musicxml_xsd_et_root.find(search_for)
    copied_el = copy.deepcopy(found_et_xml)
    if copied_el.attrib.get('minOccurs'):
        copied_el.attrib.pop('minOccurs')
    if copied_el.attrib.get('maxOccurs'):
        copied_el.attrib.pop('maxOccurs')
    xsd_tree = XSDTree(copied_el)
    class_name = convert_to_xml_class_name(xsd_tree.name)
    xml_element_class_names.append(class_name)

    xsd_type = extra_classes[element_name_type[0]]['xsd_type'] if extra_classes.get(element_name_type[0]) else None
    if not xsd_type:
        try:
            xsd_type = convert_to_xsd_class_name(xsd_tree.get_attributes()['type'], 'complex_type')
            if xsd_type not in all_complex_types:
                raise ValueError
        except ValueError:
            xsd_type = convert_to_xsd_class_name(xsd_tree.get_attributes()['type'], 'simple_type')
    base_classes = ('XMLElement',)

    t = Template(template_string).substitute(class_name=class_name, base_classes=', '.join(base_classes), xsd_type=xsd_type,
                                             search_for=search_for, doc=get_doc())
    if element_name_type[0] == 'score-partwise':
        t += '\n'
        t += """    def write(self, path: 'pathlib.Path', intelligent_choice: bool=False) -> None:
        \"\"\"
        :param path: Output xml file path, required.
        :param intelligent_choice: Set to True if you wish to use intelligent choice in final checks to be able to change the attachment 
                                   order of XMLElement children in self.child_container_tree if an Exception was thrown and other choices 
                                   can still be checked. (No GUARANTEE!)
        :return: None
        \"\"\"
        with open(path, 'w') as file:
            file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\\n')
            file.write(self.to_string(intelligent_choice=intelligent_choice))
"""
    return t


typed_elements.remove(('senza-misura', 'xs:string'))

with open(target_path, 'w+') as f:
    with open(default_path, 'r') as default:
        with redirect_stdout(f):
            print(default.read())
    with redirect_stdout(f):
        for element_name_type in typed_elements:
            print(element_class_as_string(element_name_type))
        print(f'__all__={xml_element_class_names}')
