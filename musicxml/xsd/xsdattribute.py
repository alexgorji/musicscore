from musicxml.util.core import convert_to_xsd_class_name, find_all_xsd_children
from musicxml.xsd.xsdtree import XSDTree, XSDElement
from musicxml.xsd.xsdsimpletype import *


class XSDAttribute:
    def __init__(self, xsd_tree):
        self._xsd_tree = None
        self.xsd_tree = xsd_tree
        self._name = None
        self._type = None
        self._is_required = None

    @property
    def xsd_tree(self):
        return self._xsd_tree

    @xsd_tree.setter
    def xsd_tree(self, value):
        if not isinstance(value, XSDTree):
            raise TypeError
        if value.tag != 'attribute':
            raise ValueError
        self._xsd_tree = value

    @property
    def name(self):
        if self._name is None:
            self._name = self.xsd_tree.get_attributes()['name']
        return self._name

    @property
    def type_(self):
        if self._type is None:
            self._type = eval(convert_to_xsd_class_name(self.xsd_tree.get_attributes()['type'], 'simple_type'))
        return self._type

    @property
    def is_required(self):
        if self._is_required is None:
            if self.xsd_tree.get_attributes().get('use') == 'required':
                self._is_required = True
            else:
                self._is_required = False
        return self._is_required

    def __call__(self, value):
        return self.type_(value)

    def __str__(self):
        attrs = self.xsd_tree.get_attributes()
        return f"XSDAttribute{''.join([f'@{attribute}={self.xsd_tree.get_attributes()[attribute]}' for attribute in attrs])}"

    def __repr__(self):
        return self.__str__()


class XSDAttributeGroup(XSDElement):

    @classmethod
    def get_xsd_attributes(cls):
        output = []
        for child in cls.XSD_TREE.get_children():
            if child.tag == 'attribute':
                output.append(XSDAttribute(child))
            if child.tag == 'attributeGroup':
                output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
        return output


"""
Creating all XSDAttributeGroup classes
"""
xml_attribute_group_class_names = []
for attribute_group in find_all_xsd_children(tag='attributeGroup', root='1'):
    xsd_tree = XSDTree(attribute_group)
    class_name = xsd_tree.xsd_element_class_name
    base_classes = "(XSDAttributeGroup, )"
    attributes = """
    {
    '__doc__': xsd_tree.get_doc(), 
    'XSD_TREE': xsd_tree
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
    xml_attribute_group_class_names.append(class_name)

__all__ = xml_attribute_group_class_names
