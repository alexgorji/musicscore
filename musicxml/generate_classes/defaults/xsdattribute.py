from musicxml.util.core import convert_to_xsd_class_name
from musicxml.xsd.xsdtree import XSDTree, XSDTreeElement
from musicxml.xsd.xsdsimpletype import *
import xml.etree.ElementTree as ET

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


class XSDAttributeGroup(XSDTreeElement):

    @classmethod
    def get_xsd_attributes(cls):
        output = []
        for child in cls.XSD_TREE.get_children():
            if child.tag == 'attribute':
                output.append(XSDAttribute(child))
            if child.tag == 'attributeGroup':
                output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
        return output

# -----------------------------------------------------
# AUTOMATICALLY GENERATED WITH generate_attributes.py
# -----------------------------------------------------
