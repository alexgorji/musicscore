from quicktions import Fraction

from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treetime import TreeTime
from musicscore.musicxml.elements import timewise as timewise
from musicscore.musicxml.elements.barline import Barline, BarStyle
from musicscore.musicxml.groups.layout import SystemLayout
from musicscore.musicxml.groups.musicdata import Print, Attributes
from musicscore.musicxml.types.complextypes.systemlayout import SystemDistance


class TreeMeasure(timewise.Measure):
    """"""

    def __init__(self, time=(4, 4), *args, **kwargs):
        super().__init__(number='1', *args, **kwargs)
        self._time = None
        self.time = time
        self._beats = None
        self._offset = None
        self._barline_style = None

    # properties

    @property
    def barline_style(self):
        return self._barline_style

    @property
    def next(self):
        return self.next_sibling

    @property
    def offset(self):
        if self._offset is None:
            self.update_offset()
        return self._offset

    @property
    def previous(self):
        if not self.up:
            return None
        index = self.up.get_children_by_type(TreeMeasure).index(self)
        if index == 0:
            return None
        return self.up.get_children_by_type(TreeMeasure)[index - 1]

    @property
    def quarter_duration(self):
        output = 0
        for time_signature in self.time.get_time_signatures():
            (beats, beat_type) = time_signature
            output += beats.value / beat_type.value * 4
        return Fraction(output).limit_denominator(10000)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if value:
            if isinstance(value, TreeTime):
                self._time = value
            else:
                if isinstance(self._time, TreeTime):
                    self._time.reset_dtd()
                    self._time.pars_arguments(value)
                else:
                    self._time = TreeTime(*value)
        else:
            self._time = None

    @property
    def __name__(self):
        index = self.up.get_children_by_type(self.__class__).index(self)
        return str(index + 1)

    # // private methods

    def _add_page_one(self):
        score = self.up

        first_part = score.get_measure(1).get_part(1)

        first_part.get_children_by_type(TreePart)
        try:
            print_ = first_part.get_children_by_type(Print)[0]
        except IndexError:
            print_ = first_part.add_child(Print())
        print_.page_number = '1'

    # // public methods
    # gets

    def get_part(self, number):
        return self.get_children_by_type(TreePart)[number - 1]

    def get_part_with_id(self, id):
        try:
            return [part for part in self.get_children_by_type(TreePart) if part.id == id][0]
        except IndexError:
            raise AttributeError('measure {} has no part with id {}'.format(self, id))

    def get_beats(self):
        output = []
        for part in self.get_children_by_type(TreePart):
            output.extend(part.get_beats())
        return output

    # sets
    def set_barline_style(self, value):
        if value:
            for part in self.get_children_by_type(TreePart):
                try:
                    bl = part.get_children_by_type(Barline)[0]
                except IndexError:
                    bl = part.add_child(Barline())

                try:
                    bs = bl.get_children_by_type(BarStyle)[0]
                    bs.value = value
                except IndexError:
                    bs = bl.add_child(BarStyle(value))

        self._barline_style = value

    # adds

    def add_page_break(self):

        score = self.up

        if not score._identifications_added:
            score._add_identifications()

        self._add_page_one()

        for part in self.get_children_by_type(TreePart):
            try:
                p = part.get_children_by_type(Print)[0]
            except IndexError:
                p = part.add_child(Print())
            p.new_page = 'yes'

    def add_system_break(self):
        score = self.up
        if not score._identifications_added:
            score._add_identifications()

        for part in self.get_children_by_type(TreePart):
            try:
                p = part.get_children_by_type(Print)[0]
            except IndexError:
                p = part.add_child(Print())
            p.new_system = 'yes'

    def add_system_distance(self, value):
        for part in self.get_children_by_type(TreePart):
            try:
                p = part.get_children_by_type(Print)[0]
            except IndexError:
                p = part.add_child(Print())

            try:
                s = p.get_children_by_type(SystemLayout)[0]
            except IndexError:
                s = p.add_child(SystemLayout())

            try:
                sd = s.get_children_by_type(SystemDistance)[0]
            except IndexError:
                sd = s.add_child(SystemDistance())

            sd.value = value

    # others
    def show_time_signature(self):
        for part in self.get_children_by_type(TreePart):
            part.get_children_by_type(Attributes)[0].add_child(self.time)

    def hide_time_signature(self):
        part = self.get_children_by_type(TreePart)[0]
        if self.time in part.get_children_by_type(Attributes)[0].get_children():
            part.get_children_by_type(Attributes)[0].remove_child(self.time)

    def update_offset(self):
        if self.previous:
            output = self.previous.offset + self.previous.quarter_duration
            self._offset = output
        else:
            self._offset = 0

    # // copy
    def __copy__(self):
        time = self.time.__copy__()
        new_measure = TreeMeasure(time)
        for key, new_key in zip(self.__dict__.keys(), new_measure.__dict__.keys()):
            item = self.__dict__[key]
            if key == '_attributes':
                new_measure.__dict__[new_key] = item
        return new_measure
