from musictree import QuarterDuration
from musictree.xmlwrapper import XMLWrapper
from musicxml.xmlelement.xmlelement import XMLMetronome, XMLBeatUnitDot


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
        self.xml_object.xml_beat_unit = self.beat_unit.get_type()

    def _set_xml_beat_unit_dots(self):
        number_of_dots = self.beat_unit.get_number_of_dots()
        current_xml_unit_dots = [ch for ch in self.xml_object.get_children() if isinstance(ch, XMLBeatUnitDot)]
        if number_of_dots == 0:
            for xml_unit_dot in current_xml_unit_dots:
                self.xml_object.remove(xml_unit_dot)



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
        if not isinstance(val, QuarterDuration):
            val = QuarterDuration(val)
        self._beat_unit = val
        self._set_xml_beat_unit()
        self._set_xml_beat_unit_dots()
