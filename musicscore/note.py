from typing import Optional, List

from musicscore.musictree import MusicTree
from musicscore.exceptions import NoteTypeError, NoteHasNoParentChordError, NoteMidiHasNoParentChordError
from musicscore.midi import Midi
from musicscore.quarterduration import QuarterDurationMixin
from musicscore.util import note_types
from musicscore.xmlwrapper import XMLWrapper
from musicxml.xmlelement.xmlelement import XMLNote, XMLDot, XMLGrace, XMLRest, XMLTie, XMLNotations, XMLTied, XMLBeam

__all__ = ['Note', 'tie', 'untie']


def tie(*notes):
    """
    Tie notes.
    """
    if hasattr(notes[0], '__iter__'):
        notes = notes[0]
    notes[0].start_tie()
    if len(notes) > 1:
        for note in notes[1:-1]:
            note.stop_tie()
            note.start_tie()
        notes[-1].stop_tie()


def untie(*notes):
    """
    Untie notes.
    """
    if hasattr(notes[0], '__iter__'):
        notes = notes[0]
    notes[0].remove_tie('start')
    if len(notes) > 1:
        for note in notes[1:-1]:
            note.remove_tie('stop')
            note.remove_tie('start')
        notes[-1].remove_tie('stop')


class Note(MusicTree, XMLWrapper, QuarterDurationMixin):
    """
    Parent type: :obj:`~musicscore.chord.Chord`

    Child type: :obj:`~musicscore.midi.Midi`
    """

    _ATTRIBUTES = {'midi', 'quarter_duration', 'parent_chord', 'is_tied', 'is_tied_to_previous'}

    XMLClass = XMLNote

    def __init__(self, midi, quarter_duration=None, *args, **kwargs):
        self._midi = None
        self._parent_chord = midi.parent_chord
        self._xml_object = self.XMLClass(*args, **kwargs)

        super().__init__(quarter_duration=quarter_duration)
        self.midi = midi
        self._parent = self.parent_chord
        self._update_xml_notehead()
        self._update_xml_voice()
        self._update_xml_staff()
        self._update_xml_dots()
        self._update_xml_time_modification()
        self._update_xml_tuplet()
        self._update_xml_beams()

    @staticmethod
    def _check_xml_duration_value(duration):
        if int(duration) != duration:
            raise ValueError(f'product of quarter_duration and divisions {duration} must be an integer')
        if duration < 0:
            raise ValueError

    def _add_child(self, child: Midi) -> Midi:
        """
        Check and add child to list of children. Child's parent is set to self.

        :param child: :obj:`~musicscore.midi.Midi`
        :return: child
        :rtype: :obj:`~musicscore.midi.Midi`
        """
        return super().add_child(child)

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

    def _update_ties(self):
        if 'stop' in self.midi._ties:
            self.stop_tie()
        else:
            self.remove_tie('stop')
        if 'start' in self.midi._ties:
            self.start_tie()
        else:
            self.remove_tie('start')

    def _update_xml_accidental(self):
        self.xml_object.xml_accidental = self.midi.accidental.xml_object

    def _update_xml_beams(self):
        if self.parent_chord and self.parent_chord.beams is not None:
            for number, value in self.parent_chord.beams.items():
                if value in ['forward', 'backward']:
                    value += ' hook'
                self.xml_object.add_child(XMLBeam(number=number, value_=value))

    def _update_xml_dots(self):
        number_of_dots = self.parent_chord.number_of_dots
        if number_of_dots is None:
            number_of_dots = 0
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
        if self.midi.value == 0 and self.quarter_duration == 0:
            raise ValueError('A rest cannot be a grace note.')
        pitch_or_rest = self.midi.get_pitch_or_rest()
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

    def _update_xml_type(self):
        self.xml_type = self.parent_chord.type

    def _update_xml_voice(self):
        self.xml_object.xml_voice = str(self.get_voice_number())

    def _update_xml_notations(self):
        """
        If ``self.xml_object.xml_notations`` has children of types :obj:`~musicxml.xmlelement.xmlelement.XMLArticulation` oder
        :obj:`~musicxml.xmlelement.xmlelement.XMLTechnical`, :obj:`~musicxml.xmlelement.xmlelement.XMLOrnaments`,
        :obj:`~musicxml.xmlelement.xmlelement.XMLDynamics`
        which have no children themselves, these will be removed.
        ``self.xml_object.xml_notations`` will be removed itself if it has no children.

        :return: None
        """
        if self.xml_object.xml_notations:
            if self.xml_object.xml_notations.xml_articulations and not self.xml_object.xml_notations.xml_articulations.get_children():
                self.xml_object.xml_notations.remove(self.xml_object.xml_notations.xml_articulations)

            if self.xml_object.xml_notations.xml_technical and not self.xml_object.xml_notations.xml_technical.get_children():
                self.xml_object.xml_notations.remove(self.xml_object.xml_notations.xml_technical)

            if self.xml_object.xml_notations.xml_ornaments and not self.xml_object.xml_notations.xml_ornaments.get_children():
                self.xml_object.xml_notations.remove(self.xml_object.xml_notations.xml_ornaments)

            if self.xml_object.xml_notations.xml_dynamics and not self.xml_object.xml_notations.xml_dynamics.get_children():
                self.xml_object.xml_notations.remove(self.xml_object.xml_notations.xml_dynamics)

            if not self.xml_object.xml_notations.get_children():
                self.xml_object.remove(self.xml_object.xml_notations)

    def _update_xml_notehead(self):
        self.xml_object.xml_notehead = self.midi.notehead

    def _update_xml_time_modification(self):
        if self.parent_chord.tuplet:
            self.xml_time_modification = self.parent_chord.tuplet.get_xml_time_modification()

    def _update_xml_tuplet(self):
        try:
            xml_tuplet = self.parent_chord.tuplet.get_xml_tuplet()
            if xml_tuplet:
                if not self.xml_notations:
                    self.xml_notations = XMLNotations()
                self.xml_notations.xml_tuplet = xml_tuplet
        except AttributeError:
            pass

    @property
    def is_tied(self) -> bool:
        """
        :return: True if an element :obj:`~musicxml.xmlelement.xmlelement.XMLTie` with type 'start' is under note's xml_object children.
        :rtype: bool
        """
        type_types = [t.type for t in self.xml_object.find_children('XMLTie')]
        if 'start' in type_types:
            return True
        else:
            return False

    @property
    def is_tied_to_next(self) -> bool:
        """
        :return: same as :obj:`~musicscore.musicscore.Note.is_tied`
        """
        return self.is_tied

    @property
    def is_tied_to_previous(self) -> bool:
        """
        :return: True if an element :obj:`~musicxml.xmlelement.xmlelement.XMLTie` with type 'stop' is under note's xml_object children.
        :rtype: bool
        """
        type_types = [t.type for t in self.find_children('XMLTie')]
        if 'stop' in type_types:
            return True
        else:
            return False

    @property
    def midi(self) -> Midi:
        """
        :obj:`~musicscore.chord.Chord`.midi property must be a :obj:`~musicscore.midi.Midi` object with a parent :obj:`~musicscore.chord.Chord`. :obj:`~musicscore.midi.Midi` with value `0` means rest.
        Setting this property will set :obj:`~musicscore.midi.Midi`\s :obj:`~musicscore.midi.Midi.parent_note` to self.

        :return: note's :obj:`~musicscore.midi.Midi`.
        """
        return self._midi

    @midi.setter
    def midi(self, value):
        if not isinstance(value, Midi):
            raise TypeError('Note.midi property must be of type Midi')
        if not value.parent_chord:
            raise NoteMidiHasNoParentChordError
        self._midi = value
        self._midi.parent_note = self
        self._update_xml_pitch_or_rest()
        self._update_xml_accidental()

    @property
    def parent_chord(self) -> 'Chord':
        """
        :return: notes parent. Same as self.up
        """
        return self._parent_chord

    @QuarterDurationMixin.quarter_duration.setter
    def quarter_duration(self, value):
        if value is not None:
            if not self.parent_chord:
                raise NoteHasNoParentChordError()
            self._set_quarter_duration(value)
            self._update_xml_duration()
            self._update_xml_type()
            # self._update_xml_dots()
        else:
            self.xml_object.xml_duration = None

    def get_parent_chord(self):
        """
        returns :obj:`~parent_chord`
        """
        return self.parent_chord

    def get_or_create_xml_notations(self) -> 'XMLNotations':
        """
        If note's ``xml_object`` has no :obj:`~musicxml.xmlelement.xmlelement.XMLNotations` as child this child will be created.

        :return: :obj:`~musicxml.xmlelement.xmlelement.XMLNotations`
        """
        if not self.xml_object.xml_notations:
            self.xml_object.xml_notations = XMLNotations()
        return self.xml_object.xml_notations

    def get_parent_measure(self) -> 'Measure':
        """
        :return: parent :obj:`~musicscore.measure.Measure`
        """
        return self.parent_chord.get_parent_measure()

    def get_staff_number(self) -> int:
        """
        :return: number of parent :obj:`~musicscore.staff.Staff`
        """
        midi_staff_number = self.midi.get_staff_number()
        if midi_staff_number:
            return midi_staff_number

        return self.parent_chord.get_staff_number()

    def get_voice_number(self) -> int:
        """
        :return: number of parent :obj:`~musicscore.voice.Voice`
        """
        return self.get_parent_chord().get_voice_number()

    def remove_tie(self, type: Optional[str] = None) -> None:
        """
        :param type: 'start', 'stop', None: if None and note has :obj:`~musicxml.xmlelement.xmlelement.XMLTie` objects with both types
                      ValueError is raised.
        :return: None
        """
        ties = self.find_children('XMLTie')
        tie_to_be_removed = None
        if len(ties) == 0:
            pass
        elif len(ties) == 1:
            if type is None:
                tie_to_be_removed = ties[0]
            else:
                tie_to_be_removed = ties[0] if ties[0].type == type else None
        elif len(ties) == 2:
            if type is None:
                raise ValueError(
                    'Note has stop and start ties. Specify type=start or type=stop to decide which one should be removed')
            else:
                tie_to_be_removed = [t for t in ties if t.type == type]
                tie_to_be_removed = None if not tie_to_be_removed else tie_to_be_removed[0]
        else:
            raise NotImplementedError
        if tie_to_be_removed:
            try:
                self.midi._ties.remove(tie_to_be_removed.type)
            except KeyError:
                pass
            tied_to_be_removed = \
                [t for t in self.xml_notations.find_children('XMLTied') if t.type == tie_to_be_removed.type][0]
            tie_to_be_removed.up.remove(tie_to_be_removed)
            xml_notations = tied_to_be_removed.up
            xml_notations.remove(tied_to_be_removed)
            if not xml_notations.get_children():
                xml_notations.up.remove(xml_notations)

    def start_tie(self) -> None:
        """
        Start a tie if not already started.
        """
        if not self.is_tied:
            self.xml_object.add_child(XMLTie(type='start'))
            self._set_xml_tied('start')
        self.midi._ties.add('start')

    def stop_tie(self) -> None:
        """
        Stop a tie if not already stopped.
        """
        if self.is_tied_to_previous:
            pass
        elif self.is_tied:
            self.find_children('XMLTie')[0].type = 'stop'
            self.xml_object.add_child(XMLTie(type='start'))
            self._set_xml_tied('stop')
        else:
            self.xml_object.add_child(XMLTie(type='stop'))
            self._set_xml_tied('stop')
        self.midi._ties.add('stop')
