from musicscore.musictree.treeinstruments import TreeInstrument
from musicscore.musictree.treepart import TreePart
from musicscore.musicxml.types.complextypes.namedisplay import DisplayText
from musicscore.musicxml.types.complextypes.partgroup import GroupNameDisplay, GroupSymbol, GroupBarline
from musicscore.musicxml.types.complextypes.partlist import ScorePart, PartGroup

from musicscore.musicxml.types.complextypes.scorepart import PartName, PartAbbreviation


class TreeScorePart(ScorePart):

    def __init__(self, id, instrument=None, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)
        self.add_child(PartName(name='none', print_object='no'))

        self._forbidden_divisions = None
        self._instrument = None
        self._max_division = None
        self._number_of_staves = None
        self._parts = []

        self.instrument = instrument
        self.parent_score = None

    # // public properties
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

    @property
    def instrument(self):
        return self._instrument

    @instrument.setter
    def instrument(self, val):
        if val is not None and not isinstance(val, TreeInstrument):
            raise TypeError('instrument.value must be of type TreeInstrument not{}'.format(type(val)))
        self._instrument = val
        if val is not None:
            if self.number_of_staves is None and val.number_of_staves is not None:
                self.number_of_staves = val.number_of_staves
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
    def number_of_staves(self):
        return self._number_of_staves

    @number_of_staves.setter
    def number_of_staves(self, val):
        if not isinstance(val, int):
            raise TypeError('number_of_staves.value must be of type int not{}'.format(type(val)))
        self._number_of_staves = val
        for part in self._parts:
            part.staves = val

    @property
    def part_abbreviation(self):
        try:
            return self.get_children_by_type(PartAbbreviation)[0]
        except IndexError:
            return None

    @property
    def part_name(self):
        try:
            return self.get_children_by_type(PartName)[0]
        except IndexError:
            return None

    # //public methods

    # add
    def add_part(self, part=None):
        if not part:
            part = TreePart(id=self.id)
        else:
            if part.id != self.id:
                raise ValueError('Part must have the same id as TreeScorePart')
        part.parent_score_part = self
        if self.number_of_staves is not None:
            part.staves = self.number_of_staves
        self._parts.append(part)
        return part

    def add_part_group(self, number, type, name=None, symbol=None, barline=None):
        pg = PartGroup(type=type, number=str(number))
        pg._up = self.up
        if name:
            gnd = pg.add_child(GroupNameDisplay())
            gnd.add_child(DisplayText(name))
        if symbol:
            pg.add_child(GroupSymbol(symbol))
        if barline:
            pg.add_child(GroupBarline(barline))
        self_index = self.up.current_children.index(self)
        if type == 'start':
            self.up.current_children.insert(self_index, pg)
        else:
            self.up.current_children.insert(self_index + 1, pg)

    # get
    def get_parts(self):
        return self._parts
