from typing import List

from musicscore.exceptions import MusicTreeTypeError
from musicscore.util import isinstance_as_string
from tree.tree import Tree

__all__ = ['MusicTree']


class MusicTree(Tree):
    """
    MusicTree is the parent class of all music tree objects:
        - :obj:`~musicscore.score.Score` (root)
        - :obj:`~musicscore.part.Part` (1st layer)
        - :obj:`~musicscore.measure.Measure` (2nd layer)
        - :obj:`~musicscore.staff.Staff` (3rd layer)
        - :obj:`~musicscore.voice.Voice` (4th layer)
        - :obj:`~musicscore.beat.Beat` (5th layer)
        - :obj:`~musicscore.chord.Chord`, :obj:`~musicscore.chord.Rest` or :obj:`~musicscore.chord.GraceChord` (6th layer)
        - :obj:`~musicscore.note.Note` (7th layer)
        - :obj:`~musicscore.midi.Midi` (8th layer)
          Midi can represent a pitch or a rest (value=0) and controls accidental sign of the pitch if necessary.
        - :obj:`~musicscore.accidental.Accidental` (9th layer)
    """
    _ATTRIBUTES = {'show_accidental_signs'}

    default_show_accidental_signs = 'modern'  #: Class attribute of :obj:`~musicscore.musictree.MusicTree`

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._show_accidental_signs = None

    @staticmethod
    def _check_args_kwargs(args, kwargs, class_name, get_class_name=None):
        for x in args:
            if not isinstance(x, int) or x < 1:
                raise TypeError(f'args {args} must be positive integers')
        for x in kwargs.values():
            if not isinstance(x, int) or x < 1:
                raise TypeError(f'kwargs values {kwargs} must be positive integers')

        def _get_default_keys():
            default_keys = ['part_number', 'measure_number', 'staff_number', 'voice_number', 'beat_number',
                            'chord_number']
            class_names = ['Score', 'Part', 'Measure', 'Staff', 'Voice', 'Beat', 'Chord']
            class_index = class_names.index(class_name)
            get_class_index = -1 if not get_class_name else class_names.index(get_class_name)
            return default_keys[class_index:get_class_index]

        default_keys = _get_default_keys()
        if args and kwargs:
            raise ValueError('Both args and kwargs cannot be set')
        if args:
            if len(args) != len(default_keys):
                raise ValueError(f'Wrong number of args {args}. Keys are: {default_keys}')
            kwargs = {key: value for key, value in zip(default_keys, args)}
        else:
            keys = kwargs.keys()
            if set(keys) != set(default_keys[:len(keys)]):
                raise ValueError(
                    f'Wrong (number) of keys: {list(keys)} in kwargs. All Keys: {default_keys} must be set.')
        return kwargs

    def _check_child_to_be_added(self, child):
        if not isinstance_as_string(child, 'MusicTree'):
            raise MusicTreeTypeError(f'MusicTree child must be of type MusicTree not {child.__class__}')

        parent_child = {'Score': 'Part', 'Part': 'Measure', 'Measure': 'Staff', 'Staff': 'Voice', 'Voice': 'Beat',
                        'Beat': 'Chord', 'GraceChord': 'Note', 'Rest': 'Note',
                        'Chord': 'Note', 'Note': 'Midi', 'Midi': 'Accidental', 'C': 'Accidental', 'D': 'Accidental',
                        'E': 'Accidental',
                        'F': 'Accidental', 'G': 'Accidental', 'A': 'Accidental', 'B': 'Accidental'}

        try:
            if not isinstance_as_string(child, parent_child[self.__class__.__name__]):
                raise MusicTreeTypeError(
                    f'{self.__class__.__name__} accepts only children of type {parent_child[self.__class__.__name__]} not '
                    f'{child.__class__.__name__}')
        except KeyError:
            raise NotImplementedError(f'{self.__class__.__name__} add_child() not implemented.')

    def _get_kwargs(self, args_, kwargs_, get_class_name):
        if isinstance_as_string(self, 'Score'):
            return self._check_args_kwargs(args_, kwargs_, 'Score', get_class_name)
        elif isinstance_as_string(self, 'Part'):
            return self._check_args_kwargs(args_, kwargs_, 'Part', get_class_name)
        elif isinstance_as_string(self, 'Measure'):
            return self._check_args_kwargs(args_, kwargs_, 'Measure', get_class_name)
        elif isinstance_as_string(self, 'Staff'):
            return self._check_args_kwargs(args_, kwargs_, 'Staff', get_class_name)
        elif isinstance_as_string(self, 'Voice'):
            return self._check_args_kwargs(args_, kwargs_, 'Voice', get_class_name)
        elif isinstance_as_string(self, 'Beat'):
            return self._check_args_kwargs(args_, kwargs_, 'Beat', get_class_name)
        elif isinstance_as_string(self, 'Chord'):
            return self._check_args_kwargs(args_, kwargs_, 'Chord', get_class_name)
        else:
            raise MusicTreeTypeError(f'MusicTree descendents of type {self.__class__} cannot use this method.')

    def _get_music_tree_descendent(self, args, kwargs, get_class_name):
        kwargs = self._get_kwargs(args, kwargs, get_class_name)

        if not kwargs:
            raise TypeError

        if len(kwargs) == 1:
            try:
                return self.get_children()[list(kwargs.values())[0] - 1]
            except IndexError:
                return None
        else:
            output = self
            for key in kwargs:
                string_to_eval = f"output.get_{key.split('_')[0]}(kwargs['{key}'])"
                output = eval(string_to_eval)
                if not output:
                    return None
            return output

    @property
    def show_accidental_signs(self) -> str:
        """
        :obj:`~musicscore.musictree.MusicTree` property

        - If show_accidental_signs is set to None the first get_quantized of ancestors which is ``False`` or ``True`` will be returned.
        - If :obj:`~musicscore.score.Score.show_accidental_signs` is set to None it will be converted to ``default_show_accidental_signs``
        - Possible show_accidental_signs are: None, 'modern', 'traditional'

        :type: Optional[str]
        :rtype: str
        """
        if self._show_accidental_signs is None:
            if self.up:
                return self.up.show_accidental_signs
            else:
                return self.default_show_accidental_signs
        return self._show_accidental_signs

    @show_accidental_signs.setter
    def show_accidental_signs(self, val):
        permitted = [None, 'modern', 'traditional']
        if val not in permitted:
            raise ValueError(f'show_accidental_signs {val} not in permitted: {permitted}')

        self._show_accidental_signs = val

    def get_beat(self, *args, **kwargs) -> 'Beat':
        """
        :obj:`~musicscore.musictree.MusicTree` method

        This method can be used for :obj:`~musicscore.score.Score` and :obj:`~musicscore.part.Part`, :obj:`~musicscore.measure.Measure` and
        :obj:`~musicscore.staff.Staff` and :obj:`~musicscore.voice.Voice`

        :param args: can be used instead of ``kwargs``. A mixture of args and kwargs is not allowed.
        :param kwargs: ``part_number``, ``measure_number``, ``staff_number``, ``voice_number``, ``beat_number`` depending on
                       musicscore's class. A :obj:`~musicscore.staff.Staff` for example needs ``voice_number`` and ``beat_number`` while a
                       :obj:`~musicscore.score.Score` needs all keyword arguments.
        :rtype: :obj:`~musicscore.beat.Beat`
        """
        return self._get_music_tree_descendent(args, kwargs, 'Beat')

    def get_chord(self, *args, **kwargs) -> 'Chord':
        """
        :obj:`~musicscore.musictree.MusicTree` method

        This method can be used for :obj:`~musicscore.score.Score` and :obj:`~musicscore.part.Part`, :obj:`~musicscore.measure.Measure`,
        :obj:`~musicscore.staff.Staff`, :obj:`~musicscore.voice.Voice` and :obj:`~musicscore.beat.Beat`

        :param args: can be used instead of ``kwargs``. A mixture of args and kwargs is not allowed.
        :param kwargs: ``part_number``, ``measure_number``, ``staff_number``, ``voice_number``, ``beat_number``, ``chord_number`` depending on
                       musicscore's class. A :obj:`~musicscore.staff.Staff` for example needs ``voice_number``, ``beat_number`` and
                       ``chord_number`` while a :obj:`~musicscore.score.Score` needs all keyword arguments.
        :rtype: :obj:`~musicscore.chord.Chord`
        """

        return self._get_music_tree_descendent(args, kwargs, 'Chord')

    def get_beats(self) -> List['Beat']:
        """
        :obj:`~musicscore.musictree.MusicTree` method

        This method can be used for :obj:`~musicscore.score.Score` and :obj:`~musicscore.part.Part`, :obj:`~musicscore.measure.Measure`,
        :obj:`~musicscore.staff.Staff` and :obj:`~musicscore.voice.Voice`.

        :return: a flat list of all beats.
        :rtype: List[:obj:`~musicscore.beat.Beat`]
        """
        if isinstance_as_string(self, 'Voice'):
            return self.get_children()
        else:
            output = [ch for child in self.get_children() for ch in child.get_beats()]
            if not output:
                for cls_name in ['Beat', 'Chord', 'Note', 'Midi', 'Accidental']:
                    if isinstance_as_string(self, cls_name):
                        raise MusicTreeTypeError(
                            f'MusicTree descendents of type {self.__class__} cannot use this method.')
            return output

    def get_chords(self) -> List['Chord']:
        """
        :obj:`~musicscore.musictree.MusicTree` method

        This method can be used for :obj:`~musicscore.score.Score` and :obj:`~musicscore.part.Part`, :obj:`~musicscore.measure.Measure` and
        :obj:`~musicscore.staff.Staff`, :obj:`~musicscore.voice.Voice` and :obj:`~musicscore.beat.Beat`

        :return: a flat list of all chords.
        :rtype: List[:obj:`~musicscore.chord.Chord`]
        """
        if isinstance_as_string(self, 'Beat'):
            return self.get_children()
        else:
            output = [ch for child in self.get_children() for ch in child.get_chords()]
            if not output:
                for cls_name in ['Chord', 'Note', 'Midi', 'Accidental']:
                    if isinstance_as_string(self, cls_name):
                        raise MusicTreeTypeError(
                            f'MusicTree descendents of type {self.__class__} cannot use this method.')
            return output

    def get_measure(self, *args, **kwargs) -> 'Measure':
        """
        :obj:`~musicscore.musictree.MusicTree` method

        This method can be used for :obj:`~musicscore.score.Score` and :obj:`~musicscore.part.Part`

        :param args: can be used instead of ``kwargs``. A mixture of args and kwargs is not allowed.
        :param kwargs: ``part_number``, ``measure_number`` depending on musicscore's class.
        :rtype: :obj:`~musicscore.measure.Measure`
        """

        return self._get_music_tree_descendent(args, kwargs, 'Measure')

    def get_part(self, *args, **kwargs) -> 'Part':
        """
        :obj:`~musicscore.musictree.MusicTree` method

        This method can be used for :obj:`~musicscore.score.Score`

        :param args: can be used instead of ``kwargs``. A mixture of args and kwargs is not allowed.
        :param kwargs: ``part_number``.
        :rtype: :obj:`~musicscore.part.Part`
        """

        return self._get_music_tree_descendent(args, kwargs, 'Part')

    def get_staff(self, *args, **kwargs) -> 'Staff':
        """
        :obj:`~musicscore.musictree.MusicTree` method

        This method can be used for :obj:`~musicscore.score.Score`, :obj:`~musicscore.part.Part` and :obj:`~musicscore.measure.Measure`

        :param args: can be used instead of ``kwargs``. A mixture of args and kwargs is not allowed.
        :param kwargs: ``part_number``, ``measure_number``, ``staff_number`` depending on musicscore's class.
        :rtype: :obj:`~musicscore.staff.Staff`
        """

        return self._get_music_tree_descendent(args, kwargs, 'Staff')

    def get_voice(self, *args, **kwargs) -> 'Voice':
        """
        :obj:`~musicscore.musictree.MusicTree` method

        This method can be used for :obj:`~musicscore.score.Score` and :obj:`~musicscore.part.Part`, :obj:`~musicscore.measure.Measure` and
        :obj:`~musicscore.staff.Staff`

        :param args: can be used instead of ``kwargs``. A mixture of args and kwargs is not allowed.
        :param kwargs: ``part_number``, ``measure_number``, ``staff_number``, ``voice_number`` depending on musicscore's class.
        :rtype: :obj:`~musicscore.voice.Voice`
        """
        return self._get_music_tree_descendent(args, kwargs, 'Voice')
