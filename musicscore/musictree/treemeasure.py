from musicscore.musictree.treepart import TreePart
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
                    self._time.reset_dtd()
                    self._time.pars_arguments(value)
                else:
                    self._time = TreeTime(*value)
        else:
            self._time = None

    def show_time_signature(self):
        part = self.get_children_by_type(TreePart)[0]
        part.attributes.add_child(self.time)

    def hide_time_signature(self):
        part = self.get_children_by_type(TreePart)[0]
        if self.time in part.attributes.get_children():
            part.attributes.remove_child(self.time)

    def get_part(self, number):
        return self.get_children_by_type(TreePart)[number - 1]

    def __copy__(self):
        time = self.time.__copy__()
        new_measure = TreeMeasure(time)
        for key, new_key in zip(self.__dict__.keys(), new_measure.__dict__.keys()):
            item = self.__dict__[key]
            if key == '_attributes':
                new_measure.__dict__[new_key] = item
        return new_measure
