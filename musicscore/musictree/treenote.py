from quicktions import Fraction

from musicscore.musicxml.elements.fullnote import Rest, Event, Pitch, Alter
from musicscore.musicxml.elements.note import Note, Dot, Duration, Type, Grace, Accidental, Tie, Notations
from musicscore.musicxml.types.complextypes.notations import Tied


class TreeAccidental(Accidental):
    """"""

    def __init__(self, value='natural', show=False, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
        self._note = None
        self._show = None
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


class TreeNote(Note):
    """
    quarter_duration = 0 means grace note
    """

    def __init__(self, event=Rest(), quarter_duration=1, is_tied=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._accidental = TreeAccidental(show=False, value='natural')
        self._accidental._note = self
        self._quarter_duration = None
        self.quarter_duration = quarter_duration
        self._event = None
        self.event = event
        self._offset = None
        self._is_tied = False
        self.is_tied = is_tied

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
            self._quarter_duration = Fraction(value).limit_denominator(1000)
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

    @property
    def previous(self):
        index = self.up.notes.index(self)
        if index == 0:
            return None
        return self.up.notes[index - 1]

    def update_offset(self):
        if self.previous:
            output = self.previous.offset + self.previous.quarter_duration
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


    # @property
    # def is_tied(self):
    #     return self._is_tied
    #
    # @is_tied.setter
    # def is_tied(self, value):
    #     if not isinstance(value, bool):
    #         raise TypeError('is_tied.value must be of type bool not{}'.format(type(value)))
    #     self._is_tied = value
    #     if value is True:
    #         self.add_tie('start')

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

    def update_duration(self, divisions):
        try:
            self.duration.value = int(self.quarter_duration * divisions)
        except AttributeError:
            self.add_child(Duration())
            self.duration.value = int(self.quarter_duration * divisions)

    def update_type(self):
        """get type of a Note() depending on its quantized duration and return it [whole, half, quarter, eighth, 16th,
        32nd, 64th]"""
        _types = {(1, 12): '32nd',
                  (1, 11): '32nd',
                  (2, 11): '16th',
                  (3, 11): '16th',
                  (4, 11): 'eighth',
                  (6, 11): 'eighth',
                  (8, 11): 'quarter',
                  (1, 10): '32nd',
                  (3, 10): '16th',
                  (1, 9): '32nd',
                  (2, 9): '16th',
                  (4, 9): 'eighth',
                  (8, 9): 'quarter',
                  (1, 8): '32nd',
                  (3, 8): '16th',
                  (7, 8): 'eighth',
                  (1, 7): '16th',
                  (2, 7): 'eighth',
                  (3, 7): 'eighth',
                  (4, 7): 'quarter',
                  (6, 7): 'quarter',
                  (1, 6): '16th',
                  (1, 5): '16th',
                  (2, 5): 'eighth',
                  (3, 5): 'eighth',
                  (4, 5): 'quarter',
                  (1, 4): '16th',
                  (2, 4): 'eighth',
                  (3, 4): 'eighth',
                  (7, 4): 'quarter',
                  (1, 3): 'eighth',
                  (2, 3): 'quarter',
                  (3, 2): 'quarter',
                  (1, 2): 'eighth',
                  (1, 1): 'quarter',
                  (2, 1): 'half',
                  (3, 1): 'half',
                  (4, 1): 'whole',
                  (6, 1): 'whole',
                  (8, 1): 'breve'}

        value = _types[(self.quarter_duration.numerator, self.quarter_duration.denominator)]

        try:
            note_type = self.get_children_by_type(Type)[0]
            note_type.value = value
        except IndexError:
            self.add_child(Type(value))

    def update_dot(self):
        _dot = 0
        division = self.up.get_divisions()
        if self.quarter_duration.numerator % 3 == 0:
            _dot = 1
        elif self.quarter_duration == Fraction(1, 2) and (
                division == 3 or division == 6 or division == 12):
            _dot = 1
        elif self.quarter_duration == Fraction(1, 4) and (
                division == 3 or division == 6 or division == 12):
            _dot = 1
        elif (self.quarter_duration == Fraction(3, 9) or self.quarter_duration == Fraction(6,
                                                                                           9)) and division == 9:
            _dot = 1
        elif self.quarter_duration == Fraction(7, 8):
            _dot = 2
        elif self.quarter_duration == Fraction(7, 4):
            _dot = 2
        else:
            _dot = 0

        for dot in self.get_children_by_type(Dot):
            self.remove_child(dot)

        for i in range(_dot):
            self.add_child(Dot())
