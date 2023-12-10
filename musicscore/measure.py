import warnings
from typing import List, Optional, Union

from math import trunc

from musicscore.clef import BassClef, TrebleClef
from musicscore.musictree import MusicTree
from musicscore.exceptions import AlreadyFinalizedError, AddChordError
from musicscore.finalize import FinalizeMixin
from musicscore.key import Key
from musicscore.quantize import QuantizeMixin
from musicscore.staff import Staff
from musicscore.time import Time, flatten_times
from musicscore.util import lcm, _chord_is_in_a_repetition, isinstance_as_string
from musicscore.voice import Voice
from musicscore.xmlwrapper import XMLWrapper
from musicxml.xmlelement.xmlelement import XMLMeasure, XMLAttributes, XMLClef, XMLBackup, XMLBarline, XMLPrint, \
    XMLRepeat, XMLEnding

__all__ = ['Measure', 'generate_measures']


class Measure(MusicTree, QuantizeMixin, FinalizeMixin, XMLWrapper):
    """
    Parent type: :obj:`~musicscore.part.Part`

    Child type: :obj:`~musicscore.staff.Staff`
    """

    _ATTRIBUTES = {'number', 'time', 'key', 'clefs', 'quarter_duration', 'barline_style', 'new_system'}
    _ATTRIBUTES = _ATTRIBUTES.union(MusicTree._ATTRIBUTES)
    _ATTRIBUTES = _ATTRIBUTES.union(QuantizeMixin._ATTRIBUTES)
    XMLClass = XMLMeasure

    def __init__(self, number, time=None, *args, **kwargs):
        super().__init__()
        self._updated = False
        self._xml_object = self.XMLClass(*args, **kwargs)
        self.number = number
        self._time = None
        self._key = Key()
        self.time = time
        self._set_attributes()
        self._new_system = False
        self._barlines = {'left': None, 'right': None}

    def _add_chord(self, chord, staff_number=None, voice_number=1):

        voice = self.add_voice(staff_number=staff_number, voice_number=voice_number)
        if not voice.get_children():
            voice.update_beats()
        return voice._add_chord(chord)

    def _set_attributes(self):
        self.xml_object.xml_attributes = XMLAttributes()
        self.xml_object.xml_attributes.xml_divisions = 1

    def _set_clefs(self):
        existing_clefs = self.xml_object.xml_attributes.find_children(XMLClef)
        for existing_clef in existing_clefs:
            existing_clef.up.remove(existing_clef)
        for clef in [c for c in self.clefs if c and c.show is True]:
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

    def _split_not_writable_chords(self):
        """
        Calls :obj:`~musicscore.beat.Beat._split_not_writable_chords()` method of all :obj:`~musicscore.beat.Beat` descendents.
        """
        for b in [beat for staff in self.get_children() for voice in staff.get_children() for beat in
                  voice.get_children()]:
            b._split_not_writable_chords()

    def _update_accidentals(self):

        for staff in self.get_children():
            if staff.show_accidental_signs == 'modern':
                previous_staff = staff.get_previous_staff()
                steps_with_accidentals = set()
                relevant_chords = [ch for ch in staff.get_chords() if not ch.is_rest]
                relevant_chords_not_tied = [ch for ch in relevant_chords if
                                            True not in set(m.is_tied_to_previous for m in ch.midis)]
                for chord in relevant_chords:
                    for midi in chord.midis:
                        step = midi.accidental.get_pitch_parameters()[0]
                        if midi.accidental.show is None:
                            if midi.accidental.sign == 'natural':
                                if step in steps_with_accidentals:
                                    midi.accidental.show = True
                                    steps_with_accidentals.remove(step)
                                elif relevant_chords_not_tied and chord == relevant_chords_not_tied[
                                    0] and previous_staff and step in \
                                        previous_staff.get_last_pitch_steps_with_accidentals():
                                    midi.accidental.show = True
                                else:
                                    midi.accidental.show = False
                            else:
                                if _chord_is_in_a_repetition(chord):
                                    midi.accidental.show = False
                                else:
                                    midi.accidental.show = True
                                    if step not in steps_with_accidentals:
                                        steps_with_accidentals.add(step)
                        elif midi.accidental.sign != 'natural' and step not in steps_with_accidentals:
                            steps_with_accidentals.add(step)
            else:
                raise NotImplementedError(f'{staff.show_accidental_signs} not implemented yet.')

    def _update_attributes(self):
        self._set_key()
        self._set_time()
        self._set_staves()
        self._set_clefs()

    def _update_left_barline(self):
        if self.get_barline(location='left'):
            self.xml_object.add_child(self.get_barline(location='left'))

    def _update_right_barline(self):
        if self.get_barline(location='right'):
            self.xml_object.add_child(self.get_barline(location='right'))

    def _update_clef_numbers(self):
        if len(self.clefs) == 1:
            try:
                self.clefs[0].number = None
            except AttributeError:
                pass
        else:
            n = 1
            for cl in self.clefs:
                cl.number = n
                n += 1

    def _update_default_clefs(self):
        number_of_children = len(self.get_children())

        def _set_default_clef(staff_number, clef):
            staff = self.get_staff(staff_number)
            if staff.clef is None or staff.clef._default is True:
                staff.clef = clef

        if number_of_children == 1:
            _set_default_clef(1, TrebleClef(default=True))
        elif number_of_children == 2:
            _set_default_clef(1, TrebleClef(default=True))
            _set_default_clef(2, BassClef(default=True))
        elif number_of_children == 3:
            _set_default_clef(1, TrebleClef(octave_change=2, default=True))
            _set_default_clef(2, TrebleClef(default=True))
            _set_default_clef(3, BassClef(default=True))
        elif number_of_children == 4:
            _set_default_clef(1, TrebleClef(octave_change=2, default=True))
            _set_default_clef(2, TrebleClef(default=True))
            _set_default_clef(3, BassClef(default=True))
            _set_default_clef(4, BassClef(octave_change=-2, default=True))
        else:
            for index in range(number_of_children):
                if index == 0:
                    _set_default_clef(index + 1, TrebleClef(octave_change=2, default=True))
                elif index == number_of_children - 1:
                    _set_default_clef(index + 1, BassClef(octave_change=-2, default=True))
                elif index < number_of_children / 2:
                    _set_default_clef(index + 1, TrebleClef(default=True))
                else:
                    _set_default_clef(index + 1, BassClef(default=True))

    def _update_divisions(self):
        chord_divisions = {ch.quarter_duration.denominator for ch in self.get_chords()}
        divisions = lcm(list(chord_divisions))
        self.xml_object.xml_attributes.xml_divisions = divisions

    def _update_print(self):
        if self.new_system:
            if self.xml_object.xml_print:
                self.xml_object.xml_print.new_system = 'yes'
            else:
                self.xml_object.xml_print = XMLPrint(new_system='yes')
        else:
            if self.xml_object.xml_print:
                self.xml_object.xml_print.new_system = 'no'

    def _update_score_encoding(self):
        if self.new_system:
            if not isinstance_as_string(self.get_root(), "Score"):
                warnings.warn(
                    f"Measure number {self.number} sets new_system to True but hat no Score as root. Score.new_system must be True for measure's new_system to take effect.")
            else:
                self.get_root().new_system = True
        else:
            self.get_root().new_system = False

    def _update_voice_beats(self):
        for staff in self.get_children():
            for voice in staff.get_children():
                voice.update_beats()

    def _update_xml_notes_backup_and_more(self):
        def add_backup():
            b = XMLBackup()
            d = self.quarter_duration * self.get_divisions()
            if trunc(d) != d:
                raise ValueError
            b.xml_duration = trunc(d)
            self.xml_object.add_child(b)

        for staff in self.get_children():
            if staff != self.get_children()[0]:
                add_backup()
            for index, voice in enumerate(staff.get_children()):
                chords = voice.get_chords()
                if index != 0:
                    add_backup()
                for chord in chords:
                    for xml_direction in chord._xml_directions:
                        self.xml_object.add_child(xml_direction)
                    if chord.clef and chord.clef.show is True:
                        if len(self.get_children()) > 1:
                            chord.clef.number = staff.number
                        attributes = self.xml_object.add_child(XMLAttributes())
                        attributes.add_child(chord.clef.xml_object)
                    for note in chord.notes:
                        self.xml_object.add_child(note.xml_object)
                    for xml_object in chord._after_notes_xml_elements:
                        self.xml_object.add_child(xml_object)

    @property
    def clefs(self) -> List['Clef']:
        """
        :return: :obj:`~musicscore.clef.Clef` objects of children staves.
        """
        return [staff.clef for staff in self.get_children()]

    @property
    def key(self) -> Key:
        """
        :type: :obj:`~musicscore.key.Key`
        :return: :obj:`~musicscore.key.Key`
        """
        return self._key

    @key.setter
    def key(self, val):
        if not isinstance(val, Key):
            raise TypeError
        self._key = val

    @property
    def number(self):
        """
        :type: positive int
        :return: xml_object's number as integer
        :rtype: positive int
        """
        return int(self.xml_object.number)

    @number.setter
    def number(self, val):
        self.xml_object.number = str(val)

    @property
    def new_system(self) -> bool:
        """
        If ``True``: ``new_system`` attribute of self.xml_object's child :obj:`~musicxml.xmlelement.xmlelement.XMLPrint` will be set to ``yes``.
        """
        return self._new_system

    @new_system.setter
    def new_system(self, val):
        if not isinstance(val, bool):
            raise TypeError
        self._new_system = val
        self._update_print()
        self._update_score_encoding()

    @property
    def time(self) -> Time:
        """
        Set and get time. After setting value, parent_measure is set to self and method :obj:`musicscore.voice.Voice.update_beats(
        )` of descendent voices is called.

        :type: Optional[:obj:`~musicscore.time.Time`]
        :type: :obj:`~musicscore.time.Time`
        """
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
    def quarter_duration(self) -> 'QuarterDuration':
        """
        :return: sum of quarter durations defined via property :obj:`time`'s method :obj:`~musicscore.time.Time.get_beats_quarter_durations()`
        :rtype: :obj:`~musicscore.quarterduration.QuarterDuration`
        """
        return sum(self.time.get_beats_quarter_durations())

    def add_child(self, child: Staff) -> Staff:
        """
        - Adds a :obj:`~musicscore.staff.Staff` as a child to measure.
        - If staff number is ``None``, it will determined as length of children + 1.
        - If staff number is already set an is not equal to length of children + 1 a ``ValueError`` is raised.
        - If staff is the first child default clefs are set.
        - :obj:`~musicscore.clef.Clef`'s numbers are updated.

        :param child: :obj:`~musicscore.staff.Staff`, required
        :return: child
        :rtype: :obj:`~musicscore.staff.Staff`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_child')
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

        if self.previous is None:
            self._update_default_clefs()
        self._update_clef_numbers()
        return child

    def add_chord(self, *args, **kwargs):
        raise AddChordError

    def add_staff(self, staff_number: Optional[int] = None) -> 'Staff':
        """
        - Creates and adds a new :obj:`~musicscore.staff.Staff` object as child to measure if it already does not exist.
        - If staff number is greater than length of children + 1 all missing staves are created and added first.

        :param staff_number: ``positive int`` or ``None``. If ``None`` staff number it is determined as length of children + 1.
        :return: new :obj:`~musicscore.staff.Staff`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_staff')
        if staff_number is None:
            staff_number = len(self.get_children()) + 1
        staff_object = self.get_staff(staff_number=staff_number)
        if staff_object is None:
            for _ in range(staff_number - len(self.get_children())):
                new_staff = self.add_child(Staff())
                new_staff.add_child(Voice())
            return new_staff
        return staff_object

    def add_voice(self, *, staff_number: Optional[int] = None, voice_number: Optional[int] = None) -> Voice:
        """
        - Creates and adds a new :obj:`~musicscore.voice.Voice` object as child to the given :obj:`~musicscore.staff.Staff` if it already
          does not exist.
        - :obj:`add_staff()` is called to get or create the given staff.
        - :obj:`musicscore.staff.Staff.add_voice()` is called to add voice to staff.

        :param staff_number: ``positive int`` or ``None``. If ``None`` staff number it is set to 1.
        :param voice_number: ``positive int`` or ``None``. If ``None`` voice_numberit is set to 1.

        :return: new :obj:`~musicscore.voice.Voice`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_voice')
        if staff_number is None:
            staff_number = 1
        if voice_number is None:
            voice_number = 1
        voice_object = self.get_voice(staff_number=staff_number, voice_number=voice_number)
        if voice_object is None:
            staff_object = self.add_staff(staff_number=staff_number)
            return staff_object.add_voice(voice_number=voice_number)
        return voice_object

    def fill_with_rests(self):
        """
        If :obj:`~musicscore.measure.Measure` is not completely filled, it will be filled with rest(s)
        """
        if not self.get_children():
            self.add_staff()
        for staff in self.get_children():
            staff.fill_with_rests()

    def finalize(self):
        """
        finalize can only be called once.

        - It calls the finalize() method of all children.
        - Following updates are triggered: _update_attributes, _update_divisions, _update_left_barline, _update_accidentals, update_xml_backups_notes_directions, _update_right_barline
        - All beats with the property get_quantized set to True will get quantized.

        """

        if self._finalized:
            raise AlreadyFinalizedError(self)

        self.fill_with_rests()
        self._update_attributes()
        self._update_left_barline()
        # self.quantize
        for beat in self.get_beats():
            # if beat.get_quantized:
            #     beat.quantize_quarter_durations()
            beat._split_not_writable_chords()

        self._update_divisions()

        for st in self.get_children():
            if not st._finalized:
                st.finalize()

        self._update_accidentals()
        self._update_xml_notes_backup_and_more()
        self._update_right_barline()
        self._finalized = True

    def get_barline(self, location: str = 'right') -> Optional['XMLBarline']:
        """
        :param location: 'left' or 'right' barline position.
        :return: None or :obj:`~musicxml.xmlelement.xmlelement.XMLBarline`
        """
        try:
            return self._barlines[location]
        except KeyError:
            raise ValueError(f'location {location} not permitted')

    def get_children(self) -> List[Staff]:
        """
        :return: list of added children.
        :rtype: List[:obj:`~musicscore.staff.Staff`]
        """
        return super().get_children()

    def get_divisions(self) -> 'musicxml.xsd.xsdsimpletype.XSDSimpleTypeInteger':
        """
        :return: ``value_`` of existing :obj:`~musicxml.xmlelement.xmlelement.XMLDivisions`
        """
        return self.xml_object.xml_attributes.xml_divisions.value_

    def remove(self, child) -> None:
        number = child.value
        super().remove(child)
        self.clefs.pop(number - 1)

    def set_barline(self, location: str = 'right', style: Optional[str] = None, **kwargs) -> 'XMLBarline':
        """
        :param location: 'left' or 'right' barline position.
        :param style: 'regular', 'dotted', 'dashed', 'heavy', 'light-light', 'light-heavy', 'heavy-light', 'heavy-heavy', 'tick', 'short', 'none'
        :return: created :obj:`~musicxml.xmlelement.xmlelement.XMLBarline`
        """
        bl = XMLBarline(location=location, **kwargs)
        if style:
            bl.xml_bar_style = style
        self._barlines[location] = bl
        return bl

    def set_repeat_barline(self, location: str = 'right', **kwargs) -> 'XMLBarline':
        """
        If barline does not exist a :obj:`~musicxml.xmlelement.xmlelement.XMLBarline` will be added to location. Than a :obj:`~musicxml.xmlelement.xmlelement.XMLRepeat` will be added to it as child.

        :param location: ``left`` or ``right`` barline position. If ``left`` :obj:`~musicxml.xmlelement.xmlelement.XMLBarline`'s ``direction`` is set to ``forward`` otherwise to ``backward``
        :param kwargs: passed on to :obj:`~musicxml.xmlelement.xmlelement.XMLRepeat`
        :return: created or existing :obj:`~musicxml.xmlelement.xmlelement.XMLBarline`
        """
        if location == 'right':
            direction = 'backward'
        else:
            direction = 'forward'
        if not self.get_barline(location=location):
            self.set_barline(location=location)
        bl = self.get_barline(location=location)
        bl.xml_bar_style = 'light-heavy'
        bl.xml_repeat = XMLRepeat(direction=direction, **kwargs)
        return bl

    def set_repeat_ending(self, number: Union[str, int], type: str, **kwargs) -> 'XMLEnding':
        """
        If ``type`` == ``start`` location is set to ``left`` otherwise to ``right``.
        If barline does not exist a :obj:`~musicxml.xmlelement.xmlelement.XMLBarline` will be added to location. Than a :obj:`~musicxml.xmlelement.xmlelement.XMLEnding` will be added to it as child.

        :param number: :obj:`~musicxml.xmlelement.xmlelement.XMLEnding`'s number
        :param kwargs: passed on to :obj:`~musicxml.xmlelement.xmlelement.XMLEnding`
        :return: :obj:`~musicxml.xmlelement.xmlelement.XMLEnding`
        """
        if type == 'start':
            location = 'left'
        else:
            location = 'right'
        if not self.get_barline(location=location):
            self.set_barline(location=location)
        ending = XMLEnding(number=str(number), type=type, **kwargs)
        self.get_barline(location=location).add_child(ending)
        return ending

    def update_chord_accidentals(self) -> None:
        """
        Updates :obj:`musicscore.accidental.Accidental.show` attribute of descendent :obj:`~musicscore.midi.Midi`\s' accidentals.

        :return: None
        """
        for staff in self.get_children():
            for chord in staff.get_chords():
                if chord.all_midis_are_tied_to_previous:
                    for midi in chord.midis:
                        midi.accidental.show = False
                for midi in chord.midis:
                    if midi.accidental.sign == 'natural':
                        midi.accidental.show = False


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
