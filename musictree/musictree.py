from musictree.quarterduration import QuarterDuration
from musictree.util import isinstance_as_string
from tree.tree import Tree


class MusicTree(Tree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._possible_subdivisions = {}

    """
    MusicTree is the parent class of all music tree objects:
    Score (root)
    Part (1st layer)
    Measure (2nd layer)
    Staff (3rd layer)
    Voice (4th layer)
    Beat (5th layer)
    Chord (6th layer)
    Note (7th layer)
    Midi (8th layer)
    Midi can represent a pitch or a rest (value=0) and controls accidental sign of the pitch if necessary.
    Accidental (9th layer)
    """

    def _check_child_to_be_added(self, child):
        if not isinstance_as_string(child.__class__, 'MusicTree'):
            raise TypeError(f'MusicTree child must be of type MusicTree not {child.__class__}')

        parent_child = {'Score': 'Part', 'Part': 'Measure', 'Measure': 'Staff', 'Staff': 'Voice', 'Voice': 'Beat', 'Beat': 'Chord',
                        'Chord': 'Note', 'Note': 'Midi', 'Midi': 'Accidental'}

        try:
            if not isinstance_as_string(child.__class__, parent_child[self.__class__.__name__]):
                raise TypeError(f'{self.__class__.__name__} accepts only children of type {parent_child[self.__class__.__name__]} not '
                                f'{child.__class__.__name__}')
        except KeyError:
            raise NotImplementedError(f'{self.__class__.__name__} add_child() not implemented.')

    def _get_beat_quarter_duration(self):
        if isinstance_as_string(self.__class__, 'Beat'):
            beat_quarter_duration = self.quarter_duration
        else:
            beat_quarter_duration = QuarterDuration(1)
        return beat_quarter_duration

    def get_possible_subdivisions(self, beat_quarter_duration=None):
        if beat_quarter_duration is None:
            beat_quarter_duration = self._get_beat_quarter_duration()
        subdivisions = self._possible_subdivisions.get(beat_quarter_duration)
        if subdivisions is None and self.up is not None and self.up.get_possible_subdivisions(beat_quarter_duration) is not None:
            subdivisions = self.up.get_possible_subdivisions(beat_quarter_duration)[:]
        return subdivisions

    def set_possible_subdivisions(self, subdivisions, beat_quarter_duration=None):
        if beat_quarter_duration is None:
            beat_quarter_duration = self._get_beat_quarter_duration()
        elif isinstance_as_string(self.__class__, 'Beat') and beat_quarter_duration != self.quarter_duration:
            raise ValueError(
                f"beat_quarter_duration '{beat_quarter_duration}' must be None or equal to the beat quarter_duration '{self.quarter_duration}'")

        if not isinstance(beat_quarter_duration, QuarterDuration):
            beat_quarter_duration = QuarterDuration(beat_quarter_duration)
        try:
            subdivisions = list(subdivisions)
        except TypeError:
            subdivisions = [subdivisions]
        self._possible_subdivisions[beat_quarter_duration] = subdivisions

    @staticmethod
    def _check_args_kwargs(args, kwargs, class_name, get_class_name=None):
        def _get_default_keys():
            default_keys = ['part_number', 'measure_number', 'staff_number', 'voice_number', 'beat_number', 'chord_number']
            class_names = ['Score', 'Part', 'Measure', 'Staff', 'Voice', 'Beat', 'Chord']
            class_index = class_names.index(class_name)
            get_class_index = -1 if not get_class_name else class_names.index(get_class_name)
            return default_keys[class_index:get_class_index]

        default_keys = _get_default_keys()
        if args and kwargs:
            raise ValueError('Both args and kwargs cannot be set')
        if args:
            if len(args) != len(default_keys):
                raise ValueError('Wrong number of args.')
            kwargs = {key: value for key, value in zip(default_keys, args)}
        else:
            keys = kwargs.keys()
            if set(keys) != set(default_keys[:len(keys)]):
                raise ValueError('Wrong keys in kwargs.')
        return kwargs

    def get_part(self, *args, **kwargs):
        if isinstance_as_string(self.__class__, 'Score'):
            kwargs = self._check_args_kwargs(args, kwargs, 'Score', 'Part')
            try:
                return self.get_children()[kwargs['part_number'] - 1]
            except IndexError:
                return None
        raise TypeError

    def get_measure(self, *args, **kwargs):
        if isinstance_as_string(self.__class__, 'Part'):
            kwargs = self._check_args_kwargs(args, kwargs, 'Part', 'Measure')
            try:
                return self.get_children()[kwargs['measure_number'] - 1]
            except IndexError:
                return None
        raise TypeError

    def get_staff(self, *args, **kwargs):
        if isinstance_as_string(self.__class__, 'Measure'):
            kwargs = self._check_args_kwargs(args, kwargs, 'Measure', 'Staff')
            try:
                return self.get_children()[kwargs['staff_number'] - 1]
            except IndexError:
                return None
        raise TypeError

    def get_voice(self, *args, **kwargs):
        if isinstance_as_string(self.__class__, 'Staff'):
            kwargs = self._check_args_kwargs(args, kwargs, 'Staff', 'Voice')
            try:
                return self.get_children()[kwargs['voice_number'] - 1]
            except IndexError:
                return None
        raise TypeError

    def get_beat(self, *args, **kwargs):
        if isinstance_as_string(self.__class__, 'Voice'):
            kwargs = self._check_args_kwargs(args, kwargs, 'Voice', 'Beat')
            try:
                return self.get_children()[kwargs['beat_number'] - 1]
            except IndexError:
                return None
        raise TypeError

    def get_chord(self, *args, **kwargs):
        if isinstance_as_string(self.__class__, 'Beat'):
            kwargs = self._check_args_kwargs(args, kwargs, 'Beat', 'Chord')
            try:
                return self.get_children()[kwargs['chord_number'] - 1]
            except IndexError:
                return None
        raise TypeError

    def get_chords(self):
        if isinstance_as_string(self.__class__, 'Beat'):
            return self.get_children()
        else:
            return [ch for child in self.get_children() for ch in child.get_chords()]
