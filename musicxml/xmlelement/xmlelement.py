from xml.etree import ElementTree as ET

from musicxml.exceptions import XMLElementValueRequiredError
from musicxml.util.core import root1, ns, cap_first, convert_to_xsd_class_name
from musicxml.xsd.xsdtree import XSDSequence, XSDTree
from tree.tree import Tree
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdcomplextype import *


# class XMLElement(Tree):
#
#     def __init__(self, type_, name=None, value=None, attributes=None, doc=None):
#         """
#         :param type_: XSDComplexType or XSDSimpleType required
#         :param value: None if empty, otherwise depends on type_.
#         :param attributes: dict can only be set during initialization.
#         """
#         self._type = None
#         self._name = None
#         self._value = None
#         self._attributes = None
#         self._xml_element = None
#         self._set_type(type_)
#         self._set_name(name)
#         self.value = value
#         self._set_attributes(attributes)
#         self.doc = doc
#
#         self._create_xml_element()
#         self._children = []
#         self._parent = None
#
#     def _create_xml_element(self):
#         self._xml_element = ET.Element(self.type_.XSD_TREE.name, self.attributes)
#         if self.value:
#             self._xml_element.text = str(self.value)
#
#     def _order_children(self):
#         if self.type_.XSD_TREE.is_complex_type:
#             if isinstance(self.type_.get_xsd_indicator(), XSDSequence):
#                 raise NotImplementedError
#             else:
#                 pass
#         else:
#             pass
#
#     def _set_attributes(self, val):
#         if val is None:
#             self._attributes = {}
#         elif not isinstance(val, dict):
#             raise TypeError
#         else:
#             self.type_.check_attributes(val)
#             self._attributes = val
#
#     def _set_name(self, val):
#         if self._type.XSD_TREE.is_complex_type:
#             if val:
#                 raise ValueError('name cannot be set for elements with complex type.')
#             else:
#                 self._name = self.type_.XSD_TREE.name
#         elif self._type.XSD_TREE.is_simple_type:
#             if not val:
#                 raise ValueError('name must be set for elements with simple type while initializing.')
#             else:
#                 self._name = val
#         else:
#             raise TypeError
#
#     def _set_type(self, val):
#         try:
#             if val.XSD_TREE.is_complex_type or val.XSD_TREE.is_simple_type:
#                 self._type = val
#             else:
#                 raise TypeError
#         except AttributeError:
#             raise TypeError
#
#     @property
#     def attributes(self):
#         return self._attributes
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def type_(self):
#         return self._type
#
#     @property
#     def value(self):
#         return self._value
#
#     @value.setter
#     def value(self, val):
#         if val is not None:
#             self._value = self.type_(val)
#             if self._xml_element is not None:
#                 self._xml_element.text = str(self.value)
#
#     def check_children(self):
#         self._order_children()
#
#     def to_string(self):
#         if self.type_.XSD_TREE.is_simple_type and not self.value:
#             raise XMLElementValueRequiredError
#         self.check_children()
#         return ET.tostring(self._xml_element, encoding='unicode')
#
#     def get_children(self):
#         return self._children
#
#     def get_parent(self):
#         return self._parent
#
#     @property
#     def __doc__(self):
#         if self.type_.XSD_TREE.is_simple_type:
#             if not self.doc:
#                 raise ValueError('attribute doc of an element with simple type must be set')
#             else:
#                 return self.doc
#         elif self.type_.XSD_TREE.is_complex_type:
#             if self.doc:
#                 raise ValueError('attribute doc of an element with complext type cannot be set')
#             else:
#                 return self.type_.__doc__
#         else:
#             raise TypeError

class XMLElement:
    XSD_TREE = None

    def __init__(self, value=None, **kwargs):
        self._value = None
        self._attributes = None
        self._et_xml_element = None
        self.value = value
        self._set_attributes(kwargs)
        self._create_et_xml_element()

    def _create_et_xml_element(self):
        self._et_xml_element = ET.Element(self.type_.XSD_TREE.name, self.attributes)
        self._et_xml_element.tag = self.name
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
        try:
            return eval(convert_to_xsd_class_name(self.XSD_TREE.get_attributes()['type'], 'complex_type'))
        except NameError:
            return eval(convert_to_xsd_class_name(self.XSD_TREE.get_attributes()['type'], 'simple_type'))

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

    def to_string(self):
        if self.type_.value_is_required() and not self.value:
            raise XMLElementValueRequiredError
        if self.type_.XSD_TREE.is_complex_type:
            self.type_.check_attributes(self.attributes)
        return ET.tostring(self._et_xml_element, encoding='unicode')


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

xml_element_class_names = []
for element in typed_elements:
    found_et_xml = root1.find(f".//{ns}element[@name='{element[0]}'][@type='{element[1]}']")
    if found_et_xml.attrib.get('minOccurs'):
        found_et_xml.attrib.pop('minOccurs')
    if found_et_xml.attrib.get('maxOccurs'):
        found_et_xml.attrib.pop('maxOccurs')
    xsd_tree = XSDTree(found_et_xml)
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
