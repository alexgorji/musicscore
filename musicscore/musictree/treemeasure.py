from musicscore.musictree.treepart import Part
from musicscore.musictree.treetime import TreeTime
from musicscore.musicxml.elements import timewise as timewise


class TreeMeasure(timewise.Measure):
    """"""

    def __init__(self, time=(4, 4), *args, **kwargs):
        super().__init__(number='1', *args, **kwargs)
        self._time = None
        self.time = time

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
                    self._time._children = []
                    self._time.pars_arguments(value)
                else:
                    self._time = TreeTime(*value)
        else:
            self._time = None

    def show_time_signature(self):
        part = self.get_children_by_type(Part)[0]
        part.attributes.add_child(self.time)

    def hide_time_signature(self):
        part = self.get_children_by_type(Part)[0]
        part.attributes.remove_child(self.time)

    def __copy__(self):
        new_measure = TreeMeasure()
        for key, new_key in zip(self.__dict__.keys(), new_measure.__dict__.keys()):
            item = self.__dict__[key]
            if key == '_attributes':
                new_measure.__dict__[new_key] = item
            elif key == '_time':
                new_measure.__dict__[new_key] = item.__copy__()
        return new_measure
