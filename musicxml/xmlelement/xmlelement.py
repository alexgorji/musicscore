import copy
from xml.etree import ElementTree as ET
from musicxml.exceptions import XMLElementValueRequiredError, XMLElementChildrenRequired
from musicxml.util.core import root1, ns, cap_first, convert_to_xsd_class_name, convert_to_xml_class_name
from musicxml.xmlelement.exceptions import XMLChildContainerWrongElementError, XMLChildContainerMaxOccursError, \
    XMLChildContainerChoiceHasOtherElement
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdcomplextype import XSDComplexType
from musicxml.xsd.xsdelement import XSDElement
from musicxml.xsd.xsdindicators import XSDGroup, XSDSequence, XSDChoice
from musicxml.xsd.xsdtree import XSDTree
from tree.tree import Tree


class XMLChildContainer(Tree):
    def __init__(self, content, min_occurrences=None, max_occurrences=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._content = None
        if min_occurrences is None:
            min_occurrences = 1
        if max_occurrences is None:
            max_occurrences = 1
        self.min_occurrences = min_occurrences
        self.max_occurrences = max_occurrences
        self.content = content
        self._populate_children()

    def _populate_children(self):
        for xsd_child in self.content.xsd_tree.get_children():
            if xsd_child.tag == 'element':
                min_occurrences = xsd_child.get_attributes().get('minOccurs')
                max_occurrences = xsd_child.get_attributes().get('maxOccurs')
                copied_xml_child = copy.deepcopy(xsd_child)
                if min_occurrences is not None:
                    copied_xml_child.get_attributes().pop('minOccurs')
                if max_occurrences is not None:
                    copied_xml_child.get_attributes().pop('maxOccurs')
                container = XMLChildContainer(content=XSDElement(copied_xml_child), min_occurrences=min_occurrences,
                                              max_occurrences=max_occurrences)
                self.add_child(container)

    @staticmethod
    def _check_content_type(val):
        types = [XSDSequence, XSDChoice, XSDElement, XSDGroup]
        for type_ in types:
            if isinstance(val, type_):
                return
        raise TypeError

    def _check_child(self, child):
        if not isinstance(child, XMLChildContainer):
            return TypeError

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, val):
        self._check_content_type(val)
        self._content = val

    @property
    def compact_repr(self):
        type_ = None
        if isinstance(self.content, XSDSequence):
            type_ = 'Sequence'
        elif isinstance(self.content, XSDChoice):
            type_ = 'Choice'
        elif isinstance(self.content, XSDGroup):
            type_ = 'Group'
        elif isinstance(self.content, XSDElement):
            type_ = 'Element'
            output = f"{type_}@name={self.content.name}@minOccurs={self.min_occurrences}@maxOccurs={self.max_occurrences}"
            for xml_element in self.content.xml_elements:
                output += '\n'
                output += '        '
                output += xml_element.get_class_name()
            return output
        try:
            return f"{type_}@name={self.content.name}@minOccurs={self.min_occurrences}@maxOccurs={self.max_occurrences}"
        except AttributeError:
            return f"{type_}@minOccurs={self.min_occurrences}@maxOccurs={self.max_occurrences}"

    def get_required_elements(self):
        output = []
        if isinstance(self.content, XSDSequence):
            for child in self.get_children():
                if isinstance(child.content, XSDElement):
                    if child.min_occurrences != '0':
                        output.append(convert_to_xml_class_name(name=child.content.name))
                else:
                    raise NotImplementedError
        else:
            raise NotImplementedError
        return output

    def add_element(self, xml_element):
        if not isinstance(xml_element, XMLElement):
            raise TypeError
        _element_added = False
        _element_max_occurrence_is_reached = False
        _choice_has_already_an_element = False
        for node in self.traverse():
            if isinstance(node.content, XSDElement):
                if node.content.name == xml_element.name:
                    if node.max_occurrences != 'unbounded' and len(node.content.xml_elements) == node.max_occurrences:
                        _element_max_occurrence_is_reached = True
                        break
                    if isinstance(node.get_parent().content, XSDChoice):
                        for child in node.get_parent().get_children():
                            if isinstance(child.content, XSDElement) and child.content.xml_elements:
                                _choice_has_already_an_element = True
                    _element_max_occurrence_is_reached = False
                    node.content.add_xml_element(xml_element)
                    _element_added = True
                    break
        if _element_max_occurrence_is_reached:
            raise XMLChildContainerMaxOccursError()
        if _choice_has_already_an_element:
            raise XMLChildContainerChoiceHasOtherElement()
        if not _element_added:
            raise XMLChildContainerWrongElementError()


class XMLChildContainerFactory:
    def __init__(self, complex_type):
        self._child_container = None
        self._create_child_container(complex_type)

    def _create_child_container(self, complex_type):
        if XSDComplexType not in complex_type.__mro__:
            raise TypeError
        children_container = XMLChildContainer(complex_type.get_xsd_indicator())
        self._child_container = children_container

    def get_child_container(self):
        return self._child_container


class XMLElement(Tree):
    XSD_TREE = None

    def __init__(self, value=None, **kwargs):
        super().__init__()
        self._value = None
        self._attributes = None
        self._et_xml_element = None
        self._type = None
        self.value = value
        self._set_attributes(kwargs)
        self._create_et_xml_element()

    def _check_child(self, child):
        if not isinstance(child, XMLElement):
            raise TypeError

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
        return convert_to_xml_class_name(cls.XSD_TREE.name)

    def add_child(self, child):
        child = super().add_child(child)
        self._et_xml_element.append(child._et_xml_element)
        return child

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
    copied_el = copy.deepcopy(found_et_xml)
    if copied_el.attrib.get('minOccurs'):
        copied_el.attrib.pop('minOccurs')
    if copied_el.attrib.get('maxOccurs'):
        copied_el.attrib.pop('maxOccurs')
    xsd_tree = XSDTree(copied_el)
    class_name = convert_to_xml_class_name(xsd_tree.name)
    base_classes = "(XMLElement, )"
    attributes = """
    {
    'XSD_TREE': xsd_tree,
    '__doc__': __doc__,
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
    xml_element_class_names.append(class_name)

# xml score partwise
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


xml_element_class_names.extend(['XMLScorePartwise', 'XMLPart', 'XMLMeasure'])
__all__ = xml_element_class_names
