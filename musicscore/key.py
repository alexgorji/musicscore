from typing import Optional

from musicxml.xmlelement.xmlelement import XMLKey

from musicscore.xmlwrapper import XMLWrapper

__all__ = ['Key']


class Key(XMLWrapper):
    _ATTRIBUTES = {'fifths', 'show'}
    XMLClass = XMLKey

    def __init__(self, fifths: int = 0, show: bool = True, *args, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(*args, **kwargs)
        self.fifths = fifths
        self._show = None
        self.show = show

    @property
    def fifths(self) -> Optional[int]:
        """
        Set and get ``value_`` of :obj:`~musicxml.xmlelement.xmlelement.XMLFifths` child object of associated :obj:`~musicxml.xmlelement.xmlelement.XMLKey`

        :return: ``self.xml_object.xml_fifths.value_``
        """
        if self.xml_object.xml_fifths:
            return self.xml_object.xml_fifths.value_

    @fifths.setter
    def fifths(self, val):
        self.xml_object.xml_fifths = val

    @property
    def show(self) -> bool:
        """
        Set and get show attribute. If ``False`` :obj:`Key` object is not shown.
        """
        return self._show

    @show.setter
    def show(self, val):
        if not isinstance(val, bool):
            raise TypeError
        self._show = val

    def __copy__(self):
        return self.__class__(fifths=self.fifths, show=self.show)
