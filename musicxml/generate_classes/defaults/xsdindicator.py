from musicxml.util.core import cap_first, convert_to_xml_class_name
from musicxml.xsd.xsdtree import XSDTree, XSDTreeElement
import xml.etree.ElementTree as ET

class XSDSequence:
    def __init__(self, xsd_tree):
        self._xsd_tree = None
        self._elements = None
        self.xsd_tree = xsd_tree

    @property
    def elements(self):
        if not self._elements:
            self._elements = []
            for child in self.xsd_tree.get_children():
                if child.tag == 'element':
                    element = convert_to_xml_class_name(child.name)
                    min_occurrence = child.get_attributes().get('minOccurs')
                    if min_occurrence is None: min_occurrence = '1'
                    max_occurrence = child.get_attributes().get('maxOccurs')
                    if max_occurrence is None: max_occurrence = '1'
                    self._elements.append((element, min_occurrence, max_occurrence))

                elif child.tag == 'group':
                    xsd_group_name = 'XSDGroup' + ''.join([cap_first(partial) for partial in child.get_attributes()['ref'].split('-')])
                    elements = eval(xsd_group_name)().sequence.elements
                    min_occurrence = child.get_attributes().get('minOccurs')
                    max_occurrence = child.get_attributes().get('maxOccurs')
                    if min_occurrence is not None:
                        if len(elements) > 1:
                            raise NotImplementedError
                        list_el = list(elements[0])
                        list_el[1] = min_occurrence
                        elements[0] = tuple(list_el)
                    if max_occurrence is not None:
                        if len(elements) > 1:
                            raise NotImplementedError
                        list_el = list(elements[0])
                        list_el[2] = max_occurrence
                        elements[0] = tuple(list_el)
                    self._elements.extend(elements)
                else:
                    raise NotImplementedError(child.tag)
        return self._elements

    @property
    def xsd_tree(self):
        return self._xsd_tree

    @xsd_tree.setter
    def xsd_tree(self, value):
        if not isinstance(value, XSDTree):
            raise TypeError
        if value.tag != 'sequence':
            raise ValueError
        self._xsd_tree = value


class XSDChoice:
    def __init__(self, xsd_tree):
        self._xsd_tree = None
        self.xsd_tree = xsd_tree

    @property
    def xsd_tree(self):
        return self._xsd_tree

    @xsd_tree.setter
    def xsd_tree(self, value):
        if not isinstance(value, XSDTree):
            raise TypeError
        if value.tag != 'choice':
            raise ValueError
        self._xsd_tree = value


class XSDGroup(XSDTreeElement):

    def __init__(self):
        self._sequence = None
        self._name = None

    @property
    def name(self):
        return self.XSD_TREE.name

    @property
    def sequence(self):
        if not self._sequence:
            for child in self.XSD_TREE.get_children():
                if child.tag == 'sequence':
                    self._sequence = XSDSequence(child)
        return self._sequence

# -----------------------------------------------------
# AUTOMATICALLY GENERATED WITH generate_indicators.py
# -----------------------------------------------------
