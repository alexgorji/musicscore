from typing import Optional, List

from musictree.quarterduration import QuarterDuration
from musictree.util import isinstance_as_string
from tree.tree import Tree


class MusicTree(Tree):
    """
    MusicTree is the parent class of all music tree objects:
        - Score (root)
        - Part (1st layer)
        - Measure (2nd layer)
        - Staff (3rd layer)
        - Voice (4th layer)
        - Beat (5th layer)
        - Chord (6th layer)
        - Note (7th layer)
        - Midi (8th layer)
          Midi can represent a pitch or a rest (value=0) and controls accidental sign of the pitch if necessary.
        - Accidental (9th layer)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._possible_subdivisions = {}

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

    def _check_child_to_be_added(self, child):
        if not isinstance_as_string(child, 'MusicTree'):
            raise TypeError(f'MusicTree child must be of type MusicTree not {child.__class__}')

        parent_child = {'Score': 'Part', 'Part': 'Measure', 'Measure': 'Staff', 'Staff': 'Voice', 'Voice': 'Beat', 'Beat': 'Chord',
                        'Chord': 'Note', 'Note': 'Midi', 'Midi': 'Accidental', 'C': 'Accidental', 'D': 'Accidental', 'E': 'Accidental',
                        'F': 'Accidental', 'G': 'Accidental', 'A': 'Accidental', 'B': 'Accidental'}

        try:
            if not isinstance_as_string(child, parent_child[self.__class__.__name__]):
                raise TypeError(f'{self.__class__.__name__} accepts only children of type {parent_child[self.__class__.__name__]} not '
                                f'{child.__class__.__name__}')
        except KeyError:
            raise NotImplementedError(f'{self.__class__.__name__} add_child() not implemented.')

    def _get_beat_quarter_duration(self):
        if isinstance_as_string(self, 'Beat'):
            beat_quarter_duration = self.quarter_duration
        else:
            beat_quarter_duration = QuarterDuration(1)
        return beat_quarter_duration

    def get_beat(self, *args, **kwargs) -> 'Beat':
        """
        This method can be used for :obj:`~musictree.score.Score` and :obj:`~musictree.part.Part`, :obj:`~musictree.measure.Measure` and
        :obj:`~musictree.staff.Staff` and :obj:`~musictree.voice.Voice`

        :param args: can be used instead of ``kwargs``. A mixture of args and kwargs is not allowed.
        :param kwargs: ``part_number``, ``measure_number``, ``staff_number``, ``voice_number``, ``beat_number`` depending on
                       musictree's class. A :obj:`~musictree.staff.Staff` for example needs ``voice_number`` and ``beat_number`` while a
                       :obj:`~musictree.score.Score` needs all keyword arguments.
        :rtype: :obj:`~musictree.beat.Beat`
        """
        if isinstance_as_string(self, 'Voice'):
            kwargs = self._check_args_kwargs(args, kwargs, 'Voice', 'Beat')
            try:
                return self.get_children()[kwargs['beat_number'] - 1]
            except IndexError:
                return None
        raise TypeError

    def get_chord(self, *args, **kwargs) -> 'Chord':
        """
        This method can be used for :obj:`~musictree.score.Score` and :obj:`~musictree.part.Part`, :obj:`~musictree.measure.Measure` and
        :obj:`~musictree.staff.Staff`, :obj:`~musictree.voice.Voice` and :obj:`~musictree.beat.Beat`

        :param args: can be used instead of ``kwargs``. A mixture of args and kwargs is not allowed.
        :param kwargs: ``part_number``, ``measure_number``, ``staff_number``, ``voice_number``, ``beat_number``, ``chord_number`` depending on
                       musictree's class. A :obj:`~musictree.staff.Staff` for example needs ``voice_number``, ``beat_number`` and
                       ``chord_number`` while a :obj:`~musictree.score.Score` needs all keyword arguments.
        :rtype: :obj:`~musictree.chord.Chord`
        """
        if isinstance_as_string(self, 'Beat'):
            kwargs = self._check_args_kwargs(args, kwargs, 'Beat', 'Chord')
            try:
                return self.get_children()[kwargs['chord_number'] - 1]
            except IndexError:
                return None
        raise TypeError

    def get_chords(self) -> List['Chord']:
        """
        :return: a flat list of all chords.
        :rtype: List[:obj:`~musictree.chord.Chord`]
        """
        if isinstance_as_string(self, 'Beat'):
            return self.get_children()
        else:
            return [ch for child in self.get_children() for ch in child.get_chords()]

    def get_measure(self, *args, **kwargs) -> 'Measure':
        """
        This method can be used for :obj:`~musictree.score.Score` and :obj:`~musictree.part.Part`

        :param args: can be used instead of ``kwargs``. A mixture of args and kwargs is not allowed.
        :param kwargs: ``part_number``, ``measure_number`` depending on musictree's class.
        :rtype: :obj:`~musictree.measure.Measure`
        """
        if isinstance_as_string(self, 'Part'):
            kwargs = self._check_args_kwargs(args, kwargs, 'Part', 'Measure')
            try:
                return self.get_children()[kwargs['measure_number'] - 1]
            except IndexError:
                return None
        raise TypeError

    def get_part(self, *args, **kwargs) -> 'Part':
        """
        This method can be used for :obj:`~musictree.score.Score`

        :param args: can be used instead of ``kwargs``. A mixture of args and kwargs is not allowed.
        :param kwargs: ``part_number``.
        :rtype: :obj:`~musictree.part.Part`
        """
        if isinstance_as_string(self, 'Score'):
            kwargs = self._check_args_kwargs(args, kwargs, 'Score', 'Part')
            try:
                return self.get_children()[kwargs['part_number'] - 1]
            except IndexError:
                return None
        raise TypeError

    def get_possible_subdivisions(self, beat_quarter_duration: Optional[QuarterDuration] = None) -> List[int]:
        """
        This method is used by :obj:`~musictree.beat.Beat`'s :obj:`~musictree.beat.Beat.quantize()`.

        Possible subdivisions dictionary can be set with :obj:`~musictree.core.MusicTree.set_possible_subdivisions()`.

        If it is not set or ``beat_quarter_duration`` as key does not exist, the parent's possible subdivisions dictionary will be checked.

        :obj:`~musictree.score.Score` has a default :obj:`~musictree.score.POSSIBLE_SUBDIVISIONS` dictionary which will be used if no other
        musictree node on the path from self to root has its own possilbe subdivisions dictionary set with ``beat_quarter_duration`` as a
        key. For setting possible subdivisions dictionary use always :obj:`~musictree.core.MusicTree.set_possible_subdivisions()`.

        :param beat_quarter_duration: Used as key in possible subdivisions dictionary.
               If ``None`` and self is a :obj:`~musictree.beat.Beat` ``self.quarter_duration`` is used.
               If ``None`` and self is not a :obj:`~musictree.beat.Beat` it is set to 1.
        :return: A list of possible subdivisions of a :obj:`~musictree.beat.Beat`. This is used by beat's
                 :obj:`~musictree.beat.Beat.quantize()`
        :rtype: List[int]
        """
        if beat_quarter_duration is None:
            beat_quarter_duration = self._get_beat_quarter_duration()
        subdivisions = self._possible_subdivisions.get(beat_quarter_duration)
        if subdivisions is None and self.up is not None and self.up.get_possible_subdivisions(beat_quarter_duration) is not None:
            subdivisions = self.up.get_possible_subdivisions(beat_quarter_duration)[:]
        return subdivisions

    def get_staff(self, *args, **kwargs) -> 'Staff':
        """
        This method can be used for :obj:`~musictree.score.Score`, :obj:`~musictree.part.Part` and :obj:`~musictree.measure.Measure`

        :param args: can be used instead of ``kwargs``. A mixture of args and kwargs is not allowed.
        :param kwargs: ``part_number``, ``measure_number``, ``staff_number`` depending on musictree's class.
        :rtype: :obj:`~musictree.staff.Staff`
        """
        if isinstance_as_string(self, 'Measure'):
            kwargs = self._check_args_kwargs(args, kwargs, 'Measure', 'Staff')
            try:
                return self.get_children()[kwargs['staff_number'] - 1]
            except IndexError:
                return None
        raise TypeError

    def get_voice(self, *args, **kwargs) -> 'Voice':
        """
        This method can be used for :obj:`~musictree.score.Score` and :obj:`~musictree.part.Part`, :obj:`~musictree.measure.Measure` and
        :obj:`~musictree.staff.Staff`

        :param args: can be used instead of ``kwargs``. A mixture of args and kwargs is not allowed.
        :param kwargs: ``part_number``, ``measure_number``, ``staff_number``, ``voice_number`` depending on musictree's class.
        :rtype: :obj:`~musictree.voice.Voice`
        """
        if isinstance_as_string(self, 'Staff'):
            kwargs = self._check_args_kwargs(args, kwargs, 'Staff', 'Voice')
            try:
                return self.get_children()[kwargs['voice_number'] - 1]
            except IndexError:
                return None
        raise TypeError

    def set_possible_subdivisions(self, subdivisions: list[int], beat_quarter_duration: Optional[QuarterDuration] = None) -> None:
        """
        This method is used to set or change possible subdivisions dictionary.

        :param subdivisions: list of possible subdivisions to be used duration :obj:`musictree.beat.Beat.quantize()`
        :param beat_quarter_duration: If ``None`` and self is a :obj:`~musictree.beat.Beat` ``self.quarter_duration`` is used.
                                      If ``None`` and self is not a :obj:`~musictree.beat.Beat` it is set to 1.
        :return: None
        """
        if beat_quarter_duration is None:
            beat_quarter_duration = self._get_beat_quarter_duration()
        elif isinstance_as_string(self, 'Beat') and beat_quarter_duration != self.quarter_duration:
            raise ValueError(
                f"beat_quarter_duration '{beat_quarter_duration}' must be None or equal to the beat quarter_duration '{self.quarter_duration}'")

        if not isinstance(beat_quarter_duration, QuarterDuration):
            beat_quarter_duration = QuarterDuration(beat_quarter_duration)
        try:
            subdivisions = list(subdivisions)
        except TypeError:
            subdivisions = [subdivisions]
        self._possible_subdivisions[beat_quarter_duration] = subdivisions
