from musicscore.musicxml.types.simple_type import PositiveInteger
from musicscore.tree.tree import Tree


class DTDTree(Tree):
    def __init__(self, *args, **kwargs):
        # print('inititalizing {} {}'.format('DTDTree', self))
        super().__init__(*args, **kwargs)


class DTDNode(DTDTree):
    def __init__(self, children=[], min_occurrence=1, max_occurrence=1, *args, **kwargs):
        # print('inititalizing {} {}'.format('DTDNode', self))
        super().__init__(**kwargs)
        self._min_occurrence = None
        self._max_occurrence = None
        self.min_occurrence = min_occurrence
        self.max_occurrence = max_occurrence
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

    # def get_possibilities(self):
    #     output = []
    #     if isinstance(self, Choice) and self.min_occurrence == 1 and self.max_occurrence == 1:
    #         output


class DTDLeaf(DTDNode):
    def __init__(self, type_, min_occurrence=1, max_occurrence=1, *args, **kwargs):
        # print('inititalizing {} {} type {}'.format('DTDLeaf', self, type_.__name__))
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

    # _current_siblings = []
    # def get_siblings(self):
    #     # upwards
    #     parent = self.up
    #     if isinstance(parent, Sequence):
    #         self._current_siblings.extend(parent.get_children())
    #     elif isinstance(parent, Choice):
    #         if parent.min_occurrence == 1 and parent.max_occurrence == 1:
    #             pass


class Choice(DTDNode):
    """"""

    def __init__(self, *children, min_occurrence=1, max_occurrence=1):
        # print('inititalizing {} {}'.format('Choice', self))
        super().__init__(children=children, min_occurrence=min_occurrence, max_occurrence=max_occurrence)

    def expand(self):
        if not self.get_children():
            return []
        else:
            x = self.get_children()[0]
            xs = self.get_children()[1:]
            ex = x.expand()
            exs = Choice(*xs).expand()
            return ex + exs


class Sequence(DTDNode):
    """"""

    def __init__(self, *children):
        # print('inititalizing {} {} with children {}'.format('Sequence', self, children))
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
        # print('inititalizing {} {} type {}'.format('Element', self, type_.__name__))
        super().__init__(type_, min_occurrence=min_occurrence, max_occurrence=max_occurrence, **kwargs)

    def expand(self):
        return [[self]]


class Group(DTDLeaf):
    """"""

    def __init__(self, type_, min_occurrence=1, max_occurrence=1, *args, **kwargs):
        # print('inititalizing {} {} type {}'.format('Group', self, type_.__name__))
        super().__init__(type_, min_occurrence=min_occurrence, max_occurrence=max_occurrence, *args, **kwargs)

    def expand(self):
        return [[self]]