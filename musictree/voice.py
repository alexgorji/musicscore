from typing import Optional, Union, List

from musictree.beat import Beat
from musictree.exceptions import VoiceHasNoBeatsError, VoiceHasNoParentError, VoiceIsAlreadyFullError
from musictree.core import MusicTree
from musictree.finalupdate_mixin import FinalUpdateMixin
from musictree.xmlwrapper import XMLWrapper
from musicxml.xmlelement.xmlelement import XMLVoice

__all__ = ['Voice']


class Voice(MusicTree, FinalUpdateMixin, XMLWrapper):
    _ATTRIBUTES = {'number', '_chords', '_current_beat', 'leftover_chord', 'is_filled', '_final_updated'}
    _ATTRIBUTES = _ATTRIBUTES.union(MusicTree._ATTRIBUTES)
    XMLClass = XMLVoice

    def __init__(self, number=None, *args, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(value_='1', *args, **kwargs)
        self._number = None
        self.number = number
        self._current_beat = None
        self._leftover_chord = None
        self._final_updated = False

    @property
    def is_filled(self) -> bool:
        """
        :return: ``True`` if voice has :obj:`~musictree.beat.Beat` children and the last child is filled, else ``False``
        """
        if self.get_children():
            return self.get_children()[-1].is_filled
        else:
            return False

    @property
    def leftover_chord(self) -> Optional['Chord']:
        """
        :return: None or a :obj:`~musictree.chord.Chord` which is left over after adding a chord to the voice.
        """
        return self._leftover_chord

    @leftover_chord.setter
    def leftover_chord(self, val):
        self._leftover_chord = val

    @property
    def number(self) -> Optional[int]:
        """
        :type: None or int. If None number is set to 1.
        :return: positive int or None
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

    @XMLWrapper.xml_object.getter
    def xml_object(self) -> XMLClass:
        return super().xml_object

    def add_beat(self, beat_quarter_duration: Optional[Union['QuarterDuration', 'Fraction', int, float]] = 1) -> Beat:
        """
        Creates and adds a :obj:`~musictree.beat.Beat` to voice

        :param beat_quarter_duration: if None beat_quarter_duration is set to 1.
        :return: :obj:`~musictree.beat.Beat`
        """
        if beat_quarter_duration is None:
            beat_quarter_duration = 1
        return self.add_child(Beat(beat_quarter_duration))

    def add_child(self, child: Beat) -> Beat:
        """
        Check and add child to list of children. Child's parent is set to self.

        :param child: :obj:`~musictree.beat.Beat`
        :return: child
        :rtype: :obj:`~musictree.beat.Beat`
        """
        if not self.up:
            raise VoiceHasNoParentError('A child Beat can only be added to a Voice if voice has a Staff parent.')
        return super().add_child(child)

    def add_chord(self, chord: 'Chord') -> List['Chord']:
        """
        :param chord: :obj:`~musictree.chord.Chord`, required
        :return: added chord or a list of split chords
        """
        if not self.get_children():
            raise VoiceHasNoBeatsError
        if self.get_current_beat() is None:
            raise VoiceIsAlreadyFullError(f'Voice number {self.value_} of Measure number {self.up.up.number} is full.')
        return self.get_current_beat().add_child(chord)

    def get_children(self) -> List[Beat]:
        """
        :return: list of added children.
        :rtype: List[:obj:`~musictree.beat.Beat`]
        """
        return super().get_children()

    def get_parent(self) -> 'Staff':
        """
        :return: parent
        :rtype: :obj:`~musictree.staff.Staff`
        """
        return super().get_parent()

    def get_current_beat(self) -> Beat:
        """
        :return: First not filled child :obj:`~musictree.beat.Beat`
        """
        if not self.get_children():
            raise ValueError('Voice has no beats.')
        else:
            for beat in self.get_children():
                if not beat.is_filled:
                    return beat

    def update_beats(self, *quarter_durations) -> Optional[List[Beat]]:
        """
        Creates and adds or replaces Beats.

        :param quarter_durations: if None and a measure as ancestor exists, this measure's
                                  :obj:`musictree.time.Time.get_beats_quarter_durations()` method is called.
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
