from musicxml.xmlelement.xmlelement import XMLClef

from musictree.xmlwrapper import XMLWrapper


class Clef(XMLWrapper):
    _ATTRIBUTES = {'show', 'sign', 'line', 'octave_change'}

    def __init__(self, sign='G', line=2, octave_change=None, show=True, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLClef(*args, **kwargs)
        self._show = None
        self._sign = None
        self._line = None
        self._octave_change = None
        self.show = show
        self.line = line
        self.sign = sign
        self.octave_change = octave_change

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, val):
        self._line = val
        self.xml_object.xml_line = val

    @property
    def octave_change(self):
        return self._octave_change

    @octave_change.setter
    def octave_change(self, val):
        self._octave_change = val
        self.xml_object.xml_clef_octave_change = val

    @property
    def sign(self):
        return self._sign

    @sign.setter
    def sign(self, val):
        self._sign = val
        self.xml_sign = val

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, val):
        if not isinstance(val, bool):
            raise TypeError
        self._show = val

    def __copy__(self):
        new_clef = self.__class__()
        new_clef.sign = self.sign
        new_clef.line = self.line
        new_clef.octave_change = self.octave_change
        new_clef.show = self._show
        return new_clef


class TrebleClef(Clef):
    def __init__(self, show=True, octave_change=None, *kwargs):
        super().__init__(sign='G', line=2, show=show, octave_change=octave_change, *kwargs)


class BaseClef(Clef):
    def __init__(self, show=True, octave_change=None, *kwargs):
        super().__init__(sign='F', line=4, show=show, octave_change=octave_change, *kwargs)


class AltoClef(Clef):
    def __init__(self, show=True, octave_change=None, *kwargs):
        super().__init__(sign='C', line=3, show=show, octave_change=octave_change, *kwargs)


class TenorClef(Clef):
    def __init__(self, show=True, octave_change=None, *kwargs):
        super().__init__(sign='C', line=4, show=show, octave_change=octave_change, *kwargs)
