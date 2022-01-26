from musicxml.xmlelement.xmlelement import XMLNote, XMLDot, XMLGrace, XMLRest

from musictree.exceptions import NoteTypeError
from musictree.midi import Midi
from musictree.musictree import MusicTree
from musictree.quarterduration import _check_quarter_duration, QuarterDuration
from musictree.util import note_types


class Note(MusicTree):
    _ATTRIBUTES = {'midi', 'quarter_duration', 'voice', 'parent_measure', '_divisions', '_type', '_dots'}

    def __init__(self, midi=Midi(60), quarter_duration=1, voice=1, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLNote(*args, **kwargs)
        self._midi = None
        self._quarter_duration = None
        self._divisions = None
        self._voice = None
        self._type = None
        self._dots = None
        self.parent_measure = None

        self.quarter_duration = quarter_duration
        self.midi = midi
        self.voice = voice

    def _calculate_divisions(self):
        return self._quarter_duration.value.denominator

    @staticmethod
    def _check_xml_duration_value(duration):
        if int(duration) != duration:
            raise ValueError('product of quarter_duration and divisions must be an integer')
        if duration < 0:
            raise ValueError

    def _check_dots(self, numer_of_dots):
        dots = self.xml_object.find_children('XMLDot')
        if numer_of_dots > len(dots):
            diff = numer_of_dots - len(dots)
            while diff:
                self.xml_object.add_child(XMLDot())
                diff -= 1
        elif numer_of_dots < len(dots):
            for dot in dots[numer_of_dots:]:
                dot.get_parent().remove(dot)
        else:
            pass

    def _set_quarter_duration(self, val):
        _check_quarter_duration(val)
        old_quarter_duration = self._quarter_duration
        if isinstance(val, QuarterDuration):
            self._quarter_duration = val
        elif not self._quarter_duration:
            self._quarter_duration = QuarterDuration(val)
        else:
            self._quarter_duration.value = val
        if self._type is None and self._quarter_duration != 0:
            try:
                note_types[self._quarter_duration.value.as_integer_ratio()]
            except KeyError:
                msg = f"A note with quarter_duration {self._quarter_duration} is not writable and must be split."
                self._quarter_duration = old_quarter_duration
                raise NoteTypeError(msg)

    def _update_divisions(self):
        d = self._calculate_divisions()
        if self._divisions is None:
            self._divisions = d
            if self.parent_measure:
                self.parent_measure.update_divisions()
        elif self._divisions != d:
            if self._divisions % d == 0:
                pass
            else:
                self._divisions = d
                if self.parent_measure:
                    self.parent_measure.update_divisions()
        else:
            pass

    def _update_xml_type(self):
        if self._type is None:
            if self.quarter_duration != 0:
                self.xml_type = note_types[self.quarter_duration.value.as_integer_ratio()]
            else:
                self.xml_type = None

    def _update_xml_dots(self):
        if self._dots is None:
            if self.quarter_duration != 0:
                if self.quarter_duration.value.numerator % 3 == 0:
                    self._check_dots(numer_of_dots=1)
                elif True in [self.quarter_duration == x for x in [7, 7 / 2, 7 / 4, 7 / 8, 7 / 16, 7 / 32, 7 / 64]]:
                    self._check_dots(numer_of_dots=2)
                else:
                    self._check_dots(numer_of_dots=0)

    def _update_xml_time_modifications(self):
        pass

    def _update_xml_accidental(self):
        if self.midi.accidental.sign == 'natural':
            self.xml_object.xml_accidental = None
        else:
            self.xml_object.xml_accidental = self.midi.accidental.xml_object

    def _update_xml_duration(self):
        duration = float(self.quarter_duration) * self._divisions
        self._check_xml_duration_value(duration)
        duration = int(duration)
        if duration == 0:
            if self.midi and self.midi.value == 0:
                raise ValueError('A rest cannot be a grace note.')
            self.xml_object.xml_duration = None
            if not self.xml_object.xml_grace:
                self.xml_object.xml_grace = XMLGrace()
        else:
            self.xml_object.xml_grace = None
            self.xml_object.xml_duration = duration

    def _update_xml_pitch_or_rest(self):
        midi = self.midi
        if midi is None:
            self.xml_object.xml_pitch = None
            self.xml_object.xml_rest = None
        else:
            if not isinstance(midi, Midi):
                raise TypeError
            if self.midi.value == 0 and self.quarter_duration == 0:
                raise ValueError('A rest cannot be a grace note.')
            pitch_or_rest = midi.get_pitch_or_rest()
            if isinstance(pitch_or_rest, XMLRest):
                if self.xml_object.xml_pitch:
                    self.xml_object.xml_pitch = None
                self.xml_object.xml_rest = pitch_or_rest
                self.xml_object.xml_notehead = None
            else:
                if self.xml_object.xml_rest:
                    self.xml_object.xml_rest = None
                self.xml_object.xml_pitch = pitch_or_rest

    @property
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        if value is not None:
            self._set_quarter_duration(value)
            self._update_divisions()
            self._update_xml_duration()
            self._update_xml_type()
            self._update_xml_dots()
            self._update_xml_time_modifications()
        else:
            self.xml_object.xml_duration = None

    @property
    def midi(self):
        return self._midi

    @midi.setter
    def midi(self, value):
        self._midi = value if isinstance(value, Midi) or value is None else Midi(value)
        self._update_xml_pitch_or_rest()
        if value is not None:
            self.midi.parent_note = self
            self._update_xml_accidental()

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, val):
        self.xml_object.xml_voice = str(val)
        self._voice = val

    def get_divisions(self):
        return self._divisions

    def set_divisions(self, val):
        if val != self.get_divisions():
            self._check_xml_duration_value(float(self.quarter_duration) * val)
            self._divisions = val
            self._update_xml_duration()
        else:
            self._divisions = val

    def set_dots(self, number_of_dots=None):
        if number_of_dots is None:
            self._update_xml_dots()
        else:
            self._check_dots(number_of_dots)

    def set_type(self, val=None):
        self._type = val
        if val is None:
            self._update_xml_type()
        else:
            self.xml_object.xml_type = val
