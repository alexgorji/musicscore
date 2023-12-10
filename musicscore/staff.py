from typing import Optional, Set

from musicscore.clef import Clef
from musicscore.exceptions import StaffHasNoParentError, AlreadyFinalizedError, AddChordError
from musicscore.finalize import FinalizeMixin
from musicscore.musictree import MusicTree
from musicscore.quantize import QuantizeMixin
from musicscore.voice import Voice
from musicscore.xmlwrapper import XMLWrapper
from musicxml.xmlelement.xmlelement import XMLStaff

__all__ = ['Staff']


class Staff(MusicTree, QuantizeMixin, FinalizeMixin, XMLWrapper):
    """
    Parent type: :obj:`~musicscore.measure.Measure`

    Child type: :obj:`~musicscore.voice.Voice`
    """
    _ATTRIBUTES = {'clef', 'default_clef', 'number'}
    _ATTRIBUTES = _ATTRIBUTES.union(MusicTree._ATTRIBUTES)
    _ATTRIBUTES = _ATTRIBUTES.union(QuantizeMixin._ATTRIBUTES)
    XMLClass = XMLStaff

    def __init__(self, number=None, clef=None, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(value_=1, **kwargs)
        self._number = None
        self._clef = None
        self.clef = clef
        self.number = number

    @property
    def clef(self) -> Clef:
        """
        :type: :obj:`~musicscore.clef.Clef`
        :return: Clef associated with the staff.
        :rtype: :obj:`~musicscore.clef.Clef`
        """
        if not self._clef:
            if self.get_previous_staff() and self.get_previous_staff().clef:
                self._clef = self.get_previous_staff().clef.__copy__()
                self._clef.show = False
        return self._clef

    @clef.setter
    def clef(self, val):
        if val is not None and not isinstance(val, Clef):
            raise TypeError
        if val and not val.number and self.clef:
            val.number = self.clef.number
        self._clef = val

    @property
    def number(self):
        """
        :type: None or int. If None number is set to 1.
        :return: positive int or None
        """
        if self._number is not None:
            return self.xml_object.value_
        else:
            return self._number

    @number.setter
    def number(self, val):
        self._number = val
        if val is None:
            self.xml_object.value_ = 1
        else:
            self.xml_object.value_ = val

    def add_child(self, child: Voice) -> Voice:
        """
        - Adds a :obj:`~musicscore.voice.Voice` as child to staff.
        - If voice number is ``None``, it is determined as length of children + 1.
        - If voice number is already set an is not equal to length of children + 1. a ``ValueError`` is raised.
        - If Staff has no parent :obj:`~musicscore.measure.Measure` a :obj:`~musicscore.exceptions.StaffHasNoParentError` is raised.
        - After adding voice its :obj:`~musicscore.voice.Voice.update_beats()` is called.

        :param child: :obj:`~musicscore.voice.Voice` , required
        :return: added :obj:`~musicscore.voice.Voice`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_child')
        self._check_child_to_be_added(child)

        if not self.up:
            raise StaffHasNoParentError('A child Voice can only be added to a Staff if staff has a Measure parent.')

        if child.number is not None and child.number != len(self.get_children()) + 1:
            raise ValueError(f'Voice number must be None or {len(self.get_children()) + 1}')
        if child.number is None:
            child.number = len(self.get_children()) + 1
        else:
            child.number = len(self.get_children()) + 1

        child._parent = self
        self._children.append(child)

        return child

    def add_chord(self, *args, **kwargs):
        raise AddChordError()

    def add_voice(self, voice_number: Optional[int] = None) -> Voice:
        """
        - Creates and adds a new :obj:`~musicscore.voice.Voice` object as child to staff.
        - If voice number is greater than length of children + 1 all missing voices are created and added first.

        :param voice_number: positive int or None. If ``None`` voice number is determined as length of children + 1.
        :return: new :obj:`~musicscore.voice.Voice`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_voice')
        if voice_number is None:
            voice_number = len(self.get_children()) + 1

        voice_object = self.get_voice(voice_number=voice_number)

        if voice_object is None:
            for _ in range(voice_number - len(self.get_children())):
                voice_object = self.add_child(Voice())
                voice_object.update_beats()
            return voice_object

        voice_object.update_beats()
        return voice_object

    def fill_with_rests(self):
        for voice in self.get_children():
            voice.fill_with_rests()

    def get_previous_staff(self) -> Optional['Staff']:
        """
        :return: :obj:`Staff` with the same number in previous :obj:`~musicscore.measure.Measure` if existing else ``None``
        """
        if self.up and self.up.previous:
            my_index = self.up.get_children().index(self)
            try:
                return self.up.previous.get_children()[my_index]
            except IndexError:
                return None
        return None

    def get_last_pitch_steps_with_accidentals(self) -> Set[str]:
        """
        :return: A set of pitch steps with not natural accidental. This method is used to keep track of accidental signs which needs to
                 be shown hidden.
        :rtype:  Set[str]
        """
        output = set()
        for v in self.get_children():
            if v.get_chords():
                last_chord = v.get_chords()[-1]
                if not last_chord.is_rest:
                    for m in last_chord.midis:
                        if m.accidental.sign != 'natural':
                            step = m.accidental.get_pitch_parameters()[0]
                            if step not in output:
                                output.add(step)
        return output
