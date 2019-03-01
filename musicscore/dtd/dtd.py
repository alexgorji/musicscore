from musicscore.musicxml.types.simple_type import PositiveInteger
from musicscore.tree.tree import Tree


class DTDTree(Tree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DTDNode(Tree):
    def __init__(self, *children, **kwargs):
        super().__init__(**kwargs)
        for child in children:
            if not isinstance(child, DTDTree):
                raise TypeError('{} can only have children of Type DTDTee'.format(self.__class__.__name__))
            if isinstance(child, Sequence):
                raise TypeError('{} can not have children of its own Type DTDTee'.format(self.__class__.__name__))
            self.add_child(child)


class DTDLeaf(Tree):
    def __init__(self, min_occurrence=1, max_occurrence=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._min_occurrence = None
        self._max_occurrence = None
        self.min_occurrence = min_occurrence
        self.max_occurrence = max_occurrence

    @property
    def min_occurrence(self):
        return self._min_occurrence

    @min_occurrence.setter
    def min_occurrence(self, value):
        if value is not None and not isinstance(value, int) or value < 0:
            raise TypeError('min_occurrence.value must be of type None or positive int not{}'.format(type(value)))
        self._min_occurrence = value

    @property
    def max_occurrence(self):
        return self._max_occurrence

    @max_occurrence.setter
    def max_occurrence(self, value):
        if value is not None and not isinstance(value, int) or value < 0:
            raise TypeError('max_occurrence.value must be of type None or positive int not{}'.format(type(value)))
        self._max_occurrence = value

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

    def __init__(self, min_occurrence=1, max_occurrence=1, *args, **kwargs):
        super().__init__(min_occurrence=min_occurrence, max_occurrence=max_occurrence, *args, **kwargs)


class Group(DTDTree):
    """"""

    def __init__(self, min_occurrence=1, max_occurrence=1, *args, **kwargs):
        super().__init__(min_occurrence=min_occurrence, max_occurrence=max_occurrence, *args, **kwargs)
