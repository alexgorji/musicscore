from typing import Union, List

from quicktions import Fraction

from musictree.exceptions import NoteTypeError
from musictree.midi import Midi
from musictree.musictree import MusicTree
from musictree.note import Note
from musictree.quarterduration import QuarterDuration, _check_quarter_duration


class Chord(MusicTree):
    """
    Chord is a sequence of one or more XMLNotes which occur at the same time in a XMLMeasure of a XMLPart.
    :param midis: midi, midis, midi value or midi values. 0 or [0] for a rest.
    :param quarter_duration: int or float for duration counted in quarters (crotchets). 0 for grace note (or chord).
    """
    _ATTRIBUTES = {'midis', 'quarter_duration', 'voice', 'notes', '_note_attributes'}

    def __init__(self, midis: Union[List[Union[float, int]], List[Midi], float, int, Midi],
                 quarter_duration: Union[float, int, Fraction, QuarterDuration], voice=1, **kwargs):
        super().__init__()
        self._quarter_duration = None
        self._voice = None
        self._midis = None
        self._notes = []

        self._note_attributes = kwargs
        self.voice = voice
        self.quarter_duration = quarter_duration
        self._set_midis(midis)

    def _update_notes_quarter_duration(self):
        for note in self.notes:
            try:
                note.quarter_duration = self.quarter_duration
            except NoteTypeError as err:
                print(f'NoteTypeError in Chord with quarter_duration {self.quarter_duration}')
                print(err)
                break

    def _set_quarter_duration(self, val):
        _check_quarter_duration(val)
        if isinstance(val, QuarterDuration):
            self._quarter_duration = val
        elif not self._quarter_duration:
            self._quarter_duration = QuarterDuration(val)
        else:
            self._quarter_duration.value = val

    def _set_midis(self, midis):
        if isinstance(midis, str):
            raise TypeError
        if hasattr(midis, '__iter__'):
            pass
        else:
            midis = [midis]
        if len(midis) > 1 and 0 in midis:
            raise ValueError('Chord cannot accept a mixed list of midis of rests and pitches or a list of more than one rests.')

        if midis == [0] and self.quarter_duration == 0:
            raise ValueError('A rest cannot be a grace note')

        self._midis = [Midi(v) if not isinstance(v, Midi) else v for v in midis]
        self._notes = [Note(midi, **self._note_attributes,
                            voice=self.voice) for midi in
                       self._midis]
        self._update_notes_quarter_duration()

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
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, val):
        if val is not None:
            self._set_quarter_duration(val)
            self._update_notes_quarter_duration()

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, val):
        self._voice = val
        for note in self.notes:
            note.voice = self.voice

    def to_rest(self):
        self.midis = [0]

    def to_string(self):
        raise AttributeError("object 'Chord' cannot return a string.")

    def __setattr__(self, key, value):
        if key not in self._ATTRIBUTES.union(self.PROPERTIES) and key not in [f'_{attr}' for attr in self._ATTRIBUTES.union(
                self.PROPERTIES)] and key not in self.__dict__:
            if isinstance(value, str) or not hasattr(value, '__iter__'):
                value = [value] * len(self.notes)
            for n, v in zip(self.notes, value):
                setattr(n, key, v)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, item):
        return [getattr(n, item) for n in self.notes]