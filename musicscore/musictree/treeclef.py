from musicscore.musictree.midi import Midi, C, G, E, B, F, D, A
from musicscore.musicxml.types.complextypes.attributes import Clef
from musicscore.musicxml.types.complextypes.clef import Sign, Line, ClefOctaveChange


class TreeClef(Clef):

    def __init__(self, sign='G', line=2, octave_change=None, optimal_range=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sign = None
        self._line = None
        self._octave_change = None
        self._optimal_range = None

        self.sign = sign
        self.line = line
        self.octave_change = octave_change
        self.optimal_range = optimal_range

    # //public properties
    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        if not self._line:
            self._line = self.add_child(Line(value))
        else:
            self._line.value = value

        self._line = value

    @property
    def octave_change(self):
        return self._octave_change

    @octave_change.setter
    def octave_change(self, value):
        if value:
            if not self._octave_change:
                self._octave_change = self.add_child(ClefOctaveChange(value))
            else:
                self._octave_change.value = value

            self._octave_change = value
        else:
            if self._octave_change:
                self.remove_child(self._octave_change)
                self._octave_change = None

    @property
    def optimal_range(self):
        return self._optimal_range

    @optimal_range.setter
    def optimal_range(self, val):
        if not val:
            val = [None, None]
        if not hasattr(val, '__iter__'):
            raise TypeError('{} must be an iterator.'.format(val))
        if not len(val) == 2:
            raise TypeError('{} must have two elements.'.format(val))
        for index, x in enumerate(val):
            if x and not isinstance(x, Midi):
                val[index] = Midi(x)

        self._optimal_range = val

    @property
    def sign(self):
        return self._sign

    @sign.setter
    def sign(self, value):
        if not self._sign:
            self._sign = self.add_child(Sign(value))
        else:
            self._sign.value = value

        self._sign = value

    # //public methods
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.sign == other.sign and self.line == other.line and self.octave_change == other.octave_change
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __deepcopy__(self, memodict={}):
        copy = self.__class__(sign=self.sign, line=self.line, octave_change=self.octave_change,
                              optimal_range=self.optimal_range)
        copy.number = self.number
        return copy


SUPER_HIGH_TREBLE_CLEF = TreeClef(sign='G', line=2, octave_change=2, optimal_range=[C(7), None])
HIGH_TREBLE_CLEF = TreeClef(sign='G', line=2, octave_change=1, optimal_range=[C(6), None])
TREBLE_CLEF = TreeClef(sign='G', line=2, optimal_range=[G(3), E(6)])
LOW_TREBLE_CLEF = TreeClef(sign='G', line=2, octave_change=-1, optimal_range=[G(2), E(5)])

BASS_CLEF = TreeClef(sign='F', line=4, optimal_range=[B(1), G(4)])
LOW_BASS_CLEF = TreeClef(sign='F', line=4, octave_change=-1, optimal_range=[None, B(1)])
SUPER_LOW_BASS_CLEF = TreeClef(sign='F', line=4, octave_change=-2, optimal_range=[None, G(1)])

ALTO_CLEF = TreeClef(sign='C', line=3, optimal_range=[A(2), F(5)])
TENOR_CLEF = TreeClef(sign='C', line=4, optimal_range=[F(2), D(5)])

PERCUSSION_CLEF = TreeClef('percussion')

ALL_CLEFS = [SUPER_HIGH_TREBLE_CLEF, HIGH_TREBLE_CLEF, TREBLE_CLEF, LOW_TREBLE_CLEF, BASS_CLEF, LOW_BASS_CLEF,
             SUPER_LOW_BASS_CLEF, ALTO_CLEF, TENOR_CLEF]
