from quicktions import Fraction

from musicscore.musicxml.elements.fullnote import Rest, Event, Pitch, Alter, Chord
from musicscore.musicxml.elements.note import Note, Duration, Grace, Accidental, Notations, Lyric
from musicscore.musicxml.groups.musicdata import Backup
from musicscore.musicxml.types.complextypes.lyric import Text


class TreeBackup(Backup):
    def __init__(self, quarter_duration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quarter_duration = None
        self.quarter_duration = quarter_duration

    @property
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        self._quarter_duration = value

    def update_duration(self, divisions):
        try:
            self.get_children_by_type(Duration)[0].value = int(self.quarter_duration * divisions)
        except IndexError:
            self.add_child(Duration())
            self.duration.value = int(self.quarter_duration * divisions)


class TreeAccidental(Accidental):
    """"""

    def __init__(self, value='natural', show=False, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
        self._note = None
        self._show = None
        self._force_show = None
        self._force_hide = None

        self.show = show

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, value):
        if not isinstance(value, bool):
            raise TypeError('show.value must be of type bool not{}'.format(type(value)))
        self._show = value
        if self._note:
            self._note.update_accidental()

    def set_force_show(self, value):
        self._force_show = value

    def set_force_hide(self, value):
        self._force_hide = value


class TreeNote(Note):
    # todo: Inheritance Chain must be Midi, MidiNote, TreeMidiNote (or TreeNote)
    """
    quarter_duration = 0 means grace note
    """

    def __init__(self, event=Rest(), quarter_duration=1, is_tied=False, parent_chord=None, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_chord = parent_chord
        self._accidental = TreeAccidental(show=False, value='natural')
        self._accidental._note = self
        self._quarter_duration = None
        self.quarter_duration = quarter_duration
        self._event = None
        self.event = event
        self._offset = None
        self._is_tied = False
        self.is_tied = is_tied
        self.is_finger_tremolo = False

    @property
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        if not isinstance(value, int) and not isinstance(value, float) and not isinstance(value, Fraction):
            raise TypeError('quarter_duration must be of type int, float or Fraction not {}'.format(type(value)))

        if value < 0:
            raise ValueError('quarter_duration {} must be zero or positive'.format(value))

        if not isinstance(self.quarter_duration, Fraction):
            self._quarter_duration = Fraction(value).limit_denominator(10000)
        else:
            self._quarter_duration = value

        if value == 0:
            if not self.get_children_by_type(Grace):
                children = self.get_children()[:]
                self.reset_dtd()
                for child in children:
                    if not isinstance(child, Duration):
                        self.add_child(child)
                    else:
                        del child
                self.add_child(Grace())
            # if not self.is_finger_tremolo:
            #
            # else:
            #     self._quarter_duration = 1

    @property
    def previous(self):
        index = self.up.notes.index(self)
        if index == 0:
            return None
        return self.up.notes[index - 1]

    def update_offset(self):
        if self.previous:
            if self.get_children_by_type(Chord):
                output = self.previous.offset
            else:
                output = self.previous.offset + self.previous.quarter_duration
            if self.parent_chord.staff_number:
                output -= (self.parent_chord.staff_number - 1) * self.up.up.quarter_duration
            self._offset = output
        else:
            self._offset = 0

    @property
    def offset(self):
        if self._offset is None:
            self.update_offset()
        return self._offset

    @property
    def end_position(self):
        return self.offset + self.quarter_duration

    @property
    def accidental(self):
        return self._accidental

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, value):
        if not isinstance(value, Event):
            raise TypeError('event.value must be of type  not{}'.format(type(value)))
        try:
            self.remove_child(self._event)
        except ValueError as err:
            print(err)
            pass
        self._event = self.add_child(value)
        self.update_accidental()

    def update_accidental(self):
        _accidentals = {-1.5: 'three-quarters-flat',
                        -1: 'flat',
                        -0.5: 'quarter-flat',
                        0: 'natural',
                        0.5: 'quarter-sharp',
                        1: 'sharp',
                        1.5: 'three-quarters-sharp',
                        2: 'double-sharp'
                        }
        accidental = self.get_children_by_type(type_=TreeAccidental)
        if self._accidental.show:
            if isinstance(self.event, Pitch):
                alter = self.event.get_children_by_type(type_=Alter)
                if not alter:
                    self.event.add_child(Alter(0))

                accidental_value = _accidentals[self.event.alter.value]
                if accidental:
                    accidental[0].value = accidental_value
                else:
                    self._accidental.value = accidental_value
                    self.add_child(self._accidental)
        else:
            if accidental:
                self.remove_child(accidental[0])

    def _add_notations(self, notation):
        try:
            notations = self.get_children_by_type(Notations)[0]
        except IndexError:
            notations = self.add_child(Notations())

        notations.add_child(notation)

    def update_duration(self, divisions):
        try:
            self.duration.value = int(self.quarter_duration * divisions)
        except AttributeError:
            self.add_child(Duration())
            self.duration.value = int(self.quarter_duration * divisions)

    def add_lyric(self, text, number=1, **kwargs):
        lyric = self.add_child(Lyric(number=str(number), **kwargs))
        lyric.add_child(Text(str(text)))
        return lyric
