from math import log2
from typing import Optional, Union, List

from musicxml.xmlelement.xmlelement import *  # type: ignore
from musicxml.xsd.xsdsimpletype import XSDSimpleTypeNoteheadValue  # type: ignore

from musictree.accidental import Accidental
from musictree.core import MusicTree

__all__ = ['Midi', 'MidiNote', 'C', 'D', 'E', 'F', 'G', 'A', 'B', 'midi_to_frequency', 'frequency_to_midi']


class Midi(MusicTree):
    """
    Midi is the representation of a Pitch with its midi value, and accidental sign. This object is used to create a Chord
    consisting of one or more pitches. The midi representation of a rest is a Midi object with value 0.
    """

    def __init__(self, value: Union[float, int], accidental: Optional[Accidental] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = None
        self._accidental = None
        self._pitch_or_rest = None
        self._parent_note = None

        self.value = value
        self.accidental = accidental

    def update_parent_note(self):
        if self.parent_note:
            self.parent_note._update_xml_pitch_or_rest()
            self.parent_note._update_xml_accidental()

    def _update_pitch_parameters(self):
        pitch = self.get_pitch_or_rest()
        if isinstance(pitch, XMLPitch):
            if not self.accidental.get_pitch_parameters()[1]:
                if pitch.xml_alter:
                    pitch.remove(pitch.xml_alter)
                pitch.xml_step, pitch.xml_octave = self.accidental.get_pitch_parameters()[0], self.accidental.get_pitch_parameters()[2]
            else:
                pitch.xml_step, pitch.xml_alter, pitch.xml_octave = self.accidental.get_pitch_parameters()
        else:
            raise TypeError

    def update_pitch_or_rest(self):
        if self._pitch_or_rest is None:
            if self.value == 0:
                self._pitch_or_rest = XMLRest()
            else:
                self._pitch_or_rest = XMLPitch()
        else:
            if self.value == 0:
                if not isinstance(self._pitch_or_rest, XMLRest):
                    self._pitch_or_rest = XMLRest()
                    self.update_parent_note()
                else:
                    pass
            else:
                if not isinstance(self._pitch_or_rest, XMLPitch):
                    self._pitch_or_rest = XMLPitch()
                    self.update_parent_note()
                if self.accidental:
                    self.accidental._update_xml_object()
                    self._update_pitch_parameters()
        if self.up:
            self.up._update_xml_pitch_or_rest()

    # //public properties
    @property
    def accidental(self):
        return self._accidental

    @accidental.setter
    def accidental(self, value):
        if not value:
            value = Accidental()
        elif not isinstance(value, Accidental):
            raise TypeError(f'accidental.value must be of type Accidental not {type(value)}')
        self._accidental = value
        if value:
            self._accidental.parent_midi = self

    @property
    def octave(self):
        return int(self.value / 12) - 1

    @property
    def parent_note(self):
        return self._parent_note

    @parent_note.setter
    def parent_note(self, value):
        if value is not None and 'Note' not in [cls.__name__ for cls in value.__class__.__mro__]:
            raise TypeError
        self._parent_note = value
        self._parent = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if not isinstance(v, float) and not isinstance(v, int):
            raise TypeError(f'Midi.value must be of type float or int not{type(v)}')
        if v != 0 and (v < 12 or v > 127):
            raise ValueError(f'Midi.value {v} can be zero for a rest or must be in a range between 12 and 127 inclusively')
        self._value = v
        self.update_pitch_or_rest()

    @property
    def name(self):
        """
        :returns a string like C#3 consisting of step, accidental sign (or value) and octave. Midi with value 0 returns 'rest' as its name.
        """
        if self.value == 0:
            return 'rest'

        pitch_step = self.accidental.get_pitch_parameters()[1]

        if not pitch_step:
            accidental = ''
        elif pitch_step == -1.5:
            accidental = 'b-'
        elif pitch_step == -1:
            accidental = 'b'
        elif pitch_step == -0.5:
            accidental = '-'
        elif pitch_step == 0.5:
            accidental = '+'
        elif pitch_step == 1:
            accidental = '#'
        elif pitch_step == 1.5:
            accidental = '#+'
        else:
            accidental = str(pitch_step)

        return f"{self.accidental.get_pitch_parameters()[0]}{accidental}{self.octave}"

    # //public methods
    def add_child(self, child):
        super().add_child(child)
        child._update_xml_object()
        child._update_parent_midi()
        return child

    def get_children(self) -> List[Accidental]:
        """
        :return: list of added children.
        :rtype: List[:obj:`~musictree.accidental.Accidental`]
        """
        return super().get_children()

    def get_parent(self) -> 'Note':
        """
        :return: parent
        :rtype: :obj:`~musictree.note.Note`
        """
        return super().get_parent()

    def get_pitch_or_rest(self) -> Union['XMLPitch', 'XMLRest']:
        """
        :return: XMLPitch with appropriate children.
        """
        return self._pitch_or_rest

    def transpose(self, val: float) -> 'Midi':
        """
        Adds val to value and returns self
        """
        self.value += val
        return self

    # //operators
    def __lt__(self, other):  # For x < y
        return self.value < other.value

    def __le__(self, other):  # For x <= y
        return self.value <= other.value

    def __gt__(self, other):  # For x > y
        return self.value > other.value

    def __ge__(self, other):  # For x >= y
        return self.value >= other.value

    def __copy__(self):
        return self.__class__(value=self.value, accidental=self.accidental)

    def __deepcopy__(self):
        copied_accidental = self.accidental.__copy__()
        copied = self.__class__(value=self.value, accidental=copied_accidental)
        return copied


class MidiNote(Midi):
    """
    Parent class of shorthand midi names: C, D, E, F, G, A, B.
    Example C(4, '#') = C(4, 'sharp') = C(4, sharp)
    """
    _VALUE = 60

    def __init__(self, octave, accidental_sign=None, *args, **kwargs):
        self._accidental_sign = accidental_sign
        self._octave = octave
        super().__init__(value=self._get_value(), *args, **kwargs)
        self._set_accidental_mode()

    def _set_accidental_mode(self):
        if self._get_accidental_value() == -1:
            self.accidental.mode = 'flat'
        if self._get_accidental_value() == 1:
            self.accidental.mode = 'sharp'

    def _get_value(self):
        return self._VALUE + self._get_accidental_value() - (4 - self._octave) * 12

    def _get_accidental_value(self):
        if self._accidental_sign is None:
            return 0
        if self._accidental_sign in ('flat', 'f', 'b'):
            return -1
        if self._accidental_sign in ('sharp', 's', '#'):
            return 1

    def __repr__(self):
        return f"{self.name} at {id(self)}"


class C(MidiNote):
    _VALUE = 60


class D(MidiNote):
    _VALUE = 62


class E(MidiNote):
    _VALUE = 64


class F(MidiNote):
    _VALUE = 65


class G(MidiNote):
    _VALUE = 67


class A(MidiNote):
    _VALUE = 69


class B(MidiNote):
    _VALUE = 71


def midi_to_frequency(midi, a4=440):
    try:
        midi = midi.value
    except AttributeError:
        pass

    f = 2 ** ((midi - 69) / 12) * a4
    return f


def frequency_to_midi(frequency, a4=440):
    m = 69 + 12 * log2(frequency / a4)
    return m
