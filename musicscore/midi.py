import copy
from math import log2
from typing import Optional, Union, List

from musicscore import STANDARD, ENHARMONIC, FLAT, SHARP, FORCEFLAT, FORCESHARP
from musicscore.exceptions import AlreadyFinalizedError
from musicxml.xmlelement.xmlelement import *  # type: ignore
from musicxml.xsd.xsdsimpletype import XSDSimpleTypeNoteheadValue  # type: ignore

from musicscore.accidental import Accidental
from musicscore.musictree import MusicTree

__all__ = ['Midi', 'MidiNote', 'C', 'D', 'E', 'F', 'G', 'A', 'B', 'midi_to_frequency', 'frequency_to_midi',
           'get_accidental_mode']


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


def get_accidental_mode(midi_value: Union[float, int], accidental_sign: Optional[str] = None) -> str:
    """
    :param midi_value: a valid midi value in half steps (int or float)
    :param accidental_sign: ``double-flat``, ``flat-flat``, ``bb``, ``ff`` – ``three-quarters-flat`` – ``flat``, ``b``, ``f`` – ``quarter-flat`` – ``None``, ``natural`` – ``quarter-sharp`` – ``sharp``, ``#``, ``s`` – ``three-quarters-sharp`` – ``double-sharp``, ``sharp-sharp``, ``x``, ``##``, ``ss``
    :return: accidental_mode: ``standard``, ``enharmonic``, ``flat``, ``sharp``, ``force-flat``, ``force-sharp``
    """
    # midi value is valid
    Midi(midi_value)
    if accidental_sign in [None, 'natural']:
        accidental_value = 0
    elif accidental_sign in ['quarter-sharp']:
        accidental_value = 0.5
    elif accidental_sign in ['sharp', '#', 's']:
        accidental_value = 1
    elif accidental_sign in ['three-quarters-sharp']:
        accidental_value = 1.5
    elif accidental_sign in ['double-sharp', 'sharp-sharp', 'x', '##', 'ss']:
        accidental_value = 2
    elif accidental_sign in ['quarter-flat']:
        accidental_value = -0.5
    elif accidental_sign in ['flat', 'b', 'f']:
        accidental_value = -1
    elif accidental_sign in ['three-quarters-flat']:
        accidental_value = -1.5
    elif accidental_sign in ['double-flat', 'flat-flat', 'bb', 'ff']:
        accidental_value = -2
    else:
        raise NotImplementedError(accidental_sign)

    if STANDARD[midi_value % 12][1] == accidental_value:
        return 'standard'
    elif ENHARMONIC[midi_value % 12][1] == accidental_value:
        return 'enharmonic'
    elif FLAT[midi_value % 12][1] == accidental_value:
        return 'flat'
    elif SHARP[midi_value % 12][1] == accidental_value:
        return 'sharp'
    elif FORCEFLAT[midi_value % 12][1] == accidental_value:
        return 'force-flat'
    elif FORCESHARP[midi_value % 12][1] == accidental_value:
        return 'force-sharp'


class Midi(MusicTree):
    """
    Parent type: :obj:`~musicscore.note.Note`

    Child type: :obj:`~musicscore.accidental.Accidental`

    Midi is the representation of a Pitch with its midi value, and accidental sign. This object is used to create a Chord
    consisting of one or more pitches. The midi representation of a rest is a Midi object with value 0.
    """

    def __init__(self, value: Union[float, int], accidental: Optional[Accidental] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = None
        self._accidental = None
        self._notehead = None
        self._pitch_or_rest = None
        self._parent_chord = None
        self._parent_note = None
        self._ties = set()

        self._staff_number = None

        self.value = value
        self.accidental = accidental

    def _set_parent_chord(self, value):
        if value is not None and 'Chord' not in [cls.__name__ for cls in value.__class__.__mro__]:
            raise TypeError
        self._parent_chord = value
        # self._parent = value

    def _update_parent_note(self):
        if self.parent_note:
            self.parent_note._update_xml_pitch_or_rest()
            self.parent_note._update_xml_accidental()

    def _update_pitch_parameters(self):
        pitch = self.get_pitch_or_rest()
        if isinstance(pitch, XMLPitch):
            if not self.accidental.get_pitch_parameters()[1]:
                if pitch.xml_alter:
                    pitch.remove(pitch.xml_alter)
                pitch.xml_step, pitch.xml_octave = self.accidental.get_pitch_parameters()[0], \
                    self.accidental.get_pitch_parameters()[2]
            else:
                pitch.xml_step, pitch.xml_alter, pitch.xml_octave = self.accidental.get_pitch_parameters()
        else:
            raise TypeError

    def _update_pitch_or_rest(self):
        if self._pitch_or_rest is None:
            if self.value == 0:
                self._pitch_or_rest = XMLRest()
            else:
                self._pitch_or_rest = XMLPitch()
        else:
            if self.value == 0:
                if not isinstance(self._pitch_or_rest, XMLRest):
                    self._pitch_or_rest = XMLRest()
                    self._update_parent_note()
                else:
                    pass
            else:
                if not isinstance(self._pitch_or_rest, XMLPitch):
                    self._pitch_or_rest = XMLPitch()
                    self._update_parent_note()
                if self.accidental:
                    self.accidental._update_xml_object()
                    self._update_pitch_parameters()
        if self.up:
            self.up._update_xml_pitch_or_rest()

    # //public properties
    @property
    def accidental(self) -> "Accidental":
        """
        Set or get :obj:`~musicscore.accidental.Accidental` object associated with this midi. If it is set to ``None`` an :obj:`~musicscore.accidental.Accidental` object will be created.
        """
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
    def is_tied_to_next(self) -> bool:
        """
        :return: ``True`` if this midi adds a :obj:`~musicxml.xmlelement.xmlelement.XMLTie` object of type ``start`` :obj:`~musicscore.note.Note`.
        """
        if 'start' in self._ties:
            return True
        else:
            return False

    @property
    def is_tied_to_previous(self):
        """
        :return: ``True`` if this midi adds a :obj:`~musicxml.xmlelement.xmlelement.XMLTie` object of type ``stop`` :obj:`~musicscore.note.Note`.

        """
        if 'stop' in self._ties:
            return True
        else:
            return False

    @property
    def notehead(self) -> Optional["XMLNotehead"]:
        """
        Set or get notedhead property. This can be ``None`` or an :obj:`~musicxml.xmlelement.xmlelement.XMLNotehead` object. It is possible to set this property with a valid notehead value of type str. For permitted values see :obj:`~musicxml.xmlelement.xmlelement.XMLNotehead`.
        """
        return self._notehead

    @notehead.setter
    def notehead(self, val):
        if self.parent_note:
            raise AlreadyFinalizedError('Cannot change notehead after finalizing.')

        if val is None:
            self._notehead = None
        elif not isinstance(val, XMLNotehead):
            self._notehead = XMLNotehead(val)
        else:
            self._notehead = val

    @property
    def octave(self) -> int:
        """
        :return: octave number of this midi.
        """
        return int(self.value / 12) - 1

    @property
    def parent_chord(self) -> "Chord":
        """
        Set or get parent :obj:`~musicscore.chord.Chord` object.
        """
        return self._parent_chord

    @property
    def parent_note(self) -> "Note":
        """
        Set or get parent :obj:`~musicscore.note.Note` object.
        """
        return self._parent_note

    @parent_note.setter
    def parent_note(self, value):
        if value is not None and 'Note' not in [cls.__name__ for cls in value.__class__.__mro__]:
            raise TypeError
        self._parent_note = value
        self._parent = value

    @property
    def value(self) -> Union[float, int]:
        """
        Set and get value of midi. A valid value must be of type ``float`` or ``int`` and can be between ``12`` and ``127``.
        """
        return self._value

    @value.setter
    def value(self, v):
        if not isinstance(v, float) and not isinstance(v, int):
            raise TypeError(f'Midi.value must be of type float or int not{type(v)}')
        if v != 0 and (v < 12 or v > 127):
            raise ValueError(
                f'Midi.value {v} can be zero for a rest or must be in a range between 12 and 127 inclusively')
        self._value = v
        self._update_pitch_or_rest()

    @property
    def name(self) -> str:
        """
        :return: a string like ``C#3`` consisting of ``step``, ``accidental sign`` (or value) and ``octave``. Midi with value 0 returns ``rest`` as its name.
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
    def add_child(self, child: [Accidental]) -> Accidental:
        """
        child's _update method will be called after adding.
        
        :param child:
        :return: child
        :rtype: :obj:`~musicscore.accidental.Accidental`
        """
        if self.parent_chord and self.parent_chord._finalized is True:
            raise AlreadyFinalizedError(self, 'add_child')
        super().add_child(child)
        child._update()
        return child

    def add_tie(self, type: str) -> None:
        """
        A :obj:`~musicxml.xmlelement.xmlelement.XMLTie` child of type ``start`` or ``stop``  will be added to :obj:`~parent_note` object

        :param type: ``start``, ``stop``
        :exception: ValueError
        """
        if type not in ['start', 'stop']:
            raise ValueError
        self._ties.add(type)
        if self.parent_note:
            self.parent_note._update_ties()

    def get_pitch_or_rest(self) -> Union['XMLPitch', 'XMLRest']:
        """
        :return: :obj:`~musicxml.xmlelement.xmlelement.XMLPitch` or :obj:`~musicxml.xmlelement.xmlelement.XMLRest` object associated with this :obj:`~musicscore.midi.Midi`.
        """
        return self._pitch_or_rest

    def get_staff_number(self):
        """
        :return: get manually set staff number (necessary for cross-staff notation)
        """
        return self._staff_number

    def remove_tie(self, type: str) -> None:
        """
        :param type: ``start``, ``stop``
        :exception: ValueError
        """
        removed = False
        try:
            self._ties.remove(type)
            removed = True
        except KeyError:
            pass
        if removed and self.parent_note:
            self.parent_note._update_ties()

    def set_staff_number(self, val):
        """
        Set staff number manually (necessary for cross-staff notation).
        """
        self._staff_number = val

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
        copied = self.__class__(value=self.value, accidental=self.accidental)
        copied._ties = self._ties
        return copied

    def __deepcopy__(self, memodict={}):
        copied_accidental = copy.copy(self.accidental)
        copied = self.__class__(value=self.value, accidental=copied_accidental)
        copied._ties = copy.copy(self._ties)
        return copied

    def _copy_for_split(self):
        copied_accidental = copy.copy(self.accidental)
        copied = self.__class__(value=self.value, accidental=copied_accidental)
        copied.notehead = self.notehead
        return copied


class MidiNote(Midi):
    """
    Parent class of shorthand midi names: C, D, E, F, G, A, B.
    Example C(4, '#') = C(4, 'sharp') = C(4, sharp)
    """
    _VALUE = 60

    def __init__(self, octave: object, accidental_sign: object = None, *args: object, **kwargs: object) -> object:
        self._accidental_sign = accidental_sign
        self._octave = octave
        super().__init__(value=self._get_value(), *args, **kwargs)
        self._set_accidental_mode()

    def _set_accidental_mode(self):
        self.accidental.mode = get_accidental_mode(self.value, self._accidental_sign)

    def _get_value(self):
        return self._VALUE + self._get_accidental_value() - (4 - self._octave) * 12

    def _get_accidental_value(self):
        permitted = ['double-flat', 'flat-flat', 'ff', 'bb', 'three-quarters-flat', 'flat', 'f', 'b', 'quarter-flat',
                     'quarter-sharp', 'sharp', 's', '#', 'three-quarters-sharp', 'double-sharp', 'sharp-sharp', 'ss',
                     '##', 'x']
        if self._accidental_sign in ['double-flat', 'flat-flat', 'ff', 'bb']:
            return -2
        elif self._accidental_sign in ['three-quarters-flat']:
            return -1.5
        elif self._accidental_sign in ['flat', 'f', 'b']:
            return -1
        elif self._accidental_sign in ['quarter-flat']:
            return -0.5
        elif self._accidental_sign in [None, 'natural']:
            return 0
        elif self._accidental_sign in ['quarter-sharp']:
            return 0.5
        elif self._accidental_sign in ['sharp', 's', '#']:
            return 1
        elif self._accidental_sign in ['three-quarters-sharp']:
            return 1.5
        elif self._accidental_sign in ['double-sharp', 'sharp-sharp', 'ss', '##', 'x']:
            return 2
        else:
            raise ValueError(f'accidental_sign value {self._accidental_sign} can be None or must be in {permitted}')

    def __repr__(self):
        return f"{self.name} at {id(self)}"

    def __copy__(self):
        copied = Midi(value=self.value, accidental=self.accidental)
        copied._ties = self._ties
        return copied

    def __deepcopy__(self, memodict={}):
        copied_accidental = copy.copy(self.accidental)
        copied = Midi(value=self.value, accidental=copied_accidental)
        copied._ties = copy.copy(self._ties)
        return copied

    def _copy_for_split(self):
        copied_accidental = copy.copy(self.accidental)
        copied = Midi(value=self.value, accidental=copied_accidental)
        copied.notehead = self.notehead
        return copied


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
