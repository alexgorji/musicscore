import math
from fractions import Fraction
from typing import Union, List, Optional

from musicxml.xmlelement.xmlelement import XMLTimeModification, XMLChord

from musictree.exceptions import ChordAlreadySplitError, ChordCannotSplitError, ChordHasNoParentError, \
    ChordQuarterDurationAlreadySetError, ChordNotesAreAlreadyCreatedError
from musictree.midi import Midi
from musictree.musictree import MusicTree
from musictree.note import Note
from musictree.quarterduration import QuarterDurationMixin, QuarterDuration, _check_quarter_duration


class Chord(MusicTree, QuarterDurationMixin):
    """
    Chord is a sequence of one or more XMLNotes which occur at the same time in a XMLMeasure of a XMLPart.
    :param midis: midi, midis, midi value or midi values. 0 or [0] for a rest.
    :param quarter_duration: int or float for duration counted in quarters (crotchets). 0 for grace note (or chord).
    """
    _ATTRIBUTES = {'midis', 'quarter_duration', 'notes', '_note_attributes', 'offset', 'split', '_voice', 'ties'}

    def __init__(self, midis: Optional[Union[List[Union[float, int]], List[Midi], float, int, Midi]] = None,
                 quarter_duration: Optional[Union[float, int, 'Fraction', QuarterDuration]] = None, offset=0, **kwargs):
        self._midis = None
        self._notes = None
        self._offset = None
        self._ties = []

        self._note_attributes = kwargs
        self.offset = offset
        super().__init__(quarter_duration=quarter_duration)
        self._set_midis(midis)
        self.split = False

    def _update_notes_quarter_duration(self):
        if self.notes is not None:
            for note in self.notes:
                note.quarter_duration = self.quarter_duration

    def _update_notes_pitch_or_rest(self):
        if self.notes:
            len_diff = len(self.notes) - len(self.midis)
            if len_diff > 0:
                to_be_removed = self.notes[len_diff:]
                self._notes = self.notes[:len_diff]
                for note in to_be_removed:
                    note.up.remove(note)
                    note.parent_chord = None
                    del note
            for index, m in enumerate(self.midis):
                if index < len(self.notes):
                    self.notes[index].midi = m
                else:
                    new_note = Note(parent_chord=self, midi=m, quarter_duration=self.quarter_duration)
                    self._notes.append(new_note)
                    self.add_child(new_note)

    def _update_tie(self):
        if self.notes:
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

    def _update_time_modification(self):
        normals = {3: 2, 5: 4, 6: 4, 7: 4, 9: 8, 10: 8, 11: 8, 12: 8, 13: 8, 14: 8, 15: 8}
        types = {8: '32nd', 4: '16th', 2: 'eighth'}
        try:
            normal = normals[self.quarter_duration.denominator]
            for note in self.notes:
                note.xml_time_modification = XMLTimeModification()
                note.xml_time_modification.xml_actual_notes = self.quarter_duration.denominator
                note.xml_time_modification.xml_normal_notes = normal
                note.xml_time_modification.xml_normal_type = types[normal]
        except KeyError:
            pass

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

    @property
    def is_rest(self):
        if self._midis[0].value == 0:
            return True
        else:
            return False

    @property
    def midis(self):
        return self._midis

    @midis.setter
    def midis(self, val):
        self._set_midis(val)

    @property
    def notes(self):
        return self._notes

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, val):
        _check_quarter_duration(val)
        if isinstance(val, QuarterDuration):
            self._offset = val
        else:
            self._offset = QuarterDuration(val)

    @QuarterDurationMixin.quarter_duration.setter
    def quarter_duration(self, val):
        if self._quarter_duration is not None and self.up:
            raise ChordQuarterDurationAlreadySetError('Chord is already attached to a Beat. Quarter Duration cannot be changed any more.')
        if val is not None:
            if self.midis and self.is_rest and val == 0:
                raise ValueError('A rest cannot be a grace note')
            self._set_quarter_duration(val)
            self._update_notes_quarter_duration()

    @property
    def voice(self):
        if not self.up:
            raise ChordHasNoParentError()
        if self.up and self.up.up:
            return self.up.up.value
        else:
            return 1

    def add_tie(self, val):
        if val not in ['start', 'stop']:
            raise ValueError
        if val not in self._ties:
            self._ties.append(val)
            self._update_tie()

    def get_voice_number(self):
        return self.up.up.value

    def get_parent_measure(self):
        return self.up.up.up.up

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
            left_over_chord = split_copy(self, quarter_durations[1])
            current_chord.add_tie('start')
            left_over_chord.add_tie('stop')
            for midi in left_over_chord.midis:
                midi.accidental.show = False
        else:
            left_over_chord = None
        self.up.left_over_chord = left_over_chord
        self.up.up.left_over_chord = left_over_chord

        return output

    def to_rest(self):
        self.midis = [0]

    def to_string(self):
        raise AttributeError("object 'Chord' cannot return a string.")

    def update_notes(self):
        if self._notes:
            raise ChordNotesAreAlreadyCreatedError()
        if not self.up:
            raise ChordHasNoParentError('Chord needs a parent Beat to create notes.')
        self.get_parent_measure().update_divisions()
        self._notes = [Note(parent_chord=self, midi=midi, **self._note_attributes) for midi in self._midis]
        if len(self._notes) > 1:
            self._notes[0].xml_object.add_child(XMLChord())
        self._update_notes_quarter_duration()
        self._update_time_modification()
        self._update_tie()
        for note in self.notes:
            self.add_child(note)

    def __setattr__(self, key, value):
        if key not in self._ATTRIBUTES.union(self.TREE_ATTRIBUTES) and key not in [f'_{attr}' for attr in
                                                                                   self._ATTRIBUTES.union(
                                                                                       self.TREE_ATTRIBUTES)] and key not in self.__dict__:
            if self.notes is not None:
                if isinstance(value, str) or not hasattr(value, '__iter__'):
                    value = [value] * len(self.notes)
                for n, v in zip(self.notes, value):
                    setattr(n, key, v)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, item):
        if not self.notes:
            raise AttributeError(f"AttributeError: 'Chord' object has no attribute '{item}'")
        output = [getattr(n, item) for n in self.notes]
        if output and callable(output[0]):
            raise AttributeError(f"Chord cannot call Note method {item}. Call this method on each note separately")
        return output


def split_copy(chord, new_quarter_duration=None):
    if new_quarter_duration is None:
        new_quarter_duration = chord.quarter_duration.__copy__()
    new_chord = Chord(midis=[m.__deepcopy__() for m in chord.midis], quarter_duration=new_quarter_duration)
    # new_chord._ties = chord._ties[:]
    return new_chord
