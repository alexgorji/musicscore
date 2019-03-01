from musicscore.musicxml.types.simple_type import PositiveInteger
from musicscore.tree.tree import Tree


class DTDTree(Tree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DTDNode(DTDTree):
    def __init__(self, *children, **kwargs):
        super().__init__(**kwargs)
        for child in children:
            if not isinstance(child, DTDTree):
                raise TypeError('{} can only have children of Type DTDTree not {}'.format(self.__class__.__name__, type(child)))
            if isinstance(child, type(self)):
                raise TypeError('{} can not have children of its own Type'.format(self.__class__.__name__))
            self.add_child(child)


class DTDLeaf(DTDNode):
    def __init__(self, type_, min_occurrence=1, max_occurrence=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._min_occurrence = None
        self._max_occurrence = None
        self.min_occurrence = min_occurrence
        self.max_occurrence = max_occurrence
        self._type = None
        self.type_ = type_

    @property
    def min_occurrence(self):
        return self._min_occurrence

    @min_occurrence.setter
    def min_occurrence(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('min_occurrence.value must be of type None or positive int not{}'.format(type(value)))
        if value is not None and value < 0:
            raise ValueError('min_occurrence.value must be positive'.format(type(value)))
        self._min_occurrence = value

    @property
    def max_occurrence(self):
        return self._max_occurrence

    @max_occurrence.setter
    def max_occurrence(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('max_occurrence.value must be of type None or positive int not{}'.format(type(value)))
        if value is not None and value < 0:
            raise ValueError('max_occurrence.value must be positive'.format(type(value)))
        self._max_occurrence = value

    @property
    def type_(self):
        return self._type_
        
    @type_.setter
    def type_(self, value):
        if not isinstance(value, type):
            raise TypeError('type_.value must be of type type not{}'.format(type(value)))
        self._type_ = value

    def add_child(self, child):
        raise Exception('DTDLeaf can have no children')


class Choice(DTDNode):
    """"""

    def __init__(self, *children, **kwargs):
        super().__init__(*children, **kwargs)


class Sequence(DTDNode):
    """"""

    def __init__(self, *children, **kwargs):
        super().__init__(*children, **kwargs)


class Element(DTDLeaf):
    """"""

    def __init__(self, type_, min_occurrence=1, max_occurrence=1, *args, **kwargs):
        super().__init__(type_, min_occurrence=min_occurrence, max_occurrence=max_occurrence, *args, **kwargs)


class Group(DTDLeaf):
    """"""

    def __init__(self, type_, min_occurrence=1, max_occurrence=1, *args, **kwargs):
        super().__init__(type_, min_occurrence=min_occurrence, max_occurrence=max_occurrence, *args, **kwargs)
