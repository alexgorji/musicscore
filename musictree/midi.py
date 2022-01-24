from math import log2
from typing import Optional, Union

from musicxml.xmlelement.xmlelement import *  # type: ignore
from musicxml.xsd.xsdsimpletype import XSDSimpleTypeNoteheadValue  # type: ignore


class Accidental:
    """
    Accidental can be of different modes: standard, flat, sharp, enharmonic_1 or enharmonic_2. It accepts furthermore two parameters:
    force_show and force_hide.
    """
    # (stem, alter, octaveAdd)
    STANDARD = {
        0: ('C', 0, 0),
        0.5: ('C', 0.5, 0),
        1: ('C', 1, 0),
        1.5: ('D', -0.5, 0),
        2: ('D', 0, 0),
        2.5: ('D', 0.5, 0),
        3: ('E', -1, 0),
        3.5: ('E', -0.5, 0),
        4: ('E', 0, 0),
        4.5: ('E', 0.5, 0),
        5: ('F', 0, 0),
        5.5: ('F', 0.5, 0),
        6: ('F', 1, 0),
        6.5: ('G', -0.5, 0),
        7: ('G', 0, 0),
        7.5: ('G', 0.5, 0),
        8: ('A', -1, 0),
        8.5: ('A', -0.5, 0),
        9: ('A', 0, 0),
        9.5: ('A', 0.5, 0),
        10: ('B', -1, 0),
        10.5: ('B', -0.5, 0),
        11: ('B', 0, 0),
        11.5: ('C', -0.5, 1)
    }

    FLAT = {
        0: ('C', 0, 0),
        0.5: ('D', -1.5, 0),
        1: ('D', -1, 0),
        1.5: ('D', -0.5, 0),
        2: ('D', 0, 0),
        2.5: ('E', -1.5, 0),
        3: ('E', -1, 0),
        3.5: ('E', -0.5, 0),
        4: ('E', 0, 0),
        4.5: ('F', -0.5, 0),
        5: ('F', 0, 0),
        5.5: ('G', -1.5, 0),
        6: ('G', -1, 0),
        6.5: ('G', -0.5, 0),
        7: ('G', 0, 0),
        7.5: ('A', -1.5, 0),
        8: ('A', -1, 0),
        8.5: ('A', -0.5, 0),
        9: ('A', 0, 0),
        9.5: ('B', -1.5, 0),
        10: ('B', -1, 0),
        10.5: ('B', -0.5, 0),
        11: ('B', 0, 0),
        11.5: ('C', -0.5, 1)
    }

    SHARP = {
        0: ('C', 0, 0),
        0.5: ('C', 0.5, 0),
        1: ('C', 1, 0),
        1.5: ('C', 1.5, 0),
        2: ('D', 0, 0),
        2.5: ('D', 0.5, 0),
        3: ('D', 1, 0),
        3.5: ('D', 1.5, 0),
        4: ('E', 0, 0),
        4.5: ('E', 0.5, 0),
        5: ('F', 0, 0),
        5.5: ('F', 0.5, 0),
        6: ('F', 1, 0),
        6.5: ('F', 1.5, 0),
        7: ('G', 0, 0),
        7.5: ('G', 0.5, 0),
        8: ('G', 1, 0),
        8.5: ('G', 1.5, 0),
        9: ('A', 0, 0),
        9.5: ('A', 0.5, 0),
        10: ('A', 1, 0),
        10.5: ('A', 1.5, 0),
        11: ('B', 0, 0),
        11.5: ('B', 0.5, 0)
    }

    ENHARMONIC1 = {
        0: ('B', 1, -1),
        0.5: ('D', -1.5, 0),
        1: ('D', -1, 0),
        1.5: ('C', 1.5, 0),
        2: ('C', 2, 0),
        2.5: ('E', -1.5, 0),
        3: ('D', 1, 0),
        3.5: ('D', 1.5, 0),
        4: ('F', -1, 0),
        4.5: ('F', -0.5, 0),
        5: ('E', 1, 0),
        5.5: ('G', -1.5, 0),
        6: ('G', -1, 0),
        6.5: ('F', 1.5, 0),
        7: ('F', 2, 0),
        7.5: ('A', -1.5, 0),
        8: ('G', 1, 0),
        8.5: ('G', 1.5, 0),
        9: ('G', 2, 0),
        9.5: ('B', -1.5, 0),
        10: ('A', 1, 0),
        10.5: ('A', 1.5, 0),
        11: ('C', -1, 1),
        11.5: ('B', 0.5, 0)
    }

    ENHARMONIC2 = {
        0: ('D', -2, 0),
        1: ('B', 2, -1),
        2: ('E', 2, 0),
        3: ('F', -2, 0),
        4: ('D', 2, 0),
        5: ('G', -2, 0),
        6: ('E', 2, 0),
        7: ('A', -2, 0),
        9: ('B', -2, 0),
        10: ('C', -2, 1),
        11: ('A', 2, 0)
    }

    def __init__(self, mode='standard', force_show: bool = False, force_hide: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = None
        self._force_show = None
        self._force_hide = None
        self.parent_midi = None

        self.mode = mode
        self.force_show = force_show
        self.force_hide = force_hide

    def _update_parent_midi(self):
        if self.parent_midi:
            self.parent_midi.update_accidental()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        permitted = ('standard', 'flat', 'sharp', 'enharmonic_1', 'enharmonic_2')
        if value not in permitted:
            raise TypeError(f'accidental_mode.value {value} must be in {permitted}')
        self._mode = value
        self._update_parent_midi()

    @property
    def force_show(self):
        return self._force_show

    @force_show.setter
    def force_show(self, val):
        if not isinstance(val, bool):
            raise TypeError(f'force_show.value must be of type bool not {type(val)}')
        if self.force_hide is True and val is True:
            self.force_hide = False
        self._force_show = val
        self._update_parent_midi()

    @property
    def force_hide(self):
        return self._force_hide

    @force_hide.setter
    def force_hide(self, val):
        if not isinstance(val, bool):
            raise TypeError(f'force_show.value must be of type bool not {type(val)}')
        if self.force_show is True and val is True:
            self.force_show = False
        self._force_hide = val
        self._update_parent_midi()

    def __deepcopy__(self, memodict={}, **kwargs):
        output = self.__class__(mode=self.mode, force_show=self.force_show, force_hide=self.force_hide, **kwargs)
        return output


class Midi:
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

    def _update_parent_note(self):
        if self.parent_note:
            self.parent_note.update_midi()

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
                else:
                    pass
            else:
                if not isinstance(self._pitch_or_rest, XMLPitch):
                    self._pitch_or_rest = XMLPitch()
                if self.accidental:
                    self.update_accidental()

    # //public properties
    @property
    def accidental(self):
        return self._accidental

    @accidental.setter
    def accidental(self, value):
        if not value:
            if self.value:
                value = Accidental()
        elif not isinstance(value, Accidental):
            raise TypeError(f'accidental.value must be of type Accidental not {type(value)}')
        self._accidental = value
        if value:
            self._accidental.parent_midi = self
            self.update_accidental()

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
        self._update_parent_note()


    @property
    def name(self):
        """
        :returns a string like C#3 consisting of stem, accidental sign (or value) and octave. Midi with value 0 returns 'rest' as its name.
        """
        if self.value == 0:
            return 'rest'

        pitch_step = self.get_pitch_parameters()[1]

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

        return f"{self.get_pitch_parameters()[0]}{accidental}{self.octave}"

    # //public methods

    def get_pitch_parameters(self) -> Optional[tuple]:
        """
        :return: a tuple consisting of pitch stem name, alter value and octave value. A Midi object with value 0 returns None.
        """

        if self.value == 0:
            return None

        if self.accidental.mode == 'standard':
            output = Accidental.STANDARD[self.value % 12]

        elif self.accidental.mode == 'enharmonic_1':
            output = Accidental.ENHARMONIC1[self.value % 12]

        elif self.accidental.mode == 'enharmonic_2':
            output = Accidental.ENHARMONIC2[self.value % 12]

        elif self.accidental.mode == 'flat':
            output = Accidental.FLAT[self.value % 12]

        elif self.accidental.mode == 'sharp':
            output = Accidental.SHARP[self.value % 12]

        else:
            raise ValueError
        return output[0], output[1], output[2] + (int(self.value // 12)) - 1

    def get_pitch_or_rest(self) -> Union['XMLPitch', 'XMLRest']:
        """
        :return: XMLPitch with appropriate children.
        """
        return self._pitch_or_rest

    def update_accidental(self):
        pitch = self.get_pitch_or_rest()
        if isinstance(pitch, XMLPitch):
            if not self.get_pitch_parameters()[1]:
                if pitch.xml_alter:
                    pitch.remove(pitch.xml_alter)
                pitch.xml_step, pitch.xml_octave = self.get_pitch_parameters()[0], self.get_pitch_parameters()[2]
            else:
                pitch.xml_step, pitch.xml_alter, pitch.xml_octave = self.get_pitch_parameters()
        else:
            raise TypeError

    # other
    #
    # def flatten(self) -> 'Midi':
    #     """
    #     :return: A halftone lower Midi with flat as accidental mode.
    #     """
    #     return Midi(value=self.value - 1, accidental=Accidental(mode='flat'))
    #
    # def sharpen(self) -> 'Midi':
    #     """
    #     :return: A halftone higher Midi with sharp as accidental mode.
    #     """
    #     return Midi(value=self.value + 1, accidental=Accidental(mode='sharp'))

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

    # //copy
    def __deepcopy__(self, memodict=None, **kwargs):
        output = self.__class__(value=self.value, accidental=self.accidental.__deepcopy__(), note_head=self.notehead,
                                **kwargs)
        return output


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

    def __deepcopy__(self, memodict={}, **kwargs):
        output = super().__deepcopy__(octave=self._octave, accidental_sign=self._accidental_sign, **kwargs)
        return output

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
