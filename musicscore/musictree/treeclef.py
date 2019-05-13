from musicscore.musicxml.types.complextypes.attributes import Clef
from musicscore.musicxml.types.complextypes.clef import Sign, Line, ClefOctaveChange


class TreeClef(Clef):

    def __init__(self, sign='G', line=2, octave_change=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sign = None
        self._line = None
        self._octave_change = None

        self.sign = sign
        self.line = line
        self.octave_change = octave_change

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
        if not self._sign:
            self._sign = self.add_child(Sign(value))
        else:
            self._sign.value = value

        self._sign = value

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


SUPER_HIGH_TREBLE_CLEF = TreeClef(sign='G', line=2, octave_change=2)
HIGH_TREBLE_CLEF = TreeClef(sign='G', line=2, octave_change=1)
TREBLE_CLEF = TreeClef(sign='G', line=2)
LOW_TREBLE_CLEF = TreeClef(sign='G', line=2, octave_change=-1)
BASS_CLEF = TreeClef(sign='F', line=4)
LOW_BASS_CLEF = TreeClef(sign='F', line=4, octave_change=-1)
SUPER_LOW_BASS_CLEF = TreeClef(sign='F', line=4, octave_change=-2)

ALTO_CLEF = TreeClef(sign='C', line=3)
TENOR_CLEF = TreeClef(sign='C', line=4)

PERCUSSION_CLEF = TreeClef('percussion')
