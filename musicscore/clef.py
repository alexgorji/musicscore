from typing import Optional

from musicscore.xmlwrapper import XMLWrapper
from musicxml.xmlelement.xmlelement import XMLClef

__all__ = ['Clef', 'TrebleClef', 'BassClef', 'AltoClef', 'TenorClef']


class Clef(XMLWrapper):
    _ATTRIBUTES = {'show', 'sign', 'line', 'octave_change'}
    XMLClass = XMLClef

    def __init__(self, sign: str = 'G', line: Optional[int] = 2, octave_change: int = None, show: bool = True,
                 default: bool = False, *args, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(*args, **kwargs)
        self._show = None
        self.show = show
        self.line = line
        self.sign = sign
        self.octave_change = octave_change

        self._default = default

    @property
    def line(self) -> Optional[int]:
        """
        Set and get ``value_`` of :obj:`~musicxml.xmlelement.xmlelement.XMLLine`

        :return: ``self.xml_object.xml_line.value_``
        :rtype: int, None
        """
        if self.xml_object.xml_line:
            return self.xml_object.xml_line.value_

    @line.setter
    def line(self, val):
        self.xml_object.xml_line = val

    @property
    def octave_change(self) -> Optional[int]:
        """
        Set and get ``value_`` (int) of :obj:`~musicxml.xmlelement.xmlelement.XMLOctaveChange` child object of associated :obj:`~musicxml.xmlelement.xmlelement.XMLClef` which indicates how many octaves must be added to get from written pitch to the sounding pitch.

        :return: ``self.xml_object.xml_clef_octave_change.value_``
        """

        if self.xml_object.xml_clef_octave_change:
            return self.xml_object.xml_clef_octave_change.value_

    @octave_change.setter
    def octave_change(self, val):
        self.xml_object.xml_clef_octave_change = val

    @property
    def sign(self) -> Optional[str]:
        """
        Set and get ``value_`` of :obj:`~musicxml.xmlelement.xmlelement.XMLSign` child object of associated :obj:`~musicxml.xmlelement.xmlelement.XMLClef`

        :return: ``self.xml_object.xml_sign.value_``
        :rtype: str, None
        """
        if self.xml_object.xml_sign:
            return self.xml_object.xml_sign.value_

    @sign.setter
    def sign(self, val):
        self.xml_object.xml_sign = val

    @property
    def show(self) -> bool:
        """
        Set and get show attribute. If ``False`` :obj:`Clef` element is not shown.
        """
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
    """
    Default parameters:
      - sign='G'
      - line=2
    """

    def __init__(self, show: bool = True, octave_change: Optional[int] = None, **kwargs):
        super().__init__(sign='G', line=2, show=show, octave_change=octave_change, **kwargs)


class BassClef(Clef):
    """
    Default parameters:
      - sign='F'
      - line=4
    """

    def __init__(self, show: bool = True, octave_change: Optional[int] = None, **kwargs):
        super().__init__(sign='F', line=4, show=show, octave_change=octave_change, **kwargs)


class AltoClef(Clef):
    """
    Default parameters:
      - sign='C'
      - line=3
    """

    def __init__(self, show: bool = True, octave_change: Optional[int] = None, **kwargs):
        super().__init__(sign='C', line=3, show=show, octave_change=octave_change, **kwargs)


class TenorClef(Clef):
    """
    Default parameters:
      - sign='C'
      - line=4
    """

    def __init__(self, show: bool = True, octave_change: Optional[int] = None, **kwargs):
        super().__init__(sign='C', line=4, show=show, octave_change=octave_change, **kwargs)


class PercussionClef(Clef):
    """
    Default parameters:
      - sign=percussion
      - line=None
    """

    def __init__(self, show: bool = True, octave_change: Optional[int] = None, **kwargs):
        super().__init__(sign='percussion', line=None, show=show, octave_change=octave_change, **kwargs)
