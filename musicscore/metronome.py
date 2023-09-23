from musicscore.quarterduration import QuarterDuration
from musicscore.exceptions import QuarterDurationIsNotWritable, MetronomeWrongBeatUnitError
from musicscore.xmlwrapper import XMLWrapper
from musicxml.xmlelement.xmlelement import XMLMetronome, XMLBeatUnitDot, XMLSound


class Metronome(XMLWrapper):
    _ATTRIBUTES = {'per_minute', 'beat_unit'}
    XMLClass = XMLMetronome

    def __init__(self, per_minute, beat_unit=1, parenthesis=False, *args, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(*args, **kwargs)
        self._per_minute = None
        self._beat_unit = None
        self._sound = XMLSound()

        self.per_minute = per_minute
        self.beat_unit = beat_unit

    def _set_xml_beat_unit(self):
        if self.beat_unit.denominator not in [1, 2, 4, 8, 16, 32]:
            raise MetronomeWrongBeatUnitError(self.beat_unit)
        try:
            self.xml_object.xml_beat_unit = self.beat_unit.get_type()
        except QuarterDurationIsNotWritable:
            raise MetronomeWrongBeatUnitError(self.beat_unit)
        self._set_xml_sound_tempo()

    def _set_xml_per_minute(self):
        self.xml_object.xml_per_minute = str(self.per_minute)
        self._set_xml_sound_tempo()

    def _set_xml_sound_tempo(self):
        if self.beat_unit:
            if not self._sound:
                self._sound = XMLSound()
            self._sound.tempo = int(self.beat_unit.value * self.per_minute)

    def _set_xml_beat_unit_dots(self):
        number_of_dots = self.beat_unit.get_number_of_dots()
        current_xml_unit_dots = [ch for ch in self.xml_object.get_children() if isinstance(ch, XMLBeatUnitDot)]
        number_of_superfluous_dots = len(current_xml_unit_dots) - number_of_dots
        if number_of_superfluous_dots > 0:
            for xml_unit_dot in current_xml_unit_dots[:number_of_superfluous_dots]:
                self.xml_object.remove(xml_unit_dot)
        elif number_of_superfluous_dots < 0:
            for _ in range(number_of_superfluous_dots * -1):
                self.xml_object.add_child(XMLBeatUnitDot())
        else:
            pass

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

    @property
    def per_minute(self):
        return self._per_minute

    @per_minute.setter
    def per_minute(self, val):
        self._per_minute = val
        self._set_xml_per_minute()

    @property
    def sound(self):
        return self._sound

    def get_xml_beat_dot_objects(self):
        return [ch for ch in self.get_children() if isinstance(ch, XMLBeatUnitDot)]
