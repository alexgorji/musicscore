import copy

from musicxml.util.core import convert_to_xml_class_name, cap_first
from musicxml.xmlelement.exceptions import XMLChildContainerFactoryError, XMLChildContainerWrongElementError, \
    XMLChildContainerChoiceHasAnotherChosenChild, XMLChildContainerMaxOccursError, XMLElementCannotHaveChildrenError
from musicxml.xsd.xsdelement import XSDElement
from musicxml.xsd.xsdindicator import *
from musicxml.xsd.xsdtree import XSDTree
from tree.tree import Tree

import xml.etree.ElementTree as ET

from tree.tree import Tree


def _convert_xsd_child_to_xsd_container(xsd_child):
    min_occurrences = xsd_child.get_attributes().get('minOccurs')
    max_occurrences = xsd_child.get_attributes().get('maxOccurs')

    copied_xsd_child = copy.deepcopy(xsd_child)
    if min_occurrences is not None:
        copied_xsd_child.get_attributes().pop('minOccurs')
    if max_occurrences is not None:
        copied_xsd_child.get_attributes().pop('maxOccurs')
    if xsd_child.tag == 'element':
        return XMLChildContainer(content=XSDElement(copied_xsd_child), min_occurrences=min_occurrences,
                                 max_occurrences=max_occurrences)
    elif xsd_child.tag == 'sequence':
        return XMLChildContainer(content=XSDSequence(copied_xsd_child), min_occurrences=min_occurrences,
                                 max_occurrences=max_occurrences)
    elif xsd_child.tag == 'choice':
        return XMLChildContainer(content=XSDChoice(copied_xsd_child), min_occurrences=min_occurrences,
                                 max_occurrences=max_occurrences)
    elif xsd_child.tag == 'group':
        xsd_group_name = 'XSDGroup' + ''.join([cap_first(partial) for partial in xsd_child.get_attributes()['ref'].split('-')])
        return XMLChildContainer(content=eval(xsd_group_name)(), min_occurrences=min_occurrences,
                                 max_occurrences=max_occurrences)
    else:
        raise NotImplementedError(xsd_child.tag)


def _check_if_container_requires_elements(xsd_container):
    if isinstance(xsd_container.content, XSDSequence):
        return _check_if_sequence_requires_elements(xsd_container)
    elif isinstance(xsd_container.content, XSDGroup):
        return _check_if_group_requires_elements(xsd_container)
    elif isinstance(xsd_container.content, XSDChoice):
        return _check_if_choice_requires_elements(xsd_container)
    else:
        raise NotImplementedError(xsd_container)


def _check_if_choice_requires_elements(xsd_container_choice):
    element_chosen = False
    for child in xsd_container_choice.get_children():
        if isinstance(child.content, XSDGroup):
            if child.get_children()[0].force_validate:
                _check_if_container_requires_elements(child.get_children()[0])
        elif child.force_validate:
            _check_if_container_requires_elements(child)
        else:
            if child.min_occurrences == 0:
                pass
            elif int(child.min_occurrences) == 1:
                if isinstance(child.content, XSDElement):
                    if len(child.content.xml_elements) == 0:
                        pass
                    elif len(child.content.xml_elements) == 1:
                        element_chosen = True
                    else:
                        raise NotImplementedError(child)
                else:
                    _check_if_container_requires_elements(child)
            else:
                raise NotImplementedError(f'child {child} with min_occurrence greater than 1')

    if element_chosen:
        xsd_container_choice.requirements_not_fulfilled = False


def _check_if_group_requires_elements(xsd_group_container):
    if xsd_group_container.min_occurrences == 0 and not xsd_group_container.get_children()[0].force_validate:
        return
    return _check_if_sequence_requires_elements(xsd_group_container.get_children()[0])


def _check_if_sequence_requires_elements(xsd_sequence_container):
    if xsd_sequence_container.force_validate:
        for child in xsd_sequence_container.get_children():
            if isinstance(child.content, XSDElement):
                if len(child.content.xml_elements) < child.min_occurrences:
                    child.requirements_not_fulfilled = True
                else:
                    pass
            else:
                _check_if_container_requires_elements(child)

    def validate_child(ch):
        if isinstance(ch.content, XSDElement):
            if child.choices_in_reversed_path:
                pass
            elif len(ch.content.xml_elements) < ch.min_occurrences:
                ch.requirements_not_fulfilled = True
            else:
                ch.requirements_not_fulfilled = False
        else:
            _check_if_container_requires_elements(ch)

    if xsd_sequence_container.min_occurrences > 0:
        for child in xsd_sequence_container.get_children():
            if child.force_validate is True:
                _check_if_container_requires_elements(child)
            elif child.min_occurrences == 0:
                pass
            elif child.min_occurrences == 1:
                validate_child(child)
            else:
                raise NotImplementedError(f'child {child} with min_occurrence greater than 1')


class DuplicationXSDSequence(XSDSequence):
    sequence_xsd = """
            <xs:sequence xmlns:xs="http://www.w3.org/2001/XMLSchema">
            </xs:sequence>
    """

    def __init__(self):
        xsd_tree_ = XSDTree(ET.fromstring(self.sequence_xsd))
        super().__init__(xsd_tree_)


class XMLChildContainer(Tree):
    def __init__(self, content, min_occurrences=None, max_occurrences=None, populate_children=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._content = None
        self._chosen_child = None
        self._required_element_names = None
        self._requirements_not_fulfilled = None
        self.min_occurrences = 1 if min_occurrences is None else int(min_occurrences)
        self.max_occurrences = 1 if max_occurrences is None else 'unbounded' if max_occurrences == 'unbounded' else int(max_occurrences)
        self.content = content
        self._force_validate = None
        self._parent_xml_element = None
        if populate_children:
            self._populate_children()

    # private methods
    def _add_duplication_parent(self):

        if not self.get_parent():
            parent_container = XMLChildContainer(content=DuplicationXSDSequence())
            parent_container.add_child(self)
        elif not (isinstance(self.get_parent().content, DuplicationXSDSequence)):
            parent_container = XMLChildContainer(content=DuplicationXSDSequence())
            index = self.get_parent().get_children().index(self)
            parent = self.get_parent()
            parent.remove(self)
            parent.get_children().insert(index, parent_container)
            parent_container._parent = parent
            parent_container.add_child(self)
            if isinstance(parent.content, XSDChoice) and parent.chosen_child == self:
                parent.chosen_child = parent_container
        else:
            pass

    @staticmethod
    def _check_content_type(val):
        types = [XSDSequence, XSDChoice, XSDElement, XSDGroup]
        for type_ in types:
            if isinstance(val, type_):
                return
        raise TypeError(val)

    def _check_child_to_be_added(self, child):
        if not isinstance(child, XMLChildContainer):
            raise TypeError

    def _check_choices_intelligently(self, xml_element=None):
        if self.get_parent_xml_element():
            print(f'_check_choices_intelligently: intelligent choice for {self.get_parent_xml_element()}')
        """
        Check if existing xml elements can be attached to other choice paths in order to fulfill all requirements. Only possible leaves
        forwards will be checked. If xml_element is given it will be treated as a new element which going to be attached to the container.
        """

        def get_same_name_next_leaves(leaf_):
            output = []
            index = -1
            record = False
            for l in self.iterate_leaves():
                if l.content.name == leaf_.content.name:
                    index += 1
                    if not record:
                        record = True
                    else:
                        output.append((l, index))
            return output

        def get_sorted_xml_elements(sorted_options_):
            unsorted_elements = [el for el in self.get_attached_elements() if el.name != sorted_options_[-1][0]]
            output = []
            for option in sorted_options_:
                selected_elements = [el for el in unsorted_elements if el.name == option[1]]
                for el in selected_elements:
                    unsorted_elements.remove(el)
                    output.append(el)
            output.extend(unsorted_elements)
            return output

        current_leaves_with_xml_elements = [leaf for leaf in self.iterate_leaves() if leaf.content.xml_elements]
        optional_next_leaves = [get_same_name_next_leaves(leaf) for leaf in current_leaves_with_xml_elements if
                                get_same_name_next_leaves(leaf)]
        if optional_next_leaves:
            indices = {list_of_leaves[0][0].content.name: [l[1] for l in list_of_leaves] for list_of_leaves in optional_next_leaves}
            sorted_options = sorted([(k, v) for k, v in indices.items()], key=lambda v: -len(v))
            sorted_xml_elements = get_sorted_xml_elements(sorted_options)
            efficient_xml_element_name, forward_indices = sorted_options.pop()
            efficient_xml_elements = [el for el in self.get_attached_elements() if el.name == efficient_xml_element_name]
            for element in efficient_xml_elements:
                for forward_index in forward_indices:
                    copied_container = self._create_empty_copy()
                    copied_container.add_element(element, forward_index)
                    try:
                        for el in sorted_xml_elements:
                            copied_container.add_element(el, intelligent_choice=False)
                        if xml_element:
                            copied_container.add_element(xml_element, intelligent_choice=False)
                            return copied_container
                        if not copied_container.check_required_elements():
                            return copied_container
                    except XMLChildContainerChoiceHasAnotherChosenChild:
                        pass
        return None

    def _create_empty_copy(self):
        """
        Creates a copy without attached elements or duplicated nodes
        :return: XMLChildContainer
        """
        if isinstance(self.content, XSDChoice) or isinstance(self.content, XSDSequence):
            copied_content = self.content.__class__(self.content.xsd_tree)
        else:
            copied_content = eval(self.content.__class__.__name__)()
        return XMLChildContainer(copied_content, self.min_occurrences, self.max_occurrences)

    def _duplicate_parent_in_path(self):
        for node in list(self.reversed_path_to_root())[:-1]:
            if node.get_parent().max_occurrences == 'unbounded':
                return node.get_parent().duplicate()
        return None

    def _update_requirements_in_path(self):
        if not isinstance(self.content, XSDElement):
            raise ValueError
        if self.max_is_reached:
            self.requirements_not_fulfilled = False
        if self.content.xml_elements:
            for node in self.reversed_path_to_root():
                if node.get_parent():
                    if isinstance(node.get_parent().content, XSDChoice):
                        if node.get_parent().chosen_child:
                            if node.get_parent().chosen_child != node:
                                raise XMLChildContainerChoiceHasAnotherChosenChild
                            else:
                                break
                        else:
                            node.get_parent().chosen_child = node
                            if node.get_parent().requirements_not_fulfilled:
                                node.get_parent().requirements_not_fulfilled = False
                                break
                            node.get_parent().requirements_not_fulfilled = False
                    elif isinstance(node.get_parent().content, XSDSequence):
                        if node.get_parent().force_validate:
                            break
                        else:
                            node.get_parent().set_force_validate(node, True)

    def _populate_children(self):
        for xsd_child in [child for child in self.content.xsd_tree.get_children() if
                          child.tag != 'annotation' and child.tag != 'complexType']:
            container = _convert_xsd_child_to_xsd_container(xsd_child)
            self.add_child(container)

    def _set_requirement_not_fulfilled(self):
        for node in self.traverse():
            if isinstance(node.content, XSDChoice) and node.requirements_not_fulfilled is None and True not in [
                choice.requirements_not_fulfilled for choice in node.choices_in_reversed_path] and node.min_occurrences != 0:
                for leaf in node.iterate_leaves():
                    if leaf.content.xml_elements:
                        node._requirements_not_fulfilled = False
                if node._requirements_not_fulfilled is None:
                    for child in node.get_children():
                        if child.min_occurrences != 0:
                            node._requirements_not_fulfilled = True
                        break
                if node._requirements_not_fulfilled is None:
                    node._requirements_not_fulfilled = False
            else:
                node._requirements_not_fulfilled = False

    # public properties

    @property
    def compact_repr(self):
        """
        :return: A compact representation of ChildContainerTree.content.
        """
        if isinstance(self.content, XSDSequence):
            type_ = 'Sequence'
            return f"{type_}@minOccurs={self.min_occurrences}@maxOccurs={self.max_occurrences}"

        if isinstance(self.content, XSDChoice):
            type_ = 'Choice'
            output = f"{type_}@minOccurs={self.min_occurrences}@maxOccurs={self.max_occurrences}"
            if self.requirements_not_fulfilled:
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
                output += xml_element.__class__.__name__
            if self.requirements_not_fulfilled:
                output += '\n'
                output += self.get_indentation() + '    '
                output += '!Required!'
            return output

    @property
    def content(self):
        """
        :return: Content of a ChildContainerTree is its core property. It can be of types: XSDSequence, XSDChoice, XSDGroup or XSDElement
        which are used to translate the behaviour of the according a xsd tags: sequence, choice, group and element.
        """
        return self._content

    @content.setter
    def content(self, val):
        self._check_content_type(val)
        self._content = val
        self._content.parent_container = self

    @property
    def choices_in_reversed_path(self):
        return [node for node in list(self.reversed_path_to_root())[1:] if isinstance(node.content, XSDChoice)]

    @property
    def chosen_child(self):
        return self._chosen_child

    @chosen_child.setter
    def chosen_child(self, val):
        if not isinstance(self.content, XSDChoice):
            raise TypeError
        self._chosen_child = val

    @property
    def force_validate(self):
        return self._force_validate

    @property
    def max_is_reached(self):
        if not isinstance(self.content, XSDElement):
            raise TypeError
        if self.max_occurrences == 'unbounded':
            return False
        else:
            if len(self.content.xml_elements) == self.max_occurrences:
                return True
            elif len(self.content.xml_elements) > self.max_occurrences:
                raise ValueError
            else:
                return False

    @property
    def requirements_not_fulfilled(self):
        return self._requirements_not_fulfilled

    @requirements_not_fulfilled.setter
    def requirements_not_fulfilled(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError
        self._requirements_not_fulfilled = val

    # public methods

    def add_element(self, xml_element, forward=None, intelligent_choice=True):
        if self._requirements_not_fulfilled is None:
            self.check_required_elements()

        def select_valid_leaves(leaves):
            output = []
            choice_with_chosen_child = None
            for index, leaf in enumerate(leaves):
                for n in leaf.reversed_path_to_root():
                    if n.get_parent() and isinstance(n.get_parent().content, XSDChoice) and n.get_parent().chosen_child:
                        choice_with_chosen_child = n.get_parent()
                        if n == choice_with_chosen_child.chosen_child:
                            output.append(leaf)
                        break

            if not choice_with_chosen_child:
                return leaves

            elif not output and choice_with_chosen_child.max_occurrences != 'unbounded':
                return None
            else:
                return output

        if 'XMLElement' not in [cls.__name__ for cls in xml_element.__class__.__mro__]:
            raise TypeError(xml_element.__class__)

        same_name_leaves = [leaf for leaf in self.iterate_leaves() if leaf.content.name == xml_element.name]

        if not same_name_leaves:
            raise XMLChildContainerWrongElementError()

        selected_same_name_leaves = select_valid_leaves(same_name_leaves)
        if selected_same_name_leaves is None:
            intelligently_selected = None
            if forward is None and intelligent_choice is True:
                copy_with_intelligence = self._check_choices_intelligently(xml_element)
                if copy_with_intelligence:
                    for old_child, new_child in zip(self.get_children(), copy_with_intelligence.get_children()):
                        self.replace_child(old_child, new_child)
                    return [l for l in copy_with_intelligence.iterate_leaves() if xml_element in l.content.xml_elements][0]

            if not intelligently_selected:
                msg = f"{self} By adding {xml_element.__class__.__name__} to {self.get_parent_xml_element().__class__.__name__}" if \
                    self.get_parent_xml_element() else f"{self} By adding {xml_element.__class__.__name__}"
                raise XMLChildContainerChoiceHasAnotherChosenChild(msg)
            else:
                self.check_required_elements()
                return intelligently_selected

        if selected_same_name_leaves == []:
            duplicated_parent = same_name_leaves[-1]._duplicate_parent_in_path()
            if duplicated_parent:
                selected_same_name_leaves = [leaf for leaf in duplicated_parent.iterate_leaves() if
                                             leaf.content.name == xml_element.name and not
                                             leaf.max_is_reached]
                if self._parent_xml_element and self.up:
                    self._parent_xml_element._child_container_tree = self.up

            else:
                raise XMLChildContainerChoiceHasAnotherChosenChild

        if forward is not None:
            selected = same_name_leaves[forward]
            if selected not in selected_same_name_leaves:
                raise XMLChildContainerChoiceHasAnotherChosenChild('Wrong forwarding')
        else:
            selected_same_name_leaves_max_not_reached = [leaf for leaf in selected_same_name_leaves if not leaf.max_is_reached]
            if not selected_same_name_leaves_max_not_reached:
                duplicated_parent = selected_same_name_leaves[-1]._duplicate_parent_in_path()
                if duplicated_parent:
                    selected_same_name_leaves_max_not_reached = [leaf for leaf in duplicated_parent.iterate_leaves() if leaf.content.name ==
                                                                 xml_element.name and not leaf.max_is_reached]
                    if self._parent_xml_element and self.up:
                        self._parent_xml_element._child_container_tree = self.up
                else:
                    raise XMLChildContainerMaxOccursError()

            selected = selected_same_name_leaves_max_not_reached[0]

        selected.content.add_xml_element(xml_element)
        selected._update_requirements_in_path()
        # self.check_required_elements()
        return selected

    def check_required_elements(self, intelligent_choice=False):
        if self._requirements_not_fulfilled is None:
            self._set_requirement_not_fulfilled()
        _check_if_container_requires_elements(self)
        requirements_exist = False
        for node in self.traverse():
            if node.requirements_not_fulfilled:
                requirements_exist = True
        if requirements_exist and intelligent_choice:
            if isinstance(self.content, XSDChoice):
                return requirements_exist
            copy_with_intelligence = self._check_choices_intelligently()
            if copy_with_intelligence:
                for old_child, new_child in zip(self.get_children(), copy_with_intelligence.get_children()):
                    self.replace_child(old_child, new_child)
                return False

        return requirements_exist

    check_requirements = check_required_elements

    def duplicate(self):
        if not isinstance(self.content, XSDSequence) and not isinstance(self.content, XSDChoice) and not isinstance(self.content, XSDGroup):
            raise TypeError(self.content)

        if self.max_occurrences != 'unbounded':
            raise ValueError

        self._add_duplication_parent()

        copied_self = self._create_empty_copy()
        copied_self._parent = self.get_parent()
        self.get_parent().add_child(copied_self)
        return copied_self

    def get_attached_elements(self):
        output = []
        for leaf in self.iterate_leaves():
            output.extend(leaf.content.xml_elements)
        return output

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
        else:
            raise NotImplementedError

    def get_parent_xml_element(self):
        """
        :return: XMLElement which child container is attached to.
        """
        return self._parent_xml_element

    def get_required_element_names(self, intelligent_choice=False):
        def func(leaf):
            if leaf.requirements_not_fulfilled is True:
                return convert_to_xml_class_name(leaf.content.name)

            elif leaf.min_occurrences != 0 and True in [choice.requirements_not_fulfilled for choice in leaf.choices_in_reversed_path]:
                if isinstance(leaf.get_parent().content, XSDSequence) and leaf.get_parent().min_occurrences == 0 and not leaf.get_parent(

                ).force_validate:
                    pass
                else:
                    return convert_to_xml_class_name(leaf.content.name)

        self.check_required_elements(intelligent_choice)
        return self.get_leaves(func)

    def set_force_validate(self, node, val):
        self._force_validate = val
        for child in [ch for ch in self.get_children() if ch != node]:
            for n in child.traverse():
                if isinstance(n.content, XSDChoice):
                    if n.min_occurrences != 0 and not n.chosen_child and [ch for ch in n.get_children() if ch.min_occurrences != 0]:
                        n.requirements_not_fulfilled = True
                    break
                if isinstance(n.content, XSDSequence) and n.min_occurrences == 0:
                    break
                if isinstance(n.content, XSDSequence) and n.min_occurrences != 0 and not (isinstance(n.get_parent().content, XSDGroup) and
                                                                                          n.get_parent().min_occurrences == 0):
                    n._force_validate = val

    def __repr__(self):
        return f"XMLChildContainer:{self.compact_repr} {self.get_coordinates_in_tree()}"

    def __copy__(self):
        copied = self.__class__(content=copy.copy(self.content), min_occurrences=self.min_occurrences,
                                max_occurrences=self.max_occurrences,
                                populate_children=False)
        for child in self.get_children():
            copied.add_child(child.__copy__())

        return copied


class XMLChildContainerFactory:
    def __init__(self, complex_type):
        self._child_container = None
        self._create_child_container(complex_type)

    def _create_child_container(self, complex_type):
        if 'XSDComplexType' not in [cls.__name__ for cls in complex_type.__mro__]:
            raise TypeError
        if not complex_type.get_xsd_indicator():
            raise XMLChildContainerFactoryError(f'complex_type {complex_type} has no xsd_indicator.')
        child_container = XMLChildContainer(*complex_type.get_xsd_indicator())
        self._child_container = child_container

    def get_child_container(self):
        return self._child_container
