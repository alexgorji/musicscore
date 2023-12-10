from typing import Optional, Union, List

from musicscore.beat import Beat
from musicscore.chord import GraceChord, Chord
from musicscore.exceptions import VoiceHasNoBeatsError, VoiceHasNoParentError, VoiceIsFullError, \
    AddChordError, AlreadyFinalizedError
from musicscore.musictree import MusicTree
from musicscore.finalize import FinalizeMixin
from musicscore.quantize import QuantizeMixin
from musicscore.xmlwrapper import XMLWrapper
from musicxml.xmlelement.xmlelement import XMLVoice

__all__ = ['Voice']


class Voice(MusicTree, QuantizeMixin, FinalizeMixin, XMLWrapper):
    """
    Parent type: :obj:`~musicscore.staff.Staff`

    Child type: :obj:`~musicscore.beat.Beat`
    """
    _ATTRIBUTES = {'number', 'leftover_chord', 'is_filled'}
    _ATTRIBUTES = _ATTRIBUTES.union(MusicTree._ATTRIBUTES)
    _ATTRIBUTES = _ATTRIBUTES.union(QuantizeMixin._ATTRIBUTES)
    XMLClass = XMLVoice

    def __init__(self, number=None, *args, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(value_='1', *args, **kwargs)
        self._number = None
        self.number = number
        self._current_beat_index = None
        self._leftover_chord = None
        self._final_updated = False

    def _add_chord(self, chord: 'Chord') -> List['Chord']:
        """
        :param chord: :obj:`~musicscore.chord.Chord`, required
        :return: added chord or a list of split chords
        """
        if not self.get_children():
            raise VoiceHasNoBeatsError

        try:
            current_beat = self.get_children()[self.get_current_beat_index()]
        except IndexError:
            raise VoiceIsFullError(f'Voice number {self.value_} of Measure number {self.up.up.number} is full.')

        if isinstance(chord, GraceChord) and chord.position == 'after':
            return current_beat.add_child(chord)

        if current_beat.is_filled:
            self._current_beat_index += 1
            return self._add_chord(chord)
        else:
            return current_beat.add_child(chord)

    @property
    def is_filled(self) -> bool:
        """
        :return: ``True`` if voice has :obj:`~musicscore.beat.Beat` children and the last child is filled, else ``False``
        """
        if self.get_children():
            return self.get_children()[-1].is_filled
        else:
            return False

    @property
    def leftover_chord(self) -> Optional['Chord']:
        """
        :return: None or a :obj:`~musicscore.chord.Chord` which is left over after adding a chord to the voice.
        """
        return self._leftover_chord

    @leftover_chord.setter
    def leftover_chord(self, val):
        self._leftover_chord = val

    @property
    def number(self) -> Optional[int]:
        """
        :type: ``None`` or ``int``. If ``None`` number is set to 1.
        :return: ``positive int`` or ``None``
        """
        if self._number is None:
            return None
        object_value = self.xml_object.value_
        if object_value is not None:
            return int(object_value)

    @number.setter
    def number(self, val):
        self._number = val
        if val is not None:
            self.xml_object.value_ = str(val)
        else:
            self.xml_object.value_ = '1'

    def add_beat(self, beat_quarter_duration: Optional[Union['QuarterDuration', 'Fraction', int, float]] = 1) -> Beat:
        """
        Creates and adds a :obj:`~musicscore.beat.Beat` to voice

        :param beat_quarter_duration: if None beat_quarter_duration is set to 1.
        :return: :obj:`~musicscore.beat.Beat`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_beat')
        if beat_quarter_duration is None:
            beat_quarter_duration = 1
        return self.add_child(Beat(beat_quarter_duration))

    def add_chord(self, *args, **kwargs):
        raise AddChordError()

    def add_child(self, child: Beat) -> Beat:
        """
        Check and add child to list of children. Child's parent is set to self.

        :param child: :obj:`~musicscore.beat.Beat`
        :return: child
        :rtype: :obj:`~musicscore.beat.Beat`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_child')
        if not self.up:
            raise VoiceHasNoParentError('A child Beat can only be added to a Voice if voice has a Staff parent.')
        return super().add_child(child)

    def fill_with_rests(self):
        if not self.is_filled:
            if not self.get_children():
                self.update_beats()
            self._add_chord(Chord(0, sum([b.quarter_duration for b in self.get_beats()]) - sum([ch.quarter_duration for ch in self.get_chords()])))

    def get_current_beat(self) -> 'Beat':
        """
        :return: First not completely filled child of type :obj:`~musicscore.beat.Beat`
        :exception: :obj:`~musicscore.exceptions.VoiceIsFullError` is raised if all beats are already filled.
        """
        try:
            current_beat = self.get_children()[self.get_current_beat_index()]
        except IndexError:
            raise VoiceIsFullError()
        if current_beat.is_filled:
            self._current_beat_index += 1
            return self.get_current_beat()
        return current_beat

    def get_current_beat_index(self) -> int:
        """
        :return: Index of first not completely filled child of type :obj:`~musicscore.beat.Beat`
        """
        if not self.get_children():
            raise ValueError('Voice has no beats.')
        else:
            if not self._current_beat_index:
                self._current_beat_index = 0
        return self._current_beat_index

    def update_beats(self, *quarter_durations) -> Optional[List[Beat]]:
        """
        Creates and adds or replaces Beats.

        :param quarter_durations: if None and a measure as ancestor exists, this measure's
                                  :obj:`musicscore.time.Time.get_beats_quarter_durations()` method is called.
        :return: None if quarter_durations is None and no measures as ancestor exists, else list of created beats.
        """
        if not quarter_durations:
            if self.up and self.up.up:
                quarter_durations = self.up.up.time.get_beats_quarter_durations()
            else:
                return
        else:
            if len(quarter_durations) == 1 and hasattr(quarter_durations[0], '__iter__'):
                quarter_durations = quarter_durations[0]

        self.remove_children()

        for quarter_duration in quarter_durations:
            self.add_child(Beat(quarter_duration))
        return self.get_children()
