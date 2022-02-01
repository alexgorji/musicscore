from musicxml.xmlelement.xmlelement import XMLPart, XMLScorePart

from musictree.exceptions import IdHasAlreadyParentOfSameTypeError, IdWithSameValueExistsError
from musictree.musictree import MusicTree
from musictree.xmlwrapper import XMLWrapper


class Id:
    __refs__ = []

    def __init__(self, value):
        self._parents = []
        self._value = None
        self.value = value
        self.__refs__.append(self)

    @classmethod
    def _check_value(cls, val):
        for obj in cls.__refs__:
            if obj.value == val:
                raise IdWithSameValueExistsError

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._check_value(val)
        self._value = val
        for parent in self.get_parents():
            self.update_parents_id(parent)

    def delete(self):
        if self in self.__refs__:
            self.__refs__.remove(self)
        del self

    def update_parents_id(self, parent):
        parent.xml_object.id = self.value

    def add_parent(self, obj):
        if obj.__class__ in [type(parent) for parent in self.get_parents()]:
            raise IdHasAlreadyParentOfSameTypeError()
        self._parents.append(obj)
        self.update_parents_id(obj)

    def get_parents(self):
        return self._parents

    def __repr__(self):
        return f"{self.__class__}:{self.value} at {id(self)}"

    def __del__(self):
        if self in self.__refs__:
            self.__refs__.remove(self)


class ScorePart(XMLWrapper):
    _ATTRIBUTES = {'part'}

    def __init__(self, part, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLScorePart(*args, **kwargs)
        self._part = None
        self.part = part

    @property
    def part(self):
        return self._part

    @part.setter
    def part(self, val):
        if not isinstance(val, Part):
            raise TypeError
        self._part = val
        if self in self.part.id_.get_parents():
            self.part.id_.update_parents_id(self)
        else:
            self.part.id_.add_parent(self)
        self._update_name()

    def _update_name(self):
        self.xml_object.xml_part_name = self.part.name


class Part(MusicTree, XMLWrapper):
    _ATTRIBUTES = {'id_', 'name', '_score_part'}

    def __init__(self, id, name=None, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLPart(*args, **kwargs)
        self._id = None
        self.id_ = id
        self._name = None
        self.name = name
        self._score_part = ScorePart(part=self)

    @property
    def id_(self):
        return self._id

    @id_.setter
    def id_(self, val):
        if isinstance(val, Id):
            self._id = val
        elif isinstance(self._id, Id):
            self._id.value = val
        else:
            self._id = Id(val)
        if self in self.id_.get_parents():
            self.id_.update_parents_id(self)
        else:
            self.id_.add_parent(self)

    @property
    def name(self):
        if self._name is not None:
            return self._name
        else:
            return self.id

    @name.setter
    def name(self, val):
        self._name = val
        try:
            self.score_part._update_name()
        except AttributeError:
            pass

    @property
    def score_part(self):
        return self._score_part

    def add_child(self, child):
        super().add_child(child)
        self.xml_object.add_child(child.xml_object)
        return child
