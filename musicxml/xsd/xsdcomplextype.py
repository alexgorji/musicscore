from musicxml.util.core import find_all_xsd_children, get_complex_type_all_base_classes, convert_to_xsd_class_name
from musicxml.xsd.xsdattribute import XSDAttribute
from musicxml.xsd.xsdtree import XSDTree, XSDElement
from musicxml.exceptions import XSDAttributeRequiredException, XSDWrongAttribute
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdattribute import *


class XSDComplexType(XSDElement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def check_attributes(cls, val_dict):
        required_attributes = [attribute for attribute in cls.get_xsd_attributes() if attribute.is_required]
        for required_attribute in required_attributes:
            if required_attribute.name not in val_dict:
                raise XSDAttributeRequiredException

        for key in val_dict:
            if key not in [attribute.name for attribute in cls.get_xsd_attributes()]:
                raise XSDWrongAttribute
            attribute = [attribute for attribute in cls.get_xsd_attributes() if attribute.name == key][0]
            attribute(val_dict[key])

    @classmethod
    def get_xsd_attributes(cls):
        output = []
        if cls.XSD_TREE.get_simple_content_extension():
            for child in cls.XSD_TREE.get_simple_content_extension().get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
        elif cls.XSD_TREE.get_complex_content():
            complex_content_extension = cls.XSD_TREE.get_complex_content_extension()
            complex_type_extension_base_class_name = convert_to_xsd_class_name(complex_content_extension.get_attributes()['base'],
                                                                               'complex_type')
            extension_base = eval(complex_type_extension_base_class_name)
            output.extend(extension_base.get_xsd_attributes())
            for child in complex_content_extension.get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
            return output
        else:
            for child in cls.XSD_TREE.get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
        return output

    @classmethod
    def get_xsd_indicator(cls):
        return cls.XSD_TREE.get_xsd_indicator()


xsd_complex_type_class_names = []

"""
Creating all XSDComplexType classes
"""
for complex_type in find_all_xsd_children(tag='complexType'):
    xsd_tree = XSDTree(complex_type)
    class_name = xsd_tree.xsd_element_class_name
    base_classes = f"({', '.join(get_complex_type_all_base_classes(xsd_tree))}, )"
    attributes = """
    {
    '__doc__': xsd_tree.get_doc(), 
    'XSD_TREE': xsd_tree
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
    xsd_complex_type_class_names.append(class_name)

__all__ = xsd_complex_type_class_names
