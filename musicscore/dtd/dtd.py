from musicscore.tree.tree import Tree


class ChildTypeDTDConflict(Exception):
    def __init__(self, child):
        msg = 'child of type {} cannot be added due to DTD Type conflicts'.format(type(child))
        super().__init__(msg)


class ChildOccurrenceDTDConflict(Exception):
    def __init__(self, child):
        msg = 'child of type {} cannot be added due to DTD Occurrence conflicts'.format(type(child))
        super().__init__(msg)


class ChildIsNotOptional(Exception):
    def __init__(self, node):
        msg = 'child of type {} is due to  DTD Occurrence not optional'.format(node.type_)
        super().__init__(msg)


class DTDTree(Tree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DTDNode(DTDTree):
    def __init__(self, children=[], min_occurrence=1, max_occurrence=1, *args, **kwargs):
        super().__init__(**kwargs)
        self._min_occurrence = None
        self._max_occurrence = None
        self.min_occurrence = min_occurrence
        self.max_occurrence = max_occurrence
        self._possibility_index = 0
        for child in children:
            if not isinstance(child, DTDTree):
                raise TypeError(
                    '{} can only have children of Type DTDTree not {}'.format(self.__class__.__name__, type(child)))
            if isinstance(child, type(self)):
                raise TypeError('{} can not have children of its own Type'.format(self.__class__.__name__))
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

    def expand(self):
        return self

    def next(self):
        try:
            self._possibility_index += 1
            return self.expand()[self._possibility_index]

        except IndexError:
            raise StopIteration()

    def get_current_combination(self):
        return self.expand()[self._possibility_index]

    def get_current_node(self, child):
        return self.get_current_combination()[
            [node.type_ for node in self.get_current_combination()].index(type(child))]

    def check_max_occurrence(self, occurrence):
        if self.max_occurrence is not None and occurrence > self.max_occurrence:
            return False
        return True

    def check_child_type(self, parent, child):
        while type(child) not in [node.type_ for node in self.get_current_combination()]:
            try:
                self.next()
                for sibling in parent.get_children():
                    try:
                        self.check_child_type(parent, sibling)
                    except ChildTypeDTDConflict:
                        raise ChildTypeDTDConflict(child)
            except StopIteration:
                raise ChildTypeDTDConflict(child)

    def check_child_max_occurrence(self, parent, child):
        occurrence = len(parent.get_children_by_type(type(child)))
        dtd_node = self.get_current_node(child)
        while dtd_node.check_max_occurrence(occurrence + 1) is False:
            try:
                self.next()
                for sibling in parent.get_children():
                    try:
                        self.check_child_max_occurrence(parent, sibling)
                    except ChildOccurrenceDTDConflict:
                        raise ChildOccurrenceDTDConflict(child)
            except StopIteration:
                raise ChildOccurrenceDTDConflict(child)
            dtd_node = self.get_current_node(child)

    def sort_children(self, xmltree):
        current_combination = self.get_current_combination()
        new_children = []
        for node in current_combination:
            if not isinstance(node.up, Sequence):
                raise Exception('node.up is of type {} and not Sequence'.format(type(node.up)))
            new_children.extend(xmltree.get_children_by_type(node.type_))
        xmltree._children = new_children

    def close(self, xmltree):
        current_combination = self.get_current_combination()

        for node in current_combination:
            selected = xmltree.get_children_by_type(node.type_)
            if len(selected) == 0 and node.min_occurrence != 0:
                raise ChildIsNotOptional(node)


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

    def expand(self):
        if (self.min_occurrence, self.max_occurrence) == (1, 1):
            if not self.get_children():
                return []
            else:
                x = self.get_children()[0]
                xs = self.get_children()[1:]
                ex = x.expand()
                exs = Choice(*xs).expand()
                return ex + exs
        elif (self.min_occurrence, self.max_occurrence) == (0, None):
            if not self.get_children():
                return [[]]
            else:
                x = self.get_children()[0]
                xs = self.get_children()[1:]
                ex = x.expand()
                exs = Sequence(*xs).expand()
                return [a + b for a in ex for b in exs]
        else:
            raise ValueError(
                'Choice with min_occurrence {} and max_occurrence {} is not valid'.format(self.min_occurrence,
                                                                                          self.max_occurrence))


class Sequence(DTDNode):
    """"""

    def __init__(self, *children):
        super().__init__(children=children, min_occurrence=1, max_occurrence=1)

    def expand(self):
        if not self.get_children():
            return [[]]
        else:
            x = self.get_children()[0]
            xs = self.get_children()[1:]
            ex = x.expand()
            exs = Sequence(*xs).expand()
            return [a + b for a in ex for b in exs]


class Element(DTDLeaf):
    """"""

    def __init__(self, type_, min_occurrence=1, max_occurrence=1, **kwargs):
        super().__init__(type_, min_occurrence=min_occurrence, max_occurrence=max_occurrence, **kwargs)

    def expand(self):
        return [[self]]


class Group(DTDLeaf):
    """"""

    def __init__(self, type_, min_occurrence=1, max_occurrence=1, *args, **kwargs):
        super().__init__(type_, min_occurrence=min_occurrence, max_occurrence=max_occurrence, *args, **kwargs)

    def expand(self):
        return [[self]]
