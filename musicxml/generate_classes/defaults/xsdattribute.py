from musicxml.util.core import convert_to_xsd_class_name
from musicxml.xsd.xsdattribute import XSDAttribute
from musicxml.xsd.xsdtree import XSDTree, XSDTreeElement
from musicxml.xsd.xsdsimpletype import *
import xml.etree.ElementTree as ET


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
