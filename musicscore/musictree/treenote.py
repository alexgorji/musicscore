from quicktions import Fraction

from musicscore.musicxml.elements.fullnote import Rest, Event
from musicscore.musicxml.elements.note import Note, Dot, Duration, Type, Grace


class TreeNote(Note):
    """
    quarter_duration = 0 means grace note
    """

    def __init__(self, event=Rest(), quarter_duration=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quarter_duration = None
        self.quarter_duration = quarter_duration
        self._event = None
        self.event = event

    @property
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        if not isinstance(value, int) and not isinstance(value, float) and not isinstance(value, Fraction):
            raise TypeError('quarter_duration must be of type int, float or Fraction not {}'.format(type(value)))

        if value < 0:
            raise ValueError('quarter_duration {} must be zero or positive'.format(value))

        self._quarter_duration = value

        if value == 0:
            if not self.get_children_by_type(Grace):
                children = self.get_children()[:]
                self.reset_children()
                for child in children:
                    if not isinstance(child, Duration):
                        self.add_child(child)
                    else:
                        del child
                self.add_child(Grace())

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, value):
        if not isinstance(value, Event):
            raise TypeError('event.value must be of type  not{}'.format(type(value)))
        try:
            self.remove_child(self._event)
        except ValueError:
            pass
        self._event = self.add_child(value)

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
        if self.quarter_duration.numerator % 3 == 0:
            _dot = 1
        elif self.quarter_duration == Fraction(1, 2) and (
                self.up.divisions == 3 or self.up.divisions == 6 or self.up.divisions == 12):
            _dot = 1
        elif self.quarter_duration == Fraction(1, 4) and (
                self.up.divisions == 3 or self.up.divisions == 6 or self.up.divisions == 12):
            _dot = 1
        elif (self.quarter_duration == Fraction(3, 9) or self.quarter_duration == Fraction(6,
                                                                                           9)) and self.up.divisions == 9:
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
