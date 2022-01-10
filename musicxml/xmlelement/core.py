from typing import Optional
from xml.etree import ElementTree as ET

from musicxml.exceptions import XMLElementValueRequiredError, XMLElementChildrenRequired, XSDWrongAttribute
from musicxml.util.core import replace_key_underline_with_hyphen, convert_to_xsd_class_name
from musicxml.xmlelement.exceptions import XMLChildContainerFactoryError, XMLElementCannotHaveChildrenError
from musicxml.xmlelement.xmlchildcontainer import XMLChildContainerFactory
from musicxml.xsd.xsdtree import XSDTree
from tree.tree import Tree
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdcomplextype import *


class XMLElement(Tree):
    PROPERTIES = {'compact_repr', 'is_leaf', 'level', 'attributes', 'child_container_tree', 'et_xml_element', 'name', 'type_', 'value', }
    XSD_TREE: Optional[XSDTree] = None

    def __init__(self, value=None, **kwargs):
        self._type = None
        super().__init__()
        self._value = None
        self._attributes = {}
        self._et_xml_element = None
        self._child_container_tree = None
        self.value = value
        self._set_attributes(kwargs)

        self._create_child_container_tree()

    def _check_child_to_be_added(self, child):
        if not isinstance(child, XMLElement):
            raise TypeError

    def _create_et_xml_element(self):
        self._et_xml_element = ET.Element(self.name, {k: str(v) for k, v in self.attributes.items()})
        if self.value:
            self._et_xml_element.text = str(self.value)
        for child in self.get_children():
            self._et_xml_element.append(child.et_xml_element)

    def _final_checks(self):
        if self.type_.value_is_required() and not self.value:
            raise XMLElementValueRequiredError(f"{self.get_class_name()} requires a value.")
        if self._child_container_tree:
            required_children = self._child_container_tree.get_required_element_names()
            if required_children:
                raise XMLElementChildrenRequired(f"{self.__class__.__name__} requires at least following children: {required_children}")

        if self.type_.XSD_TREE.is_complex_type:
            self.type_.check_attributes(self.attributes)

        for child in self.get_children():
            child._final_checks()

    def _create_child_container_tree(self):
        try:
            if self.type_.XSD_TREE.is_complex_type:
                self._child_container_tree = XMLChildContainerFactory(complex_type=self.type_).get_child_container()
        except XMLChildContainerFactoryError:
            pass

    def _set_attributes(self, val):
        if not val:
            return

        if self.type_.XSD_TREE.is_simple_type:
            if val:
                raise XSDWrongAttribute(f'{self.__class__.__name__} has no attributes.')

        elif not isinstance(val, dict):
            raise TypeError

        new_attributes = replace_key_underline_with_hyphen(dict_=val)
        try:
            allowed_attributes = [attribute.name for attribute in self.type_.get_xsd_attributes()]
        except KeyError:
            raise XSDWrongAttribute(f'{self.__class__.__name__} has no attributes.')
        for new_attribute in new_attributes:
            if new_attribute not in allowed_attributes:
                raise XSDWrongAttribute(
                    f'{self.__class__.__name__} has no attribute {new_attribute}. Allowed attributes are: {allowed_attributes}')
        self._attributes = {**self._attributes, **new_attributes}

    @property
    def attributes(self):
        return self._attributes

    @property
    def child_container_tree(self):
        return self._child_container_tree

    @property
    def et_xml_element(self):
        if not self._et_xml_element:
            self._create_et_xml_element()
        return self._et_xml_element

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

    @classmethod
    def get_xsd(cls):
        return cls.XSD_TREE.get_xsd()

    @classmethod
    def get_class_name(cls):
        return cls.__name__

    def add_child(self, child: 'XMLElement', forward: int = 0) -> 'XMLElement':
        if not self._child_container_tree:
            raise XMLElementCannotHaveChildrenError()
        self._child_container_tree.add_element(child, forward)
        return child

    def get_children(self):
        if self._child_container_tree:
            return [xml_element for leaf in self._child_container_tree.iterate_leaves() for xml_element in leaf.content.xml_elements if
                    leaf.content.xml_elements]
        else:
            return []

    def to_string(self, add_separators=False) -> str:
        self._final_checks()
        self._create_et_xml_element()

        if add_separators:
            comment = ET.Comment('=========================================================')
            self.et_xml_element.insert(1, comment)
            self.et_xml_element.insert(3, comment)
        ET.indent(self.et_xml_element, space="    ", level=self.level)
        return ET.tostring(self.et_xml_element, encoding='unicode') + '\n'

    def __setattr__(self, key, value):
        if key[0] == '_' or key in self.PROPERTIES:
            super().__setattr__(key, value)
        else:
            self._set_attributes({key: value})
