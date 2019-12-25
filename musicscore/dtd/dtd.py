import warnings

from musicscore.tree.tree import Tree


class DTDError(Exception):
    def __init__(self, msg='DTD Error'):
        super().__init__(msg)


class ChildTypeDTDConflict(DTDError):
    def __init__(self, child, parent):
        msg = 'child of type {} cannot be added to {} due to DTD Type conflicts'.format(type(child), parent.__class__)
        super().__init__(msg)


class ChildOccurrenceDTDConflict(DTDError):
    def __init__(self, child, parent):
        msg = 'child of type {} cannot be added to {} due to DTD Occurrence conflicts'.format(type(child),
                                                                                              parent.__class__)
        super().__init__(msg)


class ChildIsNotOptional(DTDError):
    def __init__(self, node, parent):
        msg = 'child of type {} is due to DTD Occurrence not optional for {}'.format(node.type_.__name__,
                                                                                     parent.__class__)
        super().__init__(msg)


class DTDConflict(DTDError):
    def __init__(self, msg=None):
        if msg is None:
            msg = 'DTD conflicts exist'
        super().__init__(msg)


class DTDTree(Tree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DTDNode(DTDTree):
    def __init__(self, children=None, min_occurrence=1, max_occurrence=1, *args, **kwargs):
        super().__init__(**kwargs)
        self.choices = None
        self._min_occurrence = None
        self._max_occurrence = None
        self._choice_index = 0
        self._current_choice = None
        self._xml_children = None
        self.min_occurrence = min_occurrence
        self.max_occurrence = max_occurrence

        if children is None:
            children = []
        for child in children:
            if not isinstance(child, DTDTree):
                raise TypeError(
                    '{} can only have children of Type DTDTree not {}'.format(self.__class__.__name__, type(child)))
            self.add_child(child)

    @property
    def min_occurrence(self):
        return self._min_occurrence

    @min_occurrence.setter
    def min_occurrence(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('min_occurrence.value must be of type None or positive int not {}'.format(type(value)))
        if value is not None and value < 0:
            raise ValueError('min_occurrence.value must be positive'.format(type(value)))
        self._min_occurrence = value

    @property
    def max_occurrence(self):
        return self._max_occurrence

    @max_occurrence.setter
    def max_occurrence(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('max_occurrence.value must be of type None or positive int not {}'.format(type(value)))
        if value is not None and value < 0:
            raise ValueError('max_occurrence.value must be positive'.format(type(value)))
        self._max_occurrence = value

    @property
    def xml_children(self):
        if not self._xml_children:
            self._xml_children = []
        return self._xml_children

    def __repr__(self):
        if isinstance(self, Element):
            return '{} type {} at {}'.format(self.__class__.__name__, self.type_.__name__, hex(id(self)))
        return '{} at {}'.format(self.__class__.__name__, hex(id(self)))

    def copy_child(self, child, ch=None):
        if isinstance(child, Element):
            copied = child.no_child_copy(child.type_)
        else:
            copied = child.no_child_copy()

        copied.original = child
        copied.choice = ch
        return copied

    def eliminate_group_reference(self):

        for node in self.traverse():
            if isinstance(node, GroupReference):
                if len(node.get_children()) > 1:
                    warnings.warn(
                        'dtd.eliminate_group_reference: group has more than one child! Only the first child will be '
                        'replaced.')
                new_node = node.get_children()[0]
                if (new_node.min_occurrence, new_node.max_occurrence) != (1, 1):
                    warnings.warn('dtd.eliminate_group_reference: groups child occurrences are not 1.')
                (new_node.min_occurrence, new_node.max_occurrence) = (node.min_occurrence, node.max_occurrence)
                node.replace_node(new_node)

    def carbon_copy(self):
        if isinstance(self, Element):
            copied = Element(self.type_)
        else:
            copied = self.__class__()

        copied.original = self.original
        copied.choice = self.choice
        (copied.min_occurrence, copied.max_occurrence) = (self.min_occurrence, self.max_occurrence)
        for child in self.get_children():
            copied.add_child(child.carbon_copy())

        return copied

    def generate_dtd_choices(self):
        self.eliminate_group_reference()

        self.choices = [self.copy_child(self)]
        choice_index = 0

        while choice_index < len(self.choices):
            current_choice = self.choices[choice_index]
            current_choice.magic_expand(self.choices)
            choice_index += 1

    def get_choices(self):
        if not self.choices:
            self.generate_dtd_choices()
        return self.choices

    def remove_xml_child(self, xml_child):
        for node in self.traverse():
            if xml_child in node.xml_children:
                node.xml_children.remove(xml_child)

    def get_xml_children(self):
        xml_children = []
        pregnant_nodes = []

        for leaf in self.traverse_leaves():
            if isinstance(leaf.up, Choice) and (leaf.up.min_occurrence, leaf.up.max_occurrence) == (0, None):
                if leaf.up not in pregnant_nodes:
                    pregnant_nodes.append(leaf.up)
            else:
                pregnant_nodes.append(leaf)
        for node in pregnant_nodes:
            xml_children.extend(node.xml_children)
        return xml_children


class DTDLeaf(DTDNode):
    def __init__(self, type_, min_occurrence=1, max_occurrence=1, *args, **kwargs):
        super().__init__(min_occurrence=min_occurrence, max_occurrence=max_occurrence, *args, **kwargs)
        self._type = None
        self.type_ = type_

    @property
    def type_(self):
        return self._type

    @type_.setter
    def type_(self, value):
        if not isinstance(value, type):
            raise TypeError('type_.value must be of type type not{}'.format(type(value)))
        self._type = value

    def add_child(self, child):
        raise Exception('DTDLeaf can have no children')


class Choice(DTDNode):
    """"""

    def __init__(self, *children, min_occurrence=1, max_occurrence=1):
        super().__init__(children=children, min_occurrence=min_occurrence, max_occurrence=max_occurrence)

    def magic_expand(self, dtd_choices):
        if not self.original:
            raise Exception('is not copied')

        if (self.min_occurrence, self.max_occurrence) == (1, 1):
            if self.choice is None:
                for index, child in enumerate(self.original.get_children()):
                    if index == 0:
                        copied = self.copy_child(child, index)
                        self.add_child(copied)
                        self.choice = 0
                        copied.magic_expand(dtd_choices)
                    else:
                        new_choice = self.get_root().carbon_copy()
                        new_choice.goto(self.index).choice = index
                        new_choice.goto(self.index)._children = []
                        dtd_choices.append(new_choice)
            else:
                if not self.get_children():
                    copied = self.copy_child(self.original.get_children()[self.choice])
                    self.add_child(copied)
                    copied.magic_expand(dtd_choices)
                else:
                    self.get_children()[0].magic_expand(dtd_choices)
        else:
            for child in self.original.get_children():
                child_exists = False
                for ch in self.get_children():
                    if ch.original == child:
                        child_exists = True
                        ch.magic_expand(dtd_choices)
                        break

                if not child_exists:
                    copied = self.copy_child(child)
                    self.add_child(copied)
                    copied.magic_expand(dtd_choices)


class Sequence(DTDNode):
    """"""

    def __init__(self, *children, min_occurrence=1, max_occurrence=1):
        super().__init__(children=children, min_occurrence=min_occurrence, max_occurrence=max_occurrence)

    def magic_expand(self, dtd_choices):
        if not self.original:
            raise Exception('is not a copy')
        for child in self.original.get_children():
            child_exists = False
            for ch in self.get_children():
                if ch.original == child:
                    child_exists = True
                    ch.magic_expand(dtd_choices)
                    break

            if not child_exists:
                copied = self.copy_child(child)
                self.add_child(copied)
                copied.magic_expand(dtd_choices)


class Element(DTDLeaf):
    """"""

    def __init__(self, type_, min_occurrence=1, max_occurrence=1, **kwargs):
        super().__init__(type_, min_occurrence=min_occurrence, max_occurrence=max_occurrence, **kwargs)

    def magic_expand(self, dtd_choices):
        pass

    def __deepcopy__(self):
        return Element(type_=self.type_, min_occurrence=self.min_occurrence, max_occurrence=self.max_occurrence)

    def check_min_occurrence(self):
        if len(self.xml_children) >= self.min_occurrence:
            return True

        if isinstance(self.up, Choice) and self.up.min_occurrence == 0:
            return True

        if isinstance(self.up, Sequence) and self.up.min_occurrence == 0:
            siblings = [child for child in self.up.get_children() if child != self]
            for sibling in siblings:
                if sibling._xml_children:
                    return False
            return True

        if self.up.min_occurrence != 1:
            raise NotImplementedError('check_min_occurrence')
        else:
            return False

    def add_xml_child(self, xml_child):
        if not isinstance(xml_child, self.type_):
            raise DTDError('{} is of wrong type and cannot be added to {}'.format(xml_child, self))

        if isinstance(self.up, Choice) and (self.up.min_occurrence, self.up.max_occurrence) == (0, None):
            self.up.xml_children.append(xml_child)
            xml_child.node = self.up
            return True

        elif self.max_occurrence is None or len(self.xml_children) < self.max_occurrence:
            self.xml_children.append(xml_child)
            xml_child.node = self
            return True

        elif self.up.max_occurrence != 1:
            if isinstance(self.up, Sequence):
                return False
            else:
                # self.up.xml_children.append(xml_child)
                # xml_child.node = self.up
                self.xml_children.append(xml_child)
                xml_child.node = self
                return True
                # raise NotImplementedError()

        else:
            return False


class GroupReference(DTDNode):
    """"""

    def __init__(self, child, min_occurrence=1, max_occurrence=1):
        super().__init__(children=[child.__deepcopy__()], min_occurrence=min_occurrence, max_occurrence=max_occurrence)

    @property
    def child(self):
        return self.get_children()[0]

    def __deepcopy__(self):
        return GroupReference(self.child.__deepcopy__(), min_occurrence=self.min_occurrence,
                              max_occurrence=self.max_occurrence)
