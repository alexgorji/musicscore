from fractions import Fraction
from typing import Union, List, Optional

from musicxml.xmlelement.xmlelement import XMLChord, XMLLyric, XMLDirection, XMLDirectionType, XMLDynamics, XMLNotations, \
    XMLArticulations, XMLTechnical

from musictree.dynamics import Dynamics
from musictree.exceptions import ChordAlreadySplitError, ChordCannotSplitError, ChordHasNoParentError, \
    ChordQuarterDurationAlreadySetError, ChordNotesAreAlreadyCreatedError
from musictree.midi import Midi
from musictree.core import MusicTree
from musictree.note import Note
from musictree.quarterduration import QuarterDurationMixin, QuarterDuration
from musictree.util import XML_ARTICULATION_CLASSES, XML_TECHNICAL_CLASSES


class Chord(MusicTree, QuarterDurationMixin):
    """
    Chord is a sequence of one or more XMLNotes which occur at the same time in a XMLMeasure of a XMLPart.
    :param midis: Midi, Midi.value, [Midi, Midi.value] 0 or [0] for a rest.
    :param quarter_duration: int, float, Fraction, QuarterDuration for duration counted in quarters (crotchets). 0 for grace note (or
    chord).
    """
    _ATTRIBUTES = {'midis', 'quarter_duration', 'notes', '_note_attributes', 'offset', 'split', 'voice', '_lyrics', 'ties',
                   '_notes_are_set', '_directions', 'xml_directions', 'xml_articulations', 'xml_technicals'}

    def __init__(self, midis: Optional[Union[List[Union[float, int]], List[Midi], float, int, Midi]] = None,
                 quarter_duration: Optional[Union[float, int, 'Fraction', QuarterDuration]] = None, **kwargs):
        self._midis = None
        self._ties = []
        self._lyrics = []
        self._directions = {'above': [], 'below': []}
        self.xml_directions = []
        self.xml_articulations = []
        self.xml_technicals = []

        self._note_attributes = kwargs
        self._notes_are_set = False
        super().__init__(quarter_duration=quarter_duration)
        self._set_midis(midis)
        self.split = False

    def _set_midis(self, midis):
        if isinstance(midis, str):
            raise TypeError
        if hasattr(midis, '__iter__'):
            pass
        elif midis is None:
            midis = []
        else:
            midis = [midis]
        if len(midis) > 1 and 0 in midis:
            raise ValueError('Chord cannot accept a mixed list of midis of rests and pitches or a list of more than one rests.')

        if 0 in midis and self.quarter_duration == 0:
            raise ValueError('A rest cannot be a grace note')
        self._midis = [Midi(v) if not isinstance(v, Midi) else v for v in midis]
        self._update_notes_pitch_or_rest()

    def _update_directions(self):
        def _add_dynamics(list_of_dynamics, xml_direction):
            for dynamics in list_of_dynamics:
                dt = xml_direction.add_child(XMLDirectionType())
                dyn = dt.xml_dynamics = XMLDynamics()
                dyn.add_child(dynamics.xml_object)

        for placement in self._directions:
            direction_types = self._directions[placement]
            for direction_type in direction_types:
                d = XMLDirection(placement=placement)
                self.xml_directions.append(d)
                if direction_type[0] == 'dynamics':
                    _add_dynamics(list_of_dynamics=direction_type[1], xml_direction=d)
                else:
                    raise NotImplementedError

    def _check_xml_notations(self, note):
        if not note.xml_notations:
            note.xml_notations = XMLNotations()

    def _update_articulations(self):
        n = self.notes[0]
        if self.xml_articulations:
            self._check_xml_notations(note=n)
            if not n.xml_notations.xml_articulations:
                a = n.xml_notations.xml_articulations = XMLArticulations()
            else:
                a = n.xml_notations.xml_articulations
            for xml_articulation in self.xml_articulations:
                a.add_child(xml_articulation)

    def _update_technicals(self):
        n = self.notes[0]

        if self.xml_technicals:
            self._check_xml_notations(note=n)
            if not n.xml_notations.xml_technical:
                t = n.xml_notations.xml_technical = XMLTechnical()
            else:
                t = n.xml_notations.xml_technical
            for xml_technical in self.xml_technicals:
                t.add_child(xml_technical)

    def _update_notes(self):
        if self.get_children():
            raise ChordNotesAreAlreadyCreatedError()
        if not self.up:
            raise ChordHasNoParentError('Chord needs a parent Beat to create notes.')
        self.get_parent_measure()._update_divisions()
        notes = [Note(parent_chord=self, midi=midi, **self._note_attributes) for midi in self._midis]
        if len(notes) > 1:
            notes[0].xml_object.add_child(XMLChord())
        for note in notes:
            self.add_child(note)
        for lyric in self._lyrics:
            notes[0].xml_object.xml_lyric = lyric
        self._notes_are_set = True
        self._update_notes_quarter_duration()
        self._update_tie()
        self._update_directions()
        self._update_articulations()
        self._update_technicals()

    def _update_notes_quarter_duration(self):
        for note in self.notes:
            note.quarter_duration = self.quarter_duration

    def _update_notes_pitch_or_rest(self):
        if self.notes:
            len_diff = len(self.notes) - len(self.midis)
            if len_diff > 0:
                to_be_removed = self.notes[len_diff:]
                for note in to_be_removed:
                    note.up.remove(note)
                    note.parent_chord = None
                    del note
            for index, m in enumerate(self.midis):
                if index < len(self.notes):
                    self.notes[index].midi = m
                else:
                    new_note = Note(parent_chord=self, midi=m, quarter_duration=self.quarter_duration)
                    self.add_child(new_note)

    def _update_tie(self):
        if not self._ties:
            for note in self.notes:
                note.remove_tie()
        else:
            if 'stop' in self._ties:
                for note in self.notes:
                    note.stop_tie()
            if 'start' in self._ties:
                for note in self.notes:
                    note.start_tie()

    @property
    def is_rest(self):
        """
        :return bool: True if Chord represents a rest, False if otherwise.
        """
        if self._midis[0].value == 0:
            return True
        else:
            return False

    @property
    def midis(self):
        """
        >>> ch = Chord(midis=60)
        >>> [type(m) for m in ch.midis]
        [<class 'musictree.midi.Midi'>]
        >>> [m.value for m in ch.midis]
        [60]
        >>> ch = Chord(midis=[60, Midi(40)])
        >>> [m.value for m in ch.midis]
        [60, 40]
        >>> Chord([0, 60])
        Traceback (most recent call last):
        ...
        ValueError: Chord cannot accept a mixed list of midis of rests and pitches or a list of more than one rests.

        :return: list of midis
        """
        return self._midis

    @midis.setter
    def midis(self, val):
        self._set_midis(val)

    @property
    def notes(self):
        """
        :return: Chord.get_children() which are of type Note.
        """
        return self.get_children()

    @property
    def offset(self):
        """
        :return: Offset in Chord's parent Beat
        :rtype: QuarterDuration
        """
        if not self.up:
            return None
        elif self.previous is None:
            return 0
        else:
            return self.previous.offset + self.previous.quarter_duration

    @QuarterDurationMixin.quarter_duration.setter
    def quarter_duration(self, val):
        if self._quarter_duration is not None and self.up:
            raise ChordQuarterDurationAlreadySetError('Chord is already attached to a Beat. Quarter Duration cannot be changed any more.')
        if val is not None:
            if self.midis and self.is_rest and val == 0:
                raise ValueError('A rest cannot be a grace note')
            self._set_quarter_duration(val)
            if self._notes_are_set:
                self._update_notes_quarter_duration()

    @property
    def voice(self):
        if not self.up:
            raise ChordHasNoParentError()
        if self.up and self.up.up:
            return self.up.up.number
        else:
            return 1

    def add_tie(self, val):
        """
        :param val: 'start' or 'stop'
        :return: None
        :meta public:
        """
        if val not in ['start', 'stop']:
            raise ValueError
        if val not in self._ties:
            self._ties.append(val)
            self._update_tie()

    def add_articulation(self, xml_articulation_object):
        if xml_articulation_object.__class__ not in XML_ARTICULATION_CLASSES:
            raise TypeError
        self.xml_articulations.append(xml_articulation_object)

    def add_technical(self, xml_technical_object):
        if xml_technical_object.__class__ not in XML_TECHNICAL_CLASSES:
            raise TypeError
        self.xml_technicals.append(xml_technical_object)

    def add_dynamics(self, dynamics, placement='below'):
        dynamics_list = [dynamics] if isinstance(dynamics, str) or not hasattr(dynamics, '__iter__') else list(dynamics)
        dynamics_object_list = [d if isinstance(d, Dynamics) else Dynamics(d) for d in dynamics_list]
        self._directions[placement].append(('dynamics', dynamics_object_list))

    def add_lyric(self, text):
        l = XMLLyric()
        l.xml_text = str(text)
        self._lyrics.append(l)
        return l

    def get_voice_number(self):
        return self.up.up.number

    def get_staff_number(self):
        return self.up.up.up.number

    def get_parent_measure(self):
        return self.up.up.up.up

    def has_same_pitches(self, other):
        if not isinstance(other, Chord):
            raise TypeError
        if self.is_rest or other.is_rest:
            raise TypeError('Rest cannot use method has_same_pitches.')
        if [m.value for m in self.midis] != [m.value for m in other.midis]:
            return False
        for m1, m2 in zip(self.midis, other.midis):
            if m1.accidental.show != m2.accidental.show:
                return False
            if m1.accidental.get_pitch_parameters() != m2.accidental.get_pitch_parameters():
                return False
        return True

    def split_beatwise(self, beats):
        voice_set = {beat.up for beat in beats}
        if len(voice_set) != 1:
            raise ChordCannotSplitError('Beats have must have a single Voice as common ancestor.')

        voice = voice_set.pop()
        if voice is None:
            raise ChordCannotSplitError('Beats have no parent.')

        if voice.get_children()[voice.get_children().index(beats[0]): voice.get_children().index(beats[-1]) + 1] != beats:
            raise ChordCannotSplitError("Beats as Voice's children has another order as input list of beats")

        if beats[0] != voice.get_current_beat():
            raise ChordAlreadySplitError('First beat must be the next beat in voice which can accept chords.')
        if beats[-1] != voice.get_children()[-1]:
            raise ChordAlreadySplitError('Last beat must be the last beat in voice.')
        quarter_durations = self.quarter_duration.get_beatwise_sections(
            offset=beats[0].filled_quarter_duration, beats=beats)
        self.quarter_duration = quarter_durations[0][0]
        self.split = True
        voice.get_current_beat().add_child(self)
        current_chord = self
        output = [self]
        for qd in quarter_durations[0][1:]:
            copied = split_copy(self, qd)
            copied.split = True
            voice.get_current_beat().add_child(copied)
            current_chord.add_tie('start')
            copied.add_tie('stop')
            for midi in copied.midis:
                midi.accidental.show = False
            current_chord = copied
            output.append(current_chord)
        if quarter_durations[1]:
            leftover_chord = split_copy(self, quarter_durations[1])
            current_chord.add_tie('start')
            leftover_chord.add_tie('stop')
            for midi in leftover_chord.midis:
                midi.accidental.show = False
        else:
            leftover_chord = None
        self.up.leftover_chord = leftover_chord
        self.up.up.leftover_chord = leftover_chord

        return output

    def to_rest(self):
        self.midis = [0]

    def to_string(self):
        raise AttributeError("object 'Chord' cannot return a string.")

    def __setattr__(self, key, value):
        if key not in self._ATTRIBUTES.union(self._TREE_ATTRIBUTES) and key not in [f'_{attr}' for attr in
                                                                                    self._ATTRIBUTES.union(
                                                                                       self._TREE_ATTRIBUTES)] and key not in self.__dict__:
            if self.notes:
                if isinstance(value, str) or not hasattr(value, '__iter__'):
                    value = [value] * len(self.notes)
                for n, v in zip(self.notes, value):
                    setattr(n, key, v)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, item):
        if not self._notes_are_set:
            raise AttributeError(f"AttributeError: 'Chord' object has no attribute '{item}'")
        output = [getattr(n, item) for n in self.notes]
        if output and callable(output[0]):
            raise AttributeError(f"Chord cannot call Note method {item}. Call this method on each note separately")
        return output


def split_copy(chord, new_quarter_duration=None):
    if new_quarter_duration is None:
        new_quarter_duration = chord.quarter_duration.__copy__()
    new_chord = Chord(midis=[m.__deepcopy__() for m in chord.midis], quarter_duration=new_quarter_duration)
    return new_chord


def group_chords(chords, quarter_durations):
    if sum(c.quarter_duration for c in chords) != sum(quarter_durations):
        raise ValueError
    output = []
    for _ in quarter_durations:
        output.append([])
    index = 0
    current_quarter_duration = quarter_durations[0]
    for ch in chords:
        output[index].append(ch)
        current_sum = sum(c.quarter_duration for c in output[index])
        if current_sum < current_quarter_duration:
            pass
        elif current_sum == current_quarter_duration:
            index += 1
            if index == len(quarter_durations):
                pass
            else:
                current_quarter_duration = quarter_durations[index]
        else:
            return None
    return output
