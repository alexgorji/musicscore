from musicxml.xmlelement.xmlelement import XMLKey

from musictree.xmlwrapper import XMLWrapper


class Key(XMLWrapper):
    _ATTRIBUTES = {'fifths', 'show'}

    def __init__(self, fifths=0, show=True, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLKey(*args, **kwargs)
        self._fifths = None
        self.fifths = fifths
        self._show = None
        self.show = show

    @property
    def fifths(self):
        return self._fifths

    @fifths.setter
    def fifths(self, val):
        self._fifths = val
        self.xml_object.xml_fifths = val

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, val):
        if not isinstance(val, bool):
            raise TypeError
        self._show = val

    def __copy__(self):
        return self.__class__(fifths=self.fifths, show=self.show)
