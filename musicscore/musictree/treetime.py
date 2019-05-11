from musicscore.musictree.exceptions import MusicTreeError
from musicscore.musicxml.types.complextypes.attributes import Time, SenzaMisura, Beats, BeatType


class TreeTime(Time):

    def __init__(self, *time_signatures, **kwargs):
        super().__init__(**kwargs)
        self._force_show = False
        self._force_hide = False
        self.pars_arguments(time_signatures)

    @property
    def force_show(self):
        return self._force_show

    @force_show.setter
    def force_show(self, value):
        if not isinstance(value, bool):
            raise TypeError('force_show.value must be of type bool not{}'.format(type(value)))

        self._force_show = value

    @property
    def force_hide(self):
        return self._force_hide

    @force_hide.setter
    def force_hide(self, value):
        if not isinstance(value, bool):
            raise TypeError('force_hide.value must be of type bool not{}'.format(type(value)))
        self._force_hide = value

    @property
    def values(self):
        return [child.value for child in self.get_children() if isinstance(child, Beats) or isinstance(child, BeatType)]

    def pars_arguments(self, time_signatures):
        if len(time_signatures) == 1 and time_signatures[0] == 'senza_misura':
            self.add_child(SenzaMisura())

        elif len(time_signatures) % 2 == 0:

            for time_signature in zip(time_signatures[0::2], time_signatures[1::2]):
                self.set_time_signature(time_signature)
        else:
            raise MusicTreeError(
                'TreeTime can have senza_misura or (beats, beat_type)* as arguments not {}'.format(time_signatures))

    def set_time_signature(self, time_signature):
        (beats, beat_type) = time_signature
        self.add_child(Beats(beats))
        permitted = (1, 2, 4, 8, 16, 32, 64)
        if beat_type not in permitted:
            raise MusicTreeError('beat_type {} must be in {}'.format(beats, permitted))
        else:
            self.add_child(BeatType(beat_type))

    def get_time_signatures(self):
        if self.get_children_by_type(SenzaMisura):
            return []
        else:
            return list(zip(self.get_children_by_type(Beats), self.get_children_by_type(BeatType)))

    def __copy__(self):
        new_time = TreeTime()
        for key, new_key in zip(self.__dict__.keys(), new_time.__dict__.keys()):
            item = self.__dict__[key]
            if key == '_attributes':
                new_time.__dict__[new_key] = item
        for xml_child in self.get_children():
            new_time.add_child(xml_child.__copy__())

        return new_time
