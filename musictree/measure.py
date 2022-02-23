from musicxml.xmlelement.xmlelement import XMLMeasure, XMLAttributes, XMLDivisions, XMLKey, XMLClef, XMLBackup

from musictree.clef import Clef, BaseClef, TrebleClef
from musictree.key import Key
from musictree.musictree import MusicTree
from musictree.staff import Staff
from musictree.time import Time, flatten_times
from musictree.util import lcm
from musictree.voice import Voice
from musictree.xmlwrapper import XMLWrapper


class Measure(MusicTree, XMLWrapper):
    _ATTRIBUTES = {'number', 'time', 'key', 'clefs', 'quarter_duration'}
    XMLClass = XMLMeasure

    def __init__(self, number, time=None, *args, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(*args, **kwargs)
        self.number = number
        self._time = None
        self._key = Key()
        self.time = time
        self._set_attributes()

    def _set_attributes(self):
        self.xml_object.xml_attributes = XMLAttributes()
        self.xml_object.xml_attributes.xml_divisions = 1

    def _set_clefs(self):
        existing_clefs = self.xml_object.xml_attributes.find_children(XMLClef)
        for existing_clef in existing_clefs:
            existing_clef.up.remove(existing_clef)
        for clef in [c for c in self.clefs if c.show is True]:
            self.xml_object.xml_attributes.add_child(clef.xml_object)

    def _set_key(self):
        if self.key.show is True:
            self.xml_object.xml_attributes.xml_key = self.key.xml_object
        else:
            self.xml_object.xml_attributes.xml_key = None

    def _set_staves(self):
        if len(self.get_children()) > 1:
            self.xml_object.xml_attributes.xml_staves = len(self.get_children())
        else:
            self.xml_object.xml_attributes.xml_staves = None

    def _set_time(self):
        if self.time.show is True:
            self.xml_object.xml_attributes.xml_time = self.time.xml_object
        else:
            self.xml_object.xml_attributes.xml_time = None

    def _update_accidentals(self):
        def chord_is_in_a_repetition(chord):
            if chord.quarter_duration <= 1.5:
                my_index = chord.up.up.get_chords().index(chord)
                if my_index > 0:
                    previous_chord = chord.up.up.get_chords()[my_index - 1]
                    if previous_chord.quarter_duration < -1.5 and chord.has_same_pitches(previous_chord):
                        return True
            return False

        for staff in self.get_children():
            previous_staff = staff.get_previous_staff()
            steps_with_accidentals = set()
            relevant_chords = [ch for ch in staff.get_chords() if not ch.is_rest]
            relevant_chords_not_tied = [ch for ch in relevant_chords if 'stop' not in ch._ties]
            for chord in relevant_chords:
                for midi in chord.midis:
                    step = midi.accidental.get_pitch_parameters()[0]
                    if midi.accidental.show is None:
                        if midi.accidental.sign == 'natural':
                            if step in steps_with_accidentals:
                                midi.accidental.show = True
                                steps_with_accidentals.remove(step)
                            elif chord == relevant_chords_not_tied[0] and previous_staff and step in \
                                    previous_staff.get_last_steps_with_accidentals():
                                midi.accidental.show = True
                            else:
                                midi.accidental.show = False
                        else:
                            if chord_is_in_a_repetition(chord):
                                midi.accidental.show = False
                            else:
                                midi.accidental.show = True
                                if step not in steps_with_accidentals:
                                    steps_with_accidentals.add(step)
                    elif midi.accidental.sign != 'natural' and step not in steps_with_accidentals:
                        steps_with_accidentals.add(step)

    def _update_attributes(self):
        self._set_key()
        self._set_time()
        self._set_staves()
        self._set_clefs()

    def _update_clef_numbers(self):
        if len(self.clefs) == 1:
            self.clefs[0].number = None
        else:
            n = 1
            for cl in self.clefs:
                cl.number = n
                n += 1

    def _update_default_clefs(self):
        number_of_children = len(self.get_children())
        if number_of_children == 1:
            self.get_children()[0].default_clef = TrebleClef()
        elif number_of_children == 2:
            self.get_children()[0].default_clef = TrebleClef()
            self.get_children()[1].default_clef = BaseClef()
        elif number_of_children == 3:
            self.get_children()[0].default_clef = TrebleClef(octave_change=2)
            self.get_children()[1].default_clef = TrebleClef()
            self.get_children()[2].default_clef = BaseClef()
        elif number_of_children == 4:
            self.get_children()[0].default_clef = TrebleClef(octave_change=2)
            self.get_children()[1].default_clef = TrebleClef()
            self.get_children()[2].default_clef = BaseClef()
            self.get_children()[3].default_clef = BaseClef(octave_change=-2)
        else:
            for index, child in enumerate(self.get_children()):
                if index == 0:
                    child.default_clef = TrebleClef(octave_change=2)
                elif index == number_of_children - 1:
                    child.default_clef = BaseClef(octave_change=-2)
                elif index < number_of_children / 2:
                    child.default_clef = TrebleClef()
                else:
                    child.default_clef = BaseClef()

    def _update_divisions(self):
        chord_divisions = {ch.quarter_duration.denominator for ch in self.get_chords()}
        divisions = lcm(list(chord_divisions))
        self.xml_object.xml_attributes.xml_divisions = divisions

    def _update_voice_beats(self):
        for staff in self.get_children():
            for voice in staff.get_children():
                voice.update_beats()

    def _update_xml_notes(self):

        def reset_notes():
            current_xml_notes = self.xml_object.find_children('XMLNote')
            current_xml_backups = self.xml_object.find_children('XMLBackup')
            for note in current_xml_notes:
                note.up.remove(note)
            for backup in current_xml_backups:
                backup.up.remove(backup)

        def add_backup():
            b = XMLBackup()
            d = self.quarter_duration * self.get_divisions()
            if int(d) != d:
                raise ValueError
            b.xml_duration = int(d)
            self.xml_object.add_child(b)

        reset_notes()
        self._update_divisions()
        for beat in [b for staff in self.get_children() for voice in staff.get_children() for b in voice.get_children()]:
            beat._update_xml_notes()
        self._update_accidentals()
        for staff in self.get_children():
            if staff != self.get_children()[0]:
                add_backup()
            for index, voice in enumerate(staff.get_children()):
                chords = voice.get_chords()
                if index != 0:
                    add_backup()
                for chord in chords:
                    for xml_direction in chord.xml_directions:
                        self.xml_object.add_child(xml_direction)
                    for note in chord.notes:
                        self.xml_object.add_child(note.xml_object)

    @property
    def clefs(self):
        return [staff.clef for staff in self.get_children()]

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, val):
        if not isinstance(val, Key):
            raise TypeError
        self._key = val

    @property
    def number(self):
        return int(self.xml_object.number)

    @number.setter
    def number(self, val):
        self.xml_object.number = str(val)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, val):
        if val is not None and not isinstance(val, Time):
            raise TypeError()
        if val is None:
            val = Time()
        self._time = val
        self._time.parent_measure = self
        self._update_voice_beats()

    @property
    def quarter_duration(self):
        return sum(self.time.get_beats_quarter_durations())

    def add_child(self, child):
        self._check_child_to_be_added(child)

        if child.number is not None and child.number != len(self.get_children()) + 1:
            raise ValueError(f'Staff number must be None or {len(self.get_children()) + 1}')
        if child.number is None:
            if not self.get_children():
                pass
            elif len(self.get_children()) == 1:
                self.get_children()[0].number = 1
                child.number = len(self.get_children()) + 1
            else:
                child.number = len(self.get_children()) + 1

        child._parent = self
        self._children.append(child)

        self._update_default_clefs()
        self._update_clef_numbers()
        return child

    def add_chord(self, chord, *, staff_number=None, voice_number=1):
        voice = self.add_voice(staff_number=staff_number, voice_number=voice_number)
        return voice.add_chord(chord)

    def add_staff(self, staff_number=None):
        if staff_number is None:
            staff_number = len(self.get_children()) + 1
        staff_object = self.get_staff(staff_number=staff_number)
        if staff_object is None:
            for _ in range(staff_number - len(self.get_children())):
                new_staff = self.add_child(Staff())
                new_staff.add_child(Voice())
            return new_staff
        return staff_object

    def add_voice(self, *, staff_number=None, voice_number=1):
        if staff_number is None:
            staff_number = 1
        voice_object = self.get_voice(staff_number=staff_number, voice_number=voice_number)
        if voice_object is None:
            staff_object = self.add_staff(staff_number=staff_number)
            return staff_object.add_voice(voice_number=voice_number)
        return voice_object

    def get_divisions(self):
        return self.xml_object.xml_attributes.xml_divisions.value_

    def get_voice(self, *, staff_number=1, voice_number=1):
        staff_object = self.get_staff(staff_number=staff_number)
        if staff_object:
            for child in staff_object.get_children():
                if child.number == voice_number:
                    return child

    def remove(self, child) -> None:
        number = child.value
        super().remove(child)
        self.clefs.pop(number - 1)

    def split_not_writable_chords(self):
        for b in [beat for staff in self.get_children() for voice in staff.get_children() for beat in voice.get_children()]:
            b.split_not_writable_chords()

    def update_chord_accidentals(self):
        for staff in self.get_children():
            for chord in staff.get_chords():
                if 'stop' in chord._ties:
                    for midi in chord.midis:
                        midi.accidental.show = False
                for midi in chord.midis:
                    if midi.accidental.sign == 'natural':
                        midi.accidental.show = False

    def update(self):
        self._update_attributes()
        self._update_xml_notes()


def generate_measures(times, first_number=1):
    """
    :param [Time, ratio] times: list containing time objects or ratios (1, 4)
    :param int first_number: first measure number
    :return [Measure]: measures
    """
    times = flatten_times(times)
    output = []
    for index, time in enumerate(times):
        output.append(Measure(first_number + index, time=time))
    return output
