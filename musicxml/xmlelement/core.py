from typing import Optional
from xml.etree import ElementTree as ET

from musicxml.exceptions import XMLElementValueRequiredError, XMLElementChildrenRequired, XSDWrongAttribute, XSDAttributeRequiredException
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

    def _check_attribute(self, name, value):
        allowed_attributes = [attribute.name for attribute in self.type_.get_xsd_attributes()]
        if name not in [attribute.name for attribute in self.type_.get_xsd_attributes()]:
            raise XSDWrongAttribute(f"{self.__class__.__name__} has no attribute {name}. Allowed attributes are: {allowed_attributes}")

        attribute = [attribute for attribute in self.type_.get_xsd_attributes() if attribute.name == name][0]
        attribute(value)

    def _check_child_to_be_added(self, child):
        if not isinstance(child, XMLElement):
            raise TypeError

    def _create_et_xml_element(self):
        self._et_xml_element = ET.Element(self.name, {k: str(v) for k, v in self.attributes.items()})
        if self.value:
            self._et_xml_element.text = str(self.value)
        for child in self.get_children():
            self._et_xml_element.append(child.et_xml_element)

    def _check_required_attributes(self):
        if self.type_.XSD_TREE.is_complex_type:
            required_attributes = [attribute for attribute in self.type_.get_xsd_attributes() if attribute.is_required]
            for required_attribute in required_attributes:
                if required_attribute.name not in self.attributes:
                    raise XSDAttributeRequiredException(f"{self.__class__.__name__} requires attribute: {required_attribute.name}")

    def _final_checks(self, intelligent_choice=False):
        if self.type_.value_is_required() and not self.value:
            raise XMLElementValueRequiredError(f"{self.get_class_name()} requires a value.")
        if self._child_container_tree:
            required_children = self._child_container_tree.get_required_element_names(intelligent_choice=intelligent_choice)
            if required_children:
                raise XMLElementChildrenRequired(f"{self.__class__.__name__} requires at least following children: {required_children}")

        self._check_required_attributes()

        for child in self.get_children():
            child._final_checks(intelligent_choice=intelligent_choice)

    def _create_child_container_tree(self):
        try:
            if self.type_.XSD_TREE.is_complex_type:
                self._child_container_tree = XMLChildContainerFactory(complex_type=self.type_).get_child_container()
                self._child_container_tree._parent_element = self
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
        for key in new_attributes:
            self._check_attribute(key, new_attributes[key])
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
            except (NameError, ValueError):
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

    def add_child(self, child: 'XMLElement', forward=None) -> 'XMLElement':
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

    def to_string(self, intelligent_choice=False) -> str:
        self._final_checks(intelligent_choice=intelligent_choice)
        self._create_et_xml_element()

        ET.indent(self.et_xml_element, space="    ", level=self.level)
        return ET.tostring(self.et_xml_element, encoding='unicode') + '\n'

    def __setattr__(self, key, value):
        if key[0] == '_' or key in self.PROPERTIES:
            if key == 'value' and value is not None:
                try:
                    self._set_attributes({key: value})
                except XSDWrongAttribute:
                    super().__setattr__(key, value)
            else:
                super().__setattr__(key, value)
        else:
            self._set_attributes({key: value})
