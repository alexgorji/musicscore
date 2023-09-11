from musictree.xmlwrapper import XMLWrapper
from musicxml.xmlelement.xmlelement import XMLMetronome


class Metronome(XMLWrapper):
    _ATTRIBUTES = {'per_minute', 'beat_unit'}
    XMLClass = XMLMetronome

    def __init__(self, per_minute, beat_unit=1, *args, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(*args, **kwargs)
        self._per_minute = None
        self._beat_unit = None

        self.per_minute = per_minute
        self.beat_unit = beat_unit

    def _set_xml_per_minute(self):
        self.xml_object.xml_per_minute = str(self.per_minute)

    def _set_xml_beat_unit(self):
        self.xml_object.xml_beat_unit = Qua

    @property
    def per_minute(self):
        return self._per_minute

    @per_minute.setter
    def per_minute(self, val):
        self._per_minute = val
        self._set_xml_per_minute()

    @property
    def beat_unit(self):
        return self._beat_unit

    @beat_unit.setter
    def beat_unit(self, val):
        self._beat_unit = val
        self._set_xml_beat_unit()
