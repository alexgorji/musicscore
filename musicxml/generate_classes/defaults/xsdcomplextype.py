from musicxml.generate_classes.utils import musicxml_xsd_et_root
from musicxml.util.core import convert_to_xsd_class_name
from musicxml.exceptions import XSDAttributeRequiredException, XSDWrongAttribute
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdattribute import *
from musicxml.xsd.xsdindicator import *
from musicxml.xsd.xsdtree import XSDTreeElement, XSDTree
import xml.etree.ElementTree as ET


class XSDComplexType(XSDTreeElement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xsd_indicator = None

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
        def get_occurrences(ch):
            min_ = ch.get_attributes().get('minOccurs')
            max_ = ch.get_attributes().get('maxOccurs')
            return 1 if not min_ else int(min_), 1 if not max_ else 'unbounded' if max_ == 'unbounded' else int(max_)

        for child in cls.XSD_TREE.get_children():
            if child.tag == 'sequence':
                return XSDSequence(child), *get_occurrences(child)
            if child.tag == 'choice':
                return XSDChoice(child), *get_occurrences(child)
            if child.tag == 'group':
                return eval(convert_to_xsd_class_name(child.get_attributes()['ref'], 'group'))(), *get_occurrences(child)
            if child.tag == 'complexContent':
                return eval(convert_to_xsd_class_name(child.get_children()[0].get_attributes()['base'],
                                                      'complex_type')).get_xsd_indicator()

    @classmethod
    def value_is_required(cls):
        if cls.XSD_TREE.get_simple_content():
            return True
        else:
            return False


xsd_tree_score_partwise = XSDTree(musicxml_xsd_et_root.find(".//{*}element[@name='score-partwise']"))


class XSDComplexTypeScorePartwise(XSDComplexType):
    XSD_TREE = XSDTree(musicxml_xsd_et_root.findall(".//{*}element[@name='score-partwise']//{*}complexType")[0])


class XSDComplexTypePart(XSDComplexType):
    XSD_TREE = XSDTree(musicxml_xsd_et_root.findall(".//{*}element[@name='score-partwise']//{*}complexType")[1])


class XSDComplexTypeMeasure(XSDComplexType):
    XSD_TREE = XSDTree(musicxml_xsd_et_root.findall(".//{*}element[@name='score-partwise']//{*}complexType")[2])


class XSDComplexTypeDirective(XSDComplexType, XSDSimpleTypeString):
    XSD_TREE = XSDTree(musicxml_xsd_et_root.find(".//{*}complexType[@name='attributes']//{*}complexType"))

# -----------------------------------------------------
# AUTOMATICALLY GENERATED WITH generate_complex_types.py
# -----------------------------------------------------
