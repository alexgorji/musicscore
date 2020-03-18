from math import log2

from musicscore.musicxml.elements.fullnote import Pitch, Rest
from musicscore.musicxml.elements.note import Notehead


class Accidental(object):
    def __init__(self, mode='standard', force_show=False, force_hide=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = None
        self._force_show = None
        self._force_hide = None

        self.mode = mode
        self.force_show = force_show
        self.force_hide = force_hide

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        permitted = ('standard', 'flat', 'sharp', 'enharmonic_1', 'enharmonic_2')
        if value not in permitted:
            raise TypeError('accidental_mode.value {} must be in {}'.format(value, permitted))
        self._mode = value

    @property
    def force_show(self):
        return self._force_show

    @force_show.setter
    def force_show(self, val):
        if not isinstance(val, bool):
            raise TypeError('force_show.value must be of type bool not{}'.format(type(val)))
        if self.force_hide is True and val is True:
            self.force_hide = False
        self._force_show = val

    @property
    def force_hide(self):
        return self._force_hide

    @force_hide.setter
    def force_hide(self, val):
        if not isinstance(val, bool):
            raise TypeError('force_show.value must be of type bool not{}'.format(type(val)))
        if self.force_show is True and val is True:
            self.force_show = False
        self._force_hide = val

    def __deepcopy__(self, memodict={}, **kwargs):
        output = self.__class__(mode=self.mode, force_show=self.force_show, force_hide=self.force_hide, **kwargs)
        return output


class Midi(object):
    """"""
    # (stem, alter, octaveAdd)
    standard = {
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

    flat = {
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

    sharp = {
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

    enharmonic_1 = {
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

    enharmonic_2 = {
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

    def __init__(self, value=None, accidental=None, note_head=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = None
        self._accidental = None
        self._note_head = None
        self.value = value
        self.accidental = accidental
        self.notehead = note_head

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v is not None:
            if not isinstance(v, float) and not isinstance(v, int):
                raise TypeError('midi.value must be of type float or int not{}'.format(type(v)))
            if v < 16 and v != 0:
                raise ValueError('midi.value {} must be greater than 16'.format(v))
        self._value = v

    @property
    def accidental(self):
        return self._accidental

    @accidental.setter
    def accidental(self, value):
        if not value:
            value = Accidental()
        if isinstance(value, Accidental.__class__):
            raise TypeError('accidental.value must be of type Accidental not{}'.format(type(value)))
        self._accidental = value

    @property
    def notehead(self):
        return self._note_head

    @notehead.setter
    def notehead(self, val):
        if val is not None and not isinstance(val, Notehead):
            val = Notehead(val)
        self._note_head = val

    def add_notehead_object(self, val):
        if not isinstance(val, Notehead):
            raise TypeError()
        self.notehead = val

    def add_notehead(self, val, **kwargs):
        self.add_notehead_object(Notehead(val, **kwargs))

    def get_pitch_name(self):
        if self.accidental.mode == 'standard':
            output = self.standard[self.value % 12]

        elif self.accidental.mode == 'enharmonic_1':
            output = self.enharmonic_1[self.value % 12]

        elif self.accidental.mode == 'enharmonic_2':
            output = self.enharmonic_2[self.value % 12]

        elif self.accidental.mode == 'flat':
            output = self.flat[self.value % 12]

        elif self.accidental.mode == 'sharp':
            output = self.sharp[self.value % 12]

        output = list(output)
        output[2] += (int(self.value // 12)) - 1
        if output[1] == 0:
            output[1] = None

        return output

    def get_pitch_rest(self):
        if self.value == 0:
            return Rest()
        else:
            return Pitch(*self.get_pitch_name())

    def get_flat(self):
        return Midi(value=self.value - 1, accidental=Accidental(mode='flat'))

    def get_sharp(self):
        return Midi(value=self.value + 1, accidental=Accidental(mode='sharp'))

    def transpose(self, val):
        self.value += val
        return self
        # return Midi(value=self.value + val, accidental_mode=self.accidental_mode)

    @property
    def octave(self):
        return int(self.value / 12) - 1

    def __lt__(self, other):  # For x < y
        return self.value < other.value

    def __le__(self, other):  # For x <= y
        return self.value <= other.value

    def __gt__(self, other):  # For x > y
        return self.value > other.value

    def __ge__(self, other):  # For x >= y
        return self.value >= other.value

    @property
    def __name__(self):
        pitch_step = self.get_pitch_name()[1]

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

        return "{}{}{}".format(self.get_pitch_name()[0], accidental, self.octave)

    def __deepcopy__(self, memodict={}, **kwargs):
        output = self.__class__(value=self.value, accidental=self.accidental.__deepcopy__(), note_head=self.notehead,
                                **kwargs)
        return output


class MidiNote(Midi):
    _VALUE = 60

    def __init__(self, octave, accidental_sign=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._accidental_sign = None
        self._octave = None

        self.octave = octave
        self.accidental_sign = accidental_sign

    def _set_new_value(self):
        if self._get_accidental_value() == -1:
            self.accidental.mode = 'flat'
        if self._get_accidental_value() == 1:
            self.accidental.mode = 'sharp'
        self.value = (self._VALUE + self._get_accidental_value()) - (4 - self.octave) * 12

    def _get_accidental_value(self):
        if self.accidental_sign is None:
            return 0
        if self.accidental_sign in ('flat', 'f', 'b'):
            return -1
        if self.accidental_sign in ('sharp', 's', '#'):
            return 1

    @property
    def octave(self):
        return self._octave

    @octave.setter
    def octave(self, val):
        self._octave = val
        self._set_new_value()

    @property
    def accidental_sign(self):
        return self._accidental_sign

    @accidental_sign.setter
    def accidental_sign(self, val):
        self._accidental_sign = val
        self._set_new_value()

    def __deepcopy__(self, memodict={}, **kwargs):
        output = super().__deepcopy__(octave=self.octave, accidental_sign=self.accidental_sign, **kwargs)
        return output

    def __repr__(self):
        return "{} at {}".format(self.__name__, id(self))


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
