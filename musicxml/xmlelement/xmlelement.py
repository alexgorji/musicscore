import copy
from xml.etree import ElementTree as ET
import xml.dom.minidom
from musicxml.exceptions import XMLElementValueRequiredError, XMLElementChildrenRequired
from musicxml.util.core import root1, ns, cap_first, convert_to_xsd_class_name
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdtree import XSDTree
from tree.tree import Tree


class XMLElement(Tree):
    XSD_TREE = None

    def __init__(self, value=None, **kwargs):
        self._value = None
        self._attributes = None
        self._et_xml_element = None
        self._type = None
        self.value = value
        self._set_attributes(kwargs)
        self._create_et_xml_element()
        self._children = []
        self._parent = None

    def _check_required_children(self):
        if self.type_.XSD_TREE.is_complex_type:
            if self.type_.get_xsd_indicator():
                children_names = [child.get_class_name() for child in self.get_children()]
                for element_class_name in self.type_.get_xsd_indicator().required_elements:
                    if element_class_name not in children_names:
                        raise XMLElementChildrenRequired(f"{element_class_name} is required for {self.get_class_name()}")

    def _create_et_xml_element(self):
        self._et_xml_element = ET.Element(self.name, self.attributes)
        if self.value:
            self._et_xml_element.text = str(self.value)

    def _set_attributes(self, val):
        if val is None:
            val = {}
        if self.type_.XSD_TREE.is_simple_type:
            if val:
                raise AttributeError('attributes cannot be set')
        elif not isinstance(val, dict):
            raise TypeError
        self._attributes = val

    @property
    def attributes(self):
        return self._attributes

    @property
    def name(self):
        return self.XSD_TREE.get_attributes()['name']

    @property
    def type_(self):
        if self._type is None:
            try:
                self._type = eval(convert_to_xsd_class_name(self.XSD_TREE.get_attributes()['type'], 'complex_type'))
            except NameError:
                self._type = eval(convert_to_xsd_class_name(self.XSD_TREE.get_attributes()['type'], 'simple_type'))
        return self._type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val is not None:
            self._value = self.type_(val)
            if self._et_xml_element is not None:
                self._et_xml_element.text = str(self.value)

    @classmethod
    def get_xsd(cls):
        return cls.XSD_TREE.get_xsd()

    @classmethod
    def get_class_name(cls):
        return 'XML' + ''.join([cap_first(partial) for partial in cls.XSD_TREE.name.split('-')])

    def add_child(self, element):
        if not isinstance(element, XMLElement):
            raise TypeError
        element._parent = self
        self._et_xml_element.append(element._et_xml_element)
        self._children.append(element)

    def get_children(self):
        return self._children

    def get_parent(self):
        return self._parent

    def _final_checks(self):
        if self.type_.value_is_required() and not self.value:
            raise XMLElementValueRequiredError(f"{self.get_class_name()} requires a value.")

        if self.type_.XSD_TREE.is_complex_type:
            self.type_.check_attributes(self.attributes)

        self._check_required_children()

    def to_string(self):
        self._final_checks()
        for child in self.get_children():
            child._final_checks()
        ET.indent(self._et_xml_element, space="    ", level=self.level)
        return ET.tostring(self._et_xml_element, encoding='unicode')


xsd_tree_score_partwise_part = XSDTree(root1.find(f".//{ns}element[@name='score-partwise']"))


class XMLScorePartwise(XMLElement):
    XSD_TREE = XSDTree(root1.find(f".//{ns}element[@name='score-partwise']"))

    def write(self, path):
        with open(path, 'w') as file:
            file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
            file.write(self.to_string())

    @property
    def type_(self):
        if self._type is None:
            self._type = XSDComplexTypeScorePartwise
        return self._type

    @property
    def __doc__(self):
        return self.XSD_TREE.get_doc()


class XMLPart(XMLElement):
    XSD_TREE = XSDTree(root1.findall(f".//{ns}element[@name='score-partwise']//{ns}element")[0])

    @property
    def type_(self):
        if self._type is None:
            self._type = XSDComplexTypePart
        return self._type

    @property
    def __doc__(self):
        return self.XSD_TREE.get_doc()


class XMLMeasure(XMLElement):
    XSD_TREE = XSDTree(root1.findall(f".//{ns}element[@name='score-partwise']//{ns}element")[1])

    @property
    def type_(self):
        if self._type is None:
            self._type = XSDComplexTypeMeasure
        return self._type

    @property
    def __doc__(self):
        return self.XSD_TREE.get_doc()


typed_elements = list(
    dict.fromkeys(
        [
            (node.attrib['name'], node.attrib['type']) for node in root1.iter() if node.tag == f'{ns}element' and node.attrib.get('type') is
                                                                                   not None
        ]
    )
)


def get_doc(self):
    if self.type_.XSD_TREE.is_complex_type:
        return self.type_.__doc__
    else:
        return self.XSD_TREE.get_doc()


__doc__ = property(get_doc)

xml_element_class_names = ['XMLScorePartwise', 'XMLPart', 'XMLMeasure']

for element in typed_elements:
    found_et_xml = root1.find(f".//{ns}element[@name='{element[0]}'][@type='{element[1]}']")
    copied_el = copy.deepcopy(found_et_xml)
    if copied_el.attrib.get('minOccurs'):
        copied_el.attrib.pop('minOccurs')
    if copied_el.attrib.get('maxOccurs'):
        copied_el.attrib.pop('maxOccurs')
    xsd_tree = XSDTree(copied_el)
    class_name = 'XML' + ''.join([cap_first(partial) for partial in xsd_tree.name.split('-')])
    base_classes = "(XMLElement, )"
    attributes = """
    {
    'XSD_TREE': xsd_tree,
    '__doc__': __doc__,
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
    xml_element_class_names.append(class_name)

__all__ = xml_element_class_names
