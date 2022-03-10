from typing import Optional

from musicxml.xmlelement.xmlelement import XMLClef

from musictree.xmlwrapper import XMLWrapper

__all__ = ['Clef', 'TrebleClef', 'BassClef', 'AltoClef', 'TenorClef']


class Clef(XMLWrapper):
    _ATTRIBUTES = {'show', 'sign', 'line', 'octave_change'}
    XMLClass = XMLClef

    def __init__(self, sign: str = 'G', line: int = 2, octave_change: int = None, show: bool = True, *args, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(*args, **kwargs)
        self._show = None
        self.show = show
        self.line = line
        self.sign = sign
        self.octave_change = octave_change

    @property
    def line(self) -> Optional[int]:
        """
        Sets and gets ``value_`` of :obj:`~musicxml.xmlelement.xmlelement.XMLLine`

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
        Sets and gets ``value_`` of :obj:`~musicxml.xmlelement.xmlelement.XMLClefOctaveChange`

        :return: ``self.xml_object.xml_clef_octave_change.value_``
        :rtype: int, None
        """

        if self.xml_object.xml_clef_octave_change:
            return self.xml_object.xml_clef_octave_change.value_

    @octave_change.setter
    def octave_change(self, val):
        self.xml_object.xml_clef_octave_change = val

    @property
    def sign(self) -> Optional[str]:
        """
        Sets and gets ``value_`` of :obj:`~musicxml.xmlelement.xmlelement.XMLSign`

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
        Sets and gets show attribute. If ``False`` :obj:`Clef` element is not shown.
        """
        return self._show

    @show.setter
    def show(self, val):
        if not isinstance(val, bool):
            raise TypeError
        self._show = val

    @XMLWrapper.xml_object.getter
    def xml_object(self) -> XMLClass:
        return super().xml_object

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

    def __init__(self, show: bool = True, octave_change: Optional[int] = None, *kwargs):
        super().__init__(sign='G', line=2, show=show, octave_change=octave_change, *kwargs)


class BassClef(Clef):
    """
    Default parameters:
      - sign='F'
      - line=4
    """

    def __init__(self, show: bool = True, octave_change: Optional[int] = None, *kwargs):
        super().__init__(sign='F', line=4, show=show, octave_change=octave_change, *kwargs)


class AltoClef(Clef):
    """
    Default parameters:
      - sign='C'
      - line=3
    """

    def __init__(self, show: bool = True, octave_change: Optional[int] = None, *kwargs):
        super().__init__(sign='C', line=3, show=show, octave_change=octave_change, *kwargs)


class TenorClef(Clef):
    """
    Default parameters:
      - sign='C'
      - line=4
    """

    def __init__(self, show: bool = True, octave_change: Optional[int] = None, *kwargs):
        super().__init__(sign='C', line=4, show=show, octave_change=octave_change, *kwargs)
