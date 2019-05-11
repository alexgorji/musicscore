class TreeClef(object):

    def __init__(self, sign='G', line=2, octave_change=None, force_show=False):
        self._sign = sign
        self._line = line
        self._octave_change = octave_change
        self.force_show = force_show

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.sign == other.sign and self.line == other.line and self.octave_change == other.octave_change
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def sign(self):
        return self._sign

    @sign.setter
    def sign(self, value):
        self._sign = value

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._line = value

    @property
    def octave_change(self):
        return self._octave_change

    @octave_change.setter
    def octave_change(self, value):
        self._octave_change = value


HIGH_TREBLE_CLEF = Clef(sign='G', line=2, octave_change=1)
TREBLE_CLEF = Clef(sign='G', line=2)
LOW_TREBLE_CLEF = Clef(sign='G', line=2, octave_change=-1)
BASS_CLEF = Clef(sign='F', line=4)
LOW_BASS_CLEF = Clef(sign='F', line=4, octave_change=-1)

ALTO_CLEF = Clef(sign='C', line=3)
TENOR_CLEF = Clef(sign='C', line=4)

PERCUSSION_CLEF = Clef('percussion')