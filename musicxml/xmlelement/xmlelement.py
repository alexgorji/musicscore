import copy
from xml.etree import ElementTree as ET
from musicxml.exceptions import XMLElementValueRequiredError, XMLElementChildrenRequired
from musicxml.util.core import root1, ns, cap_first, convert_to_xsd_class_name, convert_to_xml_class_name
from musicxml.xmlelement.exceptions import XMLChildContainerWrongElementError, XMLChildContainerMaxOccursError, \
    XMLChildContainerChoiceHasOtherElement, XMLChildContainerFactoryError, XMLChildContainerElementRequired
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdcomplextype import XSDComplexType
from musicxml.xsd.xsdelement import XSDElement
from musicxml.xsd.xsdindicators import XSDGroup, XSDSequence, XSDChoice
from musicxml.xsd.xsdindicators import *
from musicxml.xsd.xsdtree import XSDTree
from tree.tree import Tree


def _check_element_container(xsd_container_element):
    if not isinstance(xsd_container_element.content, XSDElement):
        raise TypeError(xsd_container_element.content)
    if len(xsd_container_element.content.xml_elements) < int(xsd_container_element.min_occurrences):
        raise XMLChildContainerElementRequired(f"Element {convert_to_xml_class_name(xsd_container_element.content.name)} is required")


def _check_group_container(xsd_container_group):
    if not isinstance(xsd_container_group.content, XSDGroup):
        raise TypeError(xsd_container_group.content)
    if xsd_container_group.min_occurrences != 0:
        if isinstance(xsd_container_group.get_children()[0].content, XSDSequence):
            _check_sequence_container(xsd_container_group.get_children()[0])
        else:
            raise NotImplementedError


def _check_sequence_container(xsd_container_sequence):
    if not isinstance(xsd_container_sequence.content, XSDSequence):
        raise TypeError(xsd_container_sequence.content)
    if xsd_container_sequence.min_occurrences != 0:
        for child in xsd_container_sequence.get_children():
            if isinstance(child.content, XSDElement):
                _check_element_container(child)
            elif isinstance(child.content, XSDSequence):
                _check_sequence_container(child)
            elif isinstance(child.content, XSDGroup):
                _check_group_container(child)
            elif isinstance(child.content, XSDChoice):
                _check_choice_container(child)
            else:
                raise ValueError(child)


def _check_choice_container(xsd_container_choice):
    if not isinstance(xsd_container_choice.content, XSDChoice):
        raise TypeError(xsd_container_choice.content)
    if xsd_container_choice.min_occurrences != 0:
        for child in xsd_container_choice.get_children():
            if isinstance(child.content, XSDElement):
                try:
                    _check_element_container(child)
                    return
                except XMLChildContainerElementRequired:
                    pass
        raise XMLChildContainerElementRequired(
            f"One of choice elements {_get_choice_required_element_names(xsd_container_choice)} is required"
        )


def _convert_xsd_child_to_xsd_container(xsd_child):
    min_occurrences = xsd_child.get_attributes().get('minOccurs')
    max_occurrences = xsd_child.get_attributes().get('maxOccurs')
    copied_xml_child = copy.deepcopy(xsd_child)
    if min_occurrences is not None:
        copied_xml_child.get_attributes().pop('minOccurs')
    if max_occurrences is not None:
        copied_xml_child.get_attributes().pop('maxOccurs')
    if xsd_child.tag == 'element':
        return XMLChildContainer(content=XSDElement(copied_xml_child), min_occurrences=min_occurrences,
                                 max_occurrences=max_occurrences)
    elif xsd_child.tag == 'sequence':
        return XMLChildContainer(content=XSDSequence(copied_xml_child), min_occurrences=min_occurrences,
                                 max_occurrences=max_occurrences)
    elif xsd_child.tag == 'choice':
        return XMLChildContainer(content=XSDChoice(copied_xml_child), min_occurrences=min_occurrences,
                                 max_occurrences=max_occurrences)
    elif xsd_child.tag == 'group':
        xsd_group_name = 'XSDGroup' + ''.join([cap_first(partial) for partial in xsd_child.get_attributes()['ref'].split('-')])
        return XMLChildContainer(content=eval(xsd_group_name)(), min_occurrences=min_occurrences,
                                 max_occurrences=max_occurrences)
    else:
        raise NotImplementedError(xsd_child.tag)


def _get_container_required_element_names(xsd_container):
    if isinstance(xsd_container.content, XSDSequence):
        return _get_sequence_required_element_names(xsd_container)
    elif isinstance(xsd_container.content, XSDGroup):
        return _get_group_required_element_names(xsd_container)
    elif isinstance(xsd_container.content, XSDChoice):
        return _get_choice_required_element_names(xsd_container)
    else:
        raise NotImplementedError()


def _get_choice_required_element_names(xsd_container_choice):
    for leaf in xsd_container_choice.iterate_leaves():
        if leaf.content.xml_elements:
            return None
    output = []
    for child in xsd_container_choice.get_children():
        if int(child.min_occurrences) == 0:
            pass
        elif int(child.min_occurrences) == 1:
            if isinstance(child.content, XSDElement):
                output.append(convert_to_xml_class_name(child.content.name))
            else:
                required_element_names = _get_container_required_element_names(child)
                if required_element_names:
                    output.append(required_element_names)
        else:
            raise NotImplementedError(f'child {child} with min_occurrence greater than 1')

    if not output:
        return None
    elif len(output) == 1:
        return output[0]
    else:
        return tuple(output)


def _get_group_required_element_names(xsd_group_container):
    return _get_sequence_required_element_names(xsd_group_container.get_children()[0])


def _get_sequence_required_element_names(xsd_sequence_container):
    output = []
    for child in xsd_sequence_container.get_children():
        if int(child.min_occurrences) == 0:
            pass
        elif int(child.min_occurrences) == 1:
            if isinstance(child.content, XSDElement):
                if not child.content.xml_elements:
                    output.append(convert_to_xml_class_name(child.content.name))
            else:
                required_element_names = _get_container_required_element_names(child)
                if required_element_names:
                    output.append(required_element_names)
        else:
            raise NotImplementedError(f'child {child} with min_occurrence greater than 1')
    if not output:
        return None
    elif len(output) == 1:
        return output[0]
    else:
        return output


def _check_filled_containers(xsd_container):
    for leaf in [l for l in xsd_container.iterate_leaves() if l.content.xml_elements]:
        for node in leaf.reversed_path_to_root():
            if isinstance(node.content, XSDSequence) and node.min_occurrences == 0:
                node.force_validate = True


def _check_if_container_require_elements(xsd_container):
    _check_filled_containers(xsd_container)
    if isinstance(xsd_container.content, XSDSequence):
        return _check_if_sequence_require_elements(xsd_container)
    elif isinstance(xsd_container.content, XSDGroup):
        return _check_if_group_require_elements(xsd_container)
    elif isinstance(xsd_container.content, XSDChoice):
        return _check_if_choice_require_elements(xsd_container)
    else:
        raise NotImplementedError(xsd_container)


def _check_if_choice_require_elements(xsd_container_choice):
    required_element_names = []
    element_chosen = False
    for child in xsd_container_choice.get_children():
        if child.force_validate:
            _check_if_container_require_elements(child)
        else:
            if child.min_occurrences == 0:
                pass
            elif int(child.min_occurrences) == 1:
                if isinstance(child.content, XSDElement):
                    if len(child.content.xml_elements) == 0:
                        required_element_names.append(convert_to_xml_class_name(child.content.name))
                    elif len(child.content.xml_elements) == 1:
                        element_chosen = True
                    else:
                        raise NotImplementedError(child)
                else:
                    other_required_element_names = _check_if_container_require_elements(child)
                    if other_required_element_names:
                        required_element_names.append(other_required_element_names)
            else:
                raise NotImplementedError(f'child {child} with min_occurrence greater than 1')

    if element_chosen:
        xsd_container_choice.requirement_not_fulfilled = False
        required_element_names = []
    if not required_element_names:
        return None
    elif len(required_element_names) == 1:
        return required_element_names[0]
    else:
        return tuple(required_element_names)


def _check_if_group_require_elements(xsd_group_container):
    return _check_if_sequence_require_elements(xsd_group_container.get_children()[0])


def _check_if_sequence_require_elements(xsd_sequence_container):
    if xsd_sequence_container.force_validate:
        for child in xsd_sequence_container.get_children():
            if isinstance(child.content, XSDElement):
                if len(child.content.xml_elements) < child.min_occurrences:
                    child.requirement_not_fulfilled = True
                else:
                    pass
            else:
                _check_if_container_require_elements(child)

    def force_validate_child(ch):
        for grandchild in ch.get_children():
            if isinstance(grandchild.content, XSDElement):
                if len(grandchild.content.xml_elements) == 0:
                    grandchild.requirement_not_fulfilled = True
            else:
                _check_if_container_require_elements(grandchild)

    def validate_child(ch):
        if isinstance(ch.content, XSDElement):
            if child.choices_in_reversed_path:
                pass
            elif len(ch.content.xml_elements) == 0:
                ch.requirement_not_fulfilled = True
            elif len(ch.content.xml_elements) == 1:
                pass
            else:
                raise NotImplementedError(ch)
        else:
            _check_if_container_require_elements(ch)

    for child in xsd_sequence_container.get_children():
        if child.force_validate is True:
            _check_if_container_require_elements(child)
            # force_validate_child(child)
        elif child.min_occurrences == 0:
            pass
        elif child.min_occurrences == 1:
            validate_child(child)
        else:
            raise NotImplementedError(f'child {child} with min_occurrence greater than 1')


class XMLChildContainer(Tree):
    def __init__(self, content, min_occurrences=None, max_occurrences=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._content = None
        self._required_element_names = None
        self._requirement_not_fulfilled = None
        self.min_occurrences = 1 if min_occurrences is None else int(min_occurrences)
        self.max_occurrences = 1 if max_occurrences is None else 'unbounded' if max_occurrences == 'unbounded' else int(max_occurrences)
        self.content = content
        self.force_validate = False

        self._populate_children()

    # private methods
    @staticmethod
    def _check_content_type(val):
        types = [XSDSequence, XSDChoice, XSDElement, XSDGroup]
        for type_ in types:
            if isinstance(val, type_):
                return
        raise TypeError(val)

    def _check_child(self, child):
        if not isinstance(child, XMLChildContainer):
            raise TypeError

    def _populate_children(self):
        for xsd_child in [child for child in self.content.xsd_tree.get_children() if
                          child.tag != 'annotation' and child.tag != 'complexType']:
            container = _convert_xsd_child_to_xsd_container(xsd_child)
            self.add_child(container)

    def _set_requirement_not_fulfilled(self):
        for node in self.traverse():
            if isinstance(node.content, XSDChoice) and node.requirement_not_fulfilled is None and True not in [
                choice.requirement_not_fulfilled for choice in node.choices_in_reversed_path] and node.min_occurrences != 0:
                for leaf in node.iterate_leaves():
                    if leaf.content.xml_elements:
                        node._requirement_not_fulfilled = False
                if node._requirement_not_fulfilled is None:
                    for child in node.get_children():
                        if child.min_occurrences != 0:
                            node._requirement_not_fulfilled = True
                        break
            else:
                node._requirement_not_fulfilled = False

    # public properties

    @property
    def compact_repr(self):
        if isinstance(self.content, XSDSequence):
            type_ = 'Sequence'
            return f"{type_}@minOccurs={self.min_occurrences}@maxOccurs={self.max_occurrences}"

        if isinstance(self.content, XSDChoice):
            type_ = 'Choice'
            output = f"{type_}@minOccurs={self.min_occurrences}@maxOccurs={self.max_occurrences}"
            if self.requirement_not_fulfilled:
                output += '\n'
                output += self.get_indentation() + '    '
                output += '!Required!'
            return output

        if isinstance(self.content, XSDGroup):
            type_ = 'Group'
            return f"{type_}@name={self.content.name}@minOccurs={self.min_occurrences}@maxOccurs={self.max_occurrences}"

        if isinstance(self.content, XSDElement):
            type_ = 'Element'
            output = f"{type_}@name={self.content.name}@minOccurs={self.min_occurrences}@maxOccurs={self.max_occurrences}"
            for xml_element in self.content.xml_elements:
                output += '\n'
                output += self.get_indentation() + '    '
                output += xml_element.get_class_name()
            if self.requirement_not_fulfilled:
                output += '\n'
                output += self.get_indentation() + '    '
                output += '!Required!'
            return output

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, val):
        self._check_content_type(val)
        self._content = val

    @property
    def choices_in_reversed_path(self):
        return [node for node in list(self.reversed_path_to_root())[1:] if isinstance(node.content, XSDChoice)]

    @property
    def requirement_not_fulfilled(self):
        return self._requirement_not_fulfilled

    @requirement_not_fulfilled.setter
    def requirement_not_fulfilled(self, val):
        if not isinstance(val, bool):
            raise TypeError
        self._requirement_not_fulfilled = val

    # public methods

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
                        continue
                    if isinstance(node.get_parent().content, XSDChoice):
                        for child in node.get_parent().get_children():
                            if isinstance(child.content, XSDElement) and child.content.xml_elements:
                                _choice_has_already_an_element = True
                    _element_max_occurrence_is_reached = False
                    node.content.add_xml_element(xml_element)
                    _element_added = True
                    if len(node.content.xml_elements) >= int(node.min_occurrences) and node.requirement_not_fulfilled:
                        node.requirement_not_fulfilled = False
                    for n in node.reversed_path_to_root():
                        if isinstance(n.content, XSDChoice):
                            if n.requirement_not_fulfilled is True:
                                n.requirement_not_fulfilled = False
                                break
                        if isinstance(n.content, XSDSequence):
                            n.force_validate = True
                    break
        if _element_max_occurrence_is_reached:
            raise XMLChildContainerMaxOccursError()
        if _choice_has_already_an_element:
            raise XMLChildContainerChoiceHasOtherElement()
        if not _element_added:
            raise XMLChildContainerWrongElementError()

        return xml_element

    def check_required_elements(self):
        if self._requirement_not_fulfilled is None:
            self._set_requirement_not_fulfilled()
        _check_if_container_require_elements(self)
        for node in self.traverse():
            if node.requirement_not_fulfilled:
                return True
        return False

    def get_leaves(self, function=None):
        if isinstance(self.content, XSDElement):
            if function:
                return function(self)
            else:
                return self.content
        elif isinstance(self.content, XSDGroup):
            return self.get_children()[0].get_leaves(function=function)
        elif isinstance(self.content, XSDSequence) or isinstance(self.content, XSDChoice):
            output = [node.get_leaves(function=function) for node in self.get_children() if node.get_leaves(function=function)]
            try:
                if not output or set(output) == {None}:
                    return None
            except TypeError:
                pass
            if len(output) == 1:
                return output[0]
            return output if isinstance(self.content, XSDSequence) else tuple(output)
        # elif isinstance(self.content, XSDChoice):
        #     output = [node.get_leaves(function=function) for node in self.get_children() if node.get_leaves(function=function)]
        #     try:
        #         if not output or set(output) == {None}:
        #             return None
        #     except TypeError:
        #         pass
        #     if len(output) == 1:
        #         return output[0]
        #     return tuple(output)
        else:
            raise NotImplementedError

    def get_required_element_names(self):
        def func(leaf):
            if leaf.requirement_not_fulfilled is True:
                return convert_to_xml_class_name(leaf.content.name)

            elif leaf.min_occurrences != 0 and True in [choice.requirement_not_fulfilled for choice in leaf.choices_in_reversed_path]:
                if isinstance(leaf.get_parent().content, XSDSequence) and leaf.get_parent().min_occurrences == 0 and not leaf.get_parent(

                ).force_validate:
                    pass
                else:
                    return convert_to_xml_class_name(leaf.content.name)

        self.check_required_elements()
        return self.get_leaves(func)

    #
    # def _get_required_element_names(self):
    #     if isinstance(self.content, XSDElement):
    #         if self.requirement_not_fulfilled:
    #             return convert_to_xml_class_name(self.content.name)
    #     elif isinstance(self.content, XSDSequence) or isinstance(self.content, XSDGroup):
    #         output = [child._get_required_element_names() for child in self.get_children() if child._get_required_element_names()]
    #         if not output:
    #             return None
    #         else:
    #             return output
    #     elif isinstance(self.content, XSDChoice):
    #         if self.requirement_not_fulfilled:
    #             output = []
    #             for child in self.get_children():
    #                 if isinstance(child.content, XSDElement):
    #                     output.append(convert_to_xml_class_name(child.content.name))
    #                 elif isinstance(child.content, XSDSequence):
    #                     for grandchild in child.get_children():
    #                         if isinstance(child.content, XSDElement) and grandchild.min_occurrences != 0:
    #                             output.append(convert_to_xml_class_name(grandchild.content.name))
    #                         else:
    #                             required = grandchild._get_required_element_names()
    #                             if required:
    #                                 output.append(required)
    #                 elif isinstance(child.content, XSDChoice):
    #                     required = child._get_required_element_names()
    #                     if required:
    #                         output.append(required)
    #                 elif isinstance(child.content, XSDGroup):
    #                     if
    #                     required = child._get_required_element_names()
    #                     if required:
    #                         output.append(required)
    #                 else:
    #                     raise NotImplementedError(child)
    #                     #
    #                     # if required:
    #                     #     output.append(required)
    #
    #             if not output:
    #                 return None
    #             else:
    #                 return tuple(output)
    #     else:
    #         raise NotImplementedError
    #
    #     # self.check_required_elements()
    #     # return self._required_element_names
    #     # return output
    #
    # def get_required_element_names(self):
    #     self.check_required_elements()
    #     return self._get_required_element_names()

    def __repr__(self):
        return f"XMLChildContainer:{self.compact_repr}"


class XMLChildContainerFactory:
    def __init__(self, complex_type):
        self._child_container = None
        self._create_child_container(complex_type)

    def _create_child_container(self, complex_type):
        if XSDComplexType not in complex_type.__mro__:
            raise TypeError
        if not complex_type.get_xsd_indicator():
            raise XMLChildContainerFactoryError(f'complex_type {complex_type} has no xsd_indicator.')
        child_container = XMLChildContainer(complex_type.get_xsd_indicator())
        self._child_container = child_container

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
        self._child_container_tree = None
        self.value = value
        self._set_attributes(kwargs)
        self._create_et_xml_element()
        self._set_child_container_tree()

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

    def _set_child_container_tree(self):
        if self.type_.XSD_TREE.is_complex_type:
            pass

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
    def child_container_tree(self):
        return self._child_container_tree

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
# __all__ = xml_element_class_names
__all__ = ['XMLAccent', 'XMLAccidental', 'XMLAccidentalMark', 'XMLAccidentalText', 'XMLAccord',
           'XMLAccordionHigh', 'XMLAccordionLow', 'XMLAccordionMiddle', 'XMLAccordionRegistration',
           'XMLActualNotes', 'XMLAlter', 'XMLAppearance', 'XMLArpeggiate', 'XMLArrow',
           'XMLArrowDirection', 'XMLArrowStyle', 'XMLArrowhead', 'XMLArticulations',
           'XMLArtificial', 'XMLAssess', 'XMLAttributes', 'XMLBackup', 'XMLBarStyle', 'XMLBarline',
           'XMLBarre', 'XMLBasePitch', 'XMLBass', 'XMLBassAlter', 'XMLBassSeparator', 'XMLBassStep',
           'XMLBeam', 'XMLBeatRepeat', 'XMLBeatType', 'XMLBeatUnit', 'XMLBeatUnitDot',
           'XMLBeatUnitTied', 'XMLBeater', 'XMLBeats', 'XMLBend', 'XMLBendAlter', 'XMLBookmark',
           'XMLBottomMargin', 'XMLBracket', 'XMLBrassBend', 'XMLBreathMark', 'XMLCaesura',
           'XMLCancel', 'XMLCapo', 'XMLChord', 'XMLChromatic', 'XMLCircularArrow', 'XMLClef',
           'XMLClefOctaveChange', 'XMLCoda', 'XMLConcertScore', 'XMLCreator', 'XMLCredit',
           'XMLCreditImage', 'XMLCreditSymbol', 'XMLCreditType', 'XMLCreditWords', 'XMLCue',
           'XMLDamp', 'XMLDampAll', 'XMLDashes', 'XMLDefaults', 'XMLDegree', 'XMLDegreeAlter',
           'XMLDegreeType', 'XMLDegreeValue', 'XMLDelayedInvertedTurn', 'XMLDelayedTurn',
           'XMLDetachedLegato', 'XMLDiatonic', 'XMLDirection', 'XMLDirectionType',
           'XMLDisplayOctave', 'XMLDisplayStep', 'XMLDisplayText', 'XMLDistance', 'XMLDivisions',
           'XMLDoit', 'XMLDot', 'XMLDouble', 'XMLDoubleTongue', 'XMLDownBow', 'XMLDuration',
           'XMLDynamics', 'XMLEffect', 'XMLElevation', 'XMLElision', 'XMLEncoder', 'XMLEncoding',
           'XMLEncodingDate', 'XMLEncodingDescription', 'XMLEndLine', 'XMLEndParagraph',
           'XMLEnding', 'XMLEnsemble', 'XMLExceptVoice', 'XMLExtend', 'XMLEyeglasses', 'XMLF',
           'XMLFalloff', 'XMLFeature', 'XMLFermata', 'XMLFf', 'XMLFff', 'XMLFfff', 'XMLFffff',
           'XMLFfffff', 'XMLFifths', 'XMLFigure', 'XMLFigureNumber', 'XMLFiguredBass',
           'XMLFingering', 'XMLFingernails', 'XMLFirst', 'XMLFirstFret', 'XMLFlip', 'XMLFootnote',
           'XMLForPart', 'XMLForward', 'XMLFp', 'XMLFrame', 'XMLFrameFrets', 'XMLFrameNote',
           'XMLFrameStrings', 'XMLFret', 'XMLFunction', 'XMLFz', 'XMLGlass', 'XMLGlissando',
           'XMLGlyph', 'XMLGolpe', 'XMLGrace', 'XMLGroup', 'XMLGroupAbbreviation',
           'XMLGroupAbbreviationDisplay', 'XMLGroupBarline', 'XMLGroupLink', 'XMLGroupName',
           'XMLGroupNameDisplay', 'XMLGroupSymbol', 'XMLGroupTime', 'XMLGrouping', 'XMLHalfMuted',
           'XMLHammerOn', 'XMLHandbell', 'XMLHarmonClosed', 'XMLHarmonMute', 'XMLHarmonic',
           'XMLHarmony', 'XMLHarpPedals', 'XMLHaydn', 'XMLHeel', 'XMLHole', 'XMLHoleClosed',
           'XMLHoleShape', 'XMLHoleType', 'XMLHumming', 'XMLIdentification', 'XMLImage',
           'XMLInstrument', 'XMLInstrumentAbbreviation', 'XMLInstrumentChange', 'XMLInstrumentLink',
           'XMLInstrumentName', 'XMLInstrumentSound', 'XMLInstruments', 'XMLInterchangeable',
           'XMLInversion', 'XMLInvertedMordent', 'XMLInvertedTurn', 'XMLInvertedVerticalTurn',
           'XMLIpa', 'XMLKey', 'XMLKeyAccidental', 'XMLKeyAlter', 'XMLKeyOctave', 'XMLKeyStep',
           'XMLKind', 'XMLLaughing', 'XMLLeftDivider', 'XMLLeftMargin', 'XMLLevel', 'XMLLine',
           'XMLLineDetail', 'XMLLineWidth', 'XMLLink', 'XMLListen', 'XMLListening', 'XMLLyric',
           'XMLLyricFont', 'XMLLyricLanguage', 'XMLMeasure', 'XMLMeasureDistance',
           'XMLMeasureLayout', 'XMLMeasureNumbering', 'XMLMeasureRepeat', 'XMLMeasureStyle',
           'XMLMembrane', 'XMLMetal', 'XMLMetronome', 'XMLMetronomeArrows', 'XMLMetronomeBeam',
           'XMLMetronomeDot', 'XMLMetronomeNote', 'XMLMetronomeRelation', 'XMLMetronomeTied',
           'XMLMetronomeTuplet', 'XMLMetronomeType', 'XMLMf', 'XMLMidiBank', 'XMLMidiChannel',
           'XMLMidiDevice', 'XMLMidiInstrument', 'XMLMidiName', 'XMLMidiProgram',
           'XMLMidiUnpitched', 'XMLMillimeters', 'XMLMiscellaneous', 'XMLMiscellaneousField',
           'XMLMode', 'XMLMordent', 'XMLMovementNumber', 'XMLMovementTitle', 'XMLMp',
           'XMLMultipleRest', 'XMLMusicFont', 'XMLMute', 'XMLN', 'XMLNatural', 'XMLNonArpeggiate',
           'XMLNormalDot', 'XMLNormalNotes', 'XMLNormalType', 'XMLNotations', 'XMLNote',
           'XMLNoteSize', 'XMLNotehead', 'XMLNoteheadText', 'XMLNumeral', 'XMLNumeralAlter',
           'XMLNumeralFifths', 'XMLNumeralKey', 'XMLNumeralMode', 'XMLNumeralRoot', 'XMLOctave',
           'XMLOctaveChange', 'XMLOctaveShift', 'XMLOffset', 'XMLOpen', 'XMLOpenString', 'XMLOpus',
           'XMLOrnaments', 'XMLOtherAppearance', 'XMLOtherArticulation', 'XMLOtherDirection',
           'XMLOtherDynamics', 'XMLOtherListen', 'XMLOtherListening', 'XMLOtherNotation',
           'XMLOtherOrnament', 'XMLOtherPercussion', 'XMLOtherPlay', 'XMLOtherTechnical', 'XMLP',
           'XMLPageHeight', 'XMLPageLayout', 'XMLPageMargins', 'XMLPageWidth', 'XMLPan', 'XMLPart',
           'XMLPartAbbreviation', 'XMLPartAbbreviationDisplay', 'XMLPartClef', 'XMLPartGroup',
           'XMLPartLink', 'XMLPartList', 'XMLPartName', 'XMLPartNameDisplay', 'XMLPartSymbol',
           'XMLPartTranspose', 'XMLPedal', 'XMLPedalAlter', 'XMLPedalStep', 'XMLPedalTuning',
           'XMLPerMinute', 'XMLPercussion', 'XMLPf', 'XMLPitch', 'XMLPitched', 'XMLPlay',
           'XMLPlayer', 'XMLPlayerName', 'XMLPlop', 'XMLPluck', 'XMLPp', 'XMLPpp', 'XMLPppp',
           'XMLPpppp', 'XMLPppppp', 'XMLPreBend', 'XMLPrefix', 'XMLPrincipalVoice', 'XMLPrint',
           'XMLPullOff', 'XMLRehearsal', 'XMLRelation', 'XMLRelease', 'XMLRepeat', 'XMLRest',
           'XMLRf', 'XMLRfz', 'XMLRightDivider', 'XMLRightMargin', 'XMLRights', 'XMLRoot',
           'XMLRootAlter', 'XMLRootStep', 'XMLScaling', 'XMLSchleifer', 'XMLScoop', 'XMLScordatura',
           'XMLScoreInstrument', 'XMLScorePart', 'XMLScorePartwise', 'XMLSecond', 'XMLSegno',
           'XMLSemiPitched', 'XMLSenzaMisura', 'XMLSf', 'XMLSffz', 'XMLSfp', 'XMLSfpp', 'XMLSfz',
           'XMLSfzp', 'XMLShake', 'XMLSign', 'XMLSlash', 'XMLSlashDot', 'XMLSlashType', 'XMLSlide',
           'XMLSlur', 'XMLSmear', 'XMLSnapPizzicato', 'XMLSoftAccent', 'XMLSoftware', 'XMLSolo',
           'XMLSound', 'XMLSoundingPitch', 'XMLSource', 'XMLSpiccato', 'XMLStaccatissimo',
           'XMLStaccato', 'XMLStaff', 'XMLStaffDetails', 'XMLStaffDistance', 'XMLStaffDivide',
           'XMLStaffLayout', 'XMLStaffLines', 'XMLStaffSize', 'XMLStaffTuning', 'XMLStaffType',
           'XMLStaves', 'XMLStem', 'XMLStep', 'XMLStick', 'XMLStickLocation', 'XMLStickMaterial',
           'XMLStickType', 'XMLStopped', 'XMLStraight', 'XMLStress', 'XMLString', 'XMLStringMute',
           'XMLStrongAccent', 'XMLSuffix', 'XMLSupports', 'XMLSwing', 'XMLSwingStyle',
           'XMLSwingType', 'XMLSyllabic', 'XMLSymbol', 'XMLSync', 'XMLSystemDistance',
           'XMLSystemDividers', 'XMLSystemLayout', 'XMLSystemMargins', 'XMLTap', 'XMLTechnical',
           'XMLTenths', 'XMLTenuto', 'XMLText', 'XMLThumbPosition', 'XMLTie', 'XMLTied', 'XMLTime',
           'XMLTimeModification', 'XMLTimeRelation', 'XMLTimpani', 'XMLToe', 'XMLTopMargin',
           'XMLTopSystemDistance', 'XMLTouchingPitch', 'XMLTranspose', 'XMLTremolo', 'XMLTrillMark',
           'XMLTripleTongue', 'XMLTuningAlter', 'XMLTuningOctave', 'XMLTuningStep', 'XMLTuplet',
           'XMLTupletActual', 'XMLTupletDot', 'XMLTupletNormal', 'XMLTupletNumber', 'XMLTupletType',
           'XMLTurn', 'XMLType', 'XMLUnpitched', 'XMLUnstress', 'XMLUpBow', 'XMLVerticalTurn',
           'XMLVirtualInstrument', 'XMLVirtualLibrary', 'XMLVirtualName', 'XMLVoice', 'XMLVolume',
           'XMLWait', 'XMLWavyLine', 'XMLWedge', 'XMLWithBar', 'XMLWood', 'XMLWordFont', 'XMLWords',
           'XMLWork', 'XMLWorkNumber', 'XMLWorkTitle']
