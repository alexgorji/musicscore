from musicxml.util.helperfunctions import find_all_xsd_children, get_complex_type_all_base_classes
from musicxml.xsdtree import XSDTree, XSDElement
from musicxml.types.simpletype import *


class XSDComplexType(XSDElement):
    pass


xsd_complex_type_class_names = []
"""
Creating all XSDComplexType classes
"""
for complex_type in find_all_xsd_children(tag='complexType'):
    xsd_element_tree_element = XSDTree(complex_type)
    class_name = xsd_element_tree_element.xsd_tree_class_name
    base_classes = f"({', '.join(get_complex_type_all_base_classes(xsd_element_tree_element))}, )"
    attributes = """
    {
    '__doc__': xsd_element_tree_element.get_doc(), 
    'XSD_TREE': xsd_element_tree_element
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
    xsd_complex_type_class_names.append(class_name)

__all__ = xsd_complex_type_class_names
