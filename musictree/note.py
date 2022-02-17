from musicxml.xmlelement.xmlelement import XMLNote, XMLDot, XMLGrace, XMLRest, XMLTie, XMLNotations, XMLTied

from musictree.exceptions import NoteTypeError, NoteHasNoParentChordError
from musictree.midi import Midi
from musictree.musictree import MusicTree
from musictree.quarterduration import QuarterDurationMixin
from musictree.util import note_types
from musictree.xmlwrapper import XMLWrapper


def tie(*notes):
    notes[0].start_tie()
    if len(notes) > 1:
        for note in notes[1:-1]:
            note.stop_tie()
            note.start_tie()
        notes[-1].stop_tie()


def untie(*notes):
    notes[0].remove_tie('start')
    if len(notes) > 1:
        for note in notes[1:-1]:
            note.remove_tie('stop')
            note.remove_tie('start')
        notes[-1].remove_tie('stop')


class Note(MusicTree, XMLWrapper, QuarterDurationMixin):
    _ATTRIBUTES = {'midi', 'quarter_duration', 'parent_chord', '_type', 'number_of_dots', 'is_tied', 'is_tied_to_previous', '_parent'}

    def __init__(self, parent_chord, midi=None, quarter_duration=None, *args, **kwargs):
        self._parent_chord = parent_chord
        self._xml_object = XMLNote(*args, **kwargs)
        self._update_xml_voice()
        self._update_xml_staff()
        self._midi = None
        self._type = None
        self._number_of_dots = None
        super().__init__(quarter_duration=quarter_duration)
        self.midi = midi
        self._parent = self.parent_chord

    @staticmethod
    def _check_xml_duration_value(duration):
        if int(duration) != duration:
            raise ValueError(f'product of quarter_duration and divisions {duration} must be an integer')
        if duration < 0:
            raise ValueError

    @property
    def number_of_dots(self):
        return self._number_of_dots

    @number_of_dots.setter
    def number_of_dots(self, val):
        self._number_of_dots = val

    def _check_dots(self, number_of_dots):
        dots = self.xml_object.find_children('XMLDot')
        if number_of_dots > len(dots):
            diff = number_of_dots - len(dots)
            while diff:
                self.xml_object.add_child(XMLDot())
                diff -= 1
        elif number_of_dots < len(dots):
            for dot in dots[number_of_dots:]:
                dot.get_parent().remove(dot)
        else:
            pass

    def _set_quarter_duration(self, val):
        old_quarter_duration = self._quarter_duration
        super()._set_quarter_duration(val)
        if self._type is None and self._quarter_duration != 0:
            try:
                note_types[self._quarter_duration.as_integer_ratio()]
            except KeyError:
                msg = f"A note with quarter_duration {self._quarter_duration} and offset {self.up.offset} is not writable and must be " \
                      f"split."
                self._quarter_duration = old_quarter_duration
                raise NoteTypeError(msg)

    def _set_xml_tied(self, val):
        if not self.xml_notations:
            self.xml_notations = XMLNotations()
        tied_xml_objects = self.xml_notations.find_children('XMLTied')
        tied_xml_types = [t.type for t in tied_xml_objects]
        if val in tied_xml_types:
            pass
        elif val == 'stop' and 'start' in tied_xml_types:
            tied_xml_objects[0].type = 'stop'
            self.xml_notations.add_child(XMLTied(type='start'))
        else:
            self.xml_notations.add_child(XMLTied(type=val))

    def _update_xml_type(self):
        if self._type is None:
            if self.quarter_duration != 0:
                self.xml_type = note_types[self.quarter_duration.as_integer_ratio()]
            else:
                self.xml_type = None

    def _update_xml_accidental(self):
        self.xml_object.xml_accidental = self.midi.accidental.xml_object

    def _update_xml_duration(self):
        duration = float(self.quarter_duration) * self.get_parent_measure().get_divisions()
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

    def _update_xml_staff(self):
        self.xml_object.xml_staff = self.get_staff_number()

    def _update_xml_voice(self):
        self.xml_object.xml_voice = str(self.get_voice_number())

    @property
    def is_tied(self):
        type_types = [t.type for t in self.find_children('XMLTie')]
        if 'start' in type_types:
            return True
        else:
            return False

    @property
    def is_tied_to_next(self):
        return self.is_tied

    @property
    def is_tied_to_previous(self):
        type_types = [t.type for t in self.find_children('XMLTie')]
        if 'stop' in type_types:
            return True
        else:
            return False

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
    def parent_chord(self):
        return self._parent_chord

    @QuarterDurationMixin.quarter_duration.setter
    def quarter_duration(self, value):
        if value is not None:
            if not self.parent_chord:
                raise NoteHasNoParentChordError()
            self._set_quarter_duration(value)
            self._update_xml_duration()
            self._update_xml_type()
        else:
            self.xml_object.xml_duration = None

    @property
    def voice(self):
        return self._voice

    def get_parent_measure(self):
        return self.parent_chord.get_parent_measure()

    def get_staff_number(self):
        return self.parent_chord.get_staff_number()

    def get_voice_number(self):
        return self.parent_chord.get_voice_number()

    def set_dots(self, number_of_dots):
        self._number_of_dots = number_of_dots
        self._check_dots(number_of_dots)

    def set_type(self, val=None):
        self._type = val
        if val is None:
            self._update_xml_type()
        else:
            self.xml_object.xml_type = val

    def start_tie(self):
        if not self.is_tied:
            self.xml_object.add_child(XMLTie(type='start'))
            self._set_xml_tied('start')

    def stop_tie(self):
        if self.is_tied_to_previous:
            pass
        elif self.is_tied:
            self.find_children('XMLTie')[0].type = 'stop'
            self.xml_object.add_child(XMLTie(type='start'))
            self._set_xml_tied('stop')
        else:
            self.xml_object.add_child(XMLTie(type='stop'))
            self._set_xml_tied('stop')

    def remove_tie(self, type_=None):
        ties = self.find_children('XMLTie')
        tie_to_be_removed = None
        if len(ties) == 0:
            pass
        elif len(ties) == 1:
            if type_ is None:
                tie_to_be_removed = ties[0]
            else:
                tie_to_be_removed = ties[0] if ties[0].type == type_ else None
        elif len(ties) == 2:
            if type_ is None:
                raise ValueError('Note has stop and start ties. Specify type_=start or type_=stop to decide which one should be removed')
            else:
                tie_to_be_removed = [t for t in ties if t.type == type_]
                tie_to_be_removed = None if not tie_to_be_removed else tie_to_be_removed[0]
        else:
            raise NotImplementedError
        if tie_to_be_removed:
            tied_to_be_removed = [t for t in self.xml_notations.find_children('XMLTied') if t.type == tie_to_be_removed.type][0]
            tie_to_be_removed.up.remove(tie_to_be_removed)
            xml_notations = tied_to_be_removed.up
            xml_notations.remove(tied_to_be_removed)
            if not xml_notations.get_children():
                xml_notations.up.remove(xml_notations)
