from musicscore.musictree.treeinstruments import TreeInstrument
from musicscore.musictree.treepart import TreePart
from musicscore.musicxml.types.complextypes.partlist import ScorePart
import uuid

from musicscore.musicxml.types.complextypes.scorepart import PartName, PartAbbreviation


class TreeScorePart(ScorePart):
    """"""

    def __init__(self, id, instrument=None, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)
        self.add_child(PartName(name='none', print_object='no'))
        self._instrument = None
        self.instrument = instrument
        self._max_division = None
        self._forbidden_divisions = None
        self._parts = []
        self.parent_score = None
        # self.add_child(PartAbbreviation())
        # self._part_name = None
        # self._part_abbreviation = None

    @property
    def part_name(self):
        try:
            return self.get_children_by_type(PartName)[0]
        except IndexError:
            return None

    @property
    def part_abbreviation(self):
        try:
            return self.get_children_by_type(PartAbbreviation)[0]
        except IndexError:
            return None

    @property
    def instrument(self):
        return self._instrument

    @instrument.setter
    def instrument(self, val):
        if val is not None and not isinstance(val, TreeInstrument):
            raise TypeError('instrument.value must be of type TreeInstrument not{}'.format(type(val)))
        self._instrument = val
        if val is not None:
            val.id = self.id
            if self.part_name is not None:
                self.remove_child(self.part_name)
            self.add_child(self.instrument.part_name)

            if self.part_abbreviation is not None:
                self.remove_child(self.part_abbreviation)
            self.add_child(self.instrument.part_abbreviation)

    @property
    def max_division(self):
        if self._max_division is None:
            self._max_division = self.parent_score.max_division
        return self._max_division

    @max_division.setter
    def max_division(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('max_division.value must be None or of type int not {}'.format(type(value)))

        self._max_division = value

    @property
    def forbidden_divisions(self):
        if self._forbidden_divisions is None:
            self._forbidden_divisions = self.parent_score.forbidden_divisions

        return self._forbidden_divisions

    @forbidden_divisions.setter
    def forbidden_divisions(self, value):
        if value is not None:
            for x in value:
                if not isinstance(x, int):
                    raise TypeError('forbidden_division must be of type int not{}'.format(type(value)))

        self._forbidden_divisions = value

    def get_parts(self):
        return self._parts

    def add_part(self, part=None):
        if not part:
            part = TreePart(id=self.id)
        else:
            if part.id != self.id:
                raise ValueError('Part must have the same id as TreeScorePart')
        part.parent_score_part = self
        self._parts.append(part)
        return part
