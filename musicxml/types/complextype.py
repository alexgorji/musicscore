from musicxml.util.helperfunctions import find_all_xsd_children, get_complex_type_all_base_classes
from musicxml.xmltree import XMLTree
from musicxml.xsdtree import XSDTree
from musicxml.types.simpletype import *


class XMLComplexType(XMLTree):
    pass


xml_complex_type_class_names = []
"""
Creating all XMLComplexType classes
"""
for complex_type in find_all_xsd_children(tag='complexType'):
    xml_element_tree_element = XSDTree(complex_type)
    class_name = xml_element_tree_element.xml_tree_class_name
    base_classes = f"({', '.join(get_complex_type_all_base_classes(xml_element_tree_element))}, )"
    attributes = """
    {
    '__doc__': xml_element_tree_element.get_doc(), 
    'XSD_TREE': xml_element_tree_element
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
    xml_complex_type_class_names.append(class_name)

__all__ = xml_complex_type_class_names
