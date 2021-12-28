from musicxml.util.core import find_all_xsd_children, get_complex_type_all_base_classes
from musicxml.xsdattribute import XSDAttribute
from musicxml.xsdtree import XSDTree, XSDElement
from musicxml.exceptions import XSDAttributeRequiredException, XSDWrongAttribute
from musicxml.types.simpletype import *
from musicxml.xsdattribute import *


class XSDComplexType(XSDElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #     self._attributes = self.XSD_TREE.get_attributes()
    #
    # def _check_attributes(self, val_dict):
    #     required_attributes = [attribute for attribute in self.get_xsd_attributes() if attribute.is_required]
    #     for required_attribute in required_attributes:
    #         if required_attribute.name not in val_dict:
    #             raise XSDAttributeRequiredException
    #
    #     for key in val_dict:
    #         if key not in [attribute.name for attribute in self.get_xsd_attributes()]:
    #             raise XSDWrongAttribute
    #
    @classmethod
    def get_xsd_attributes(cls):
        output = []
        if cls.XSD_TREE.get_simple_content_extension():
            for child in cls.XSD_TREE.get_simple_content_extension().get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_attributes())
        elif cls.XSD_TREE.get_complex_content():
            raise NotImplementedError
        else:
            for child in cls.XSD_TREE.get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_attributes())
        return output


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
