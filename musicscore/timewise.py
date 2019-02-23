from musicscore.musicxml.elements.xml_timewise import XMLMeasureTimewise, XMLPartTimewise, XMLScoreTimewise
from musicscore.musicxml.elements.xml_score_header import XMLScorePart, XMLPartList, XMLPartName
from musicscore.musicxml.elements.xml_note import XMLNote, XMLType, XMLDot
from musicscore.musicxml.elements.xml_attributes import XMLAttributes, XMLDivisions
from quicktions import Fraction
from musicscore.basic_functions import lcm


class Note(XMLNote):
    """"""

    def __init__(self, event, quarter_duration, *args, **kwargs):
        super().__init__(event, duration=None, *args, **kwargs)
        self.quarter_duration = quarter_duration

    @property
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        if value <= 0:
            raise ValueError('quarter_duration must be a positive number or fraction not {}'.format(value))
        self._quarter_duration = Fraction(value).limit_denominator(12)

    def update_type(self):
        """get type of a Note() depending on its quantized duration and return it [whole, half, quarter, eighth, 16th, 32nd, 64th]"""
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

        try:
            note_type = self.get_children_by_type(XMLType)[0]
        except IndexError:
            note_type = self.add_child(XMLType('quarter'))

        note_type.value = _types[(self.quarter_duration.numerator, self.quarter_duration.denominator)]

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

        for dot in self.get_children_by_type(XMLDot):
            self.remove_child(dot)

        for i in range(_dot):
            self.add_child(XMLDot())


class Measure(XMLMeasureTimewise):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_part(self, part_number=1):
        return self.get_children_by_type(Part)[part_number - 1]


class Part(XMLPartTimewise):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attributes = self.add_child(XMLAttributes())
        attributes.add_child(XMLDivisions(4))

    def get_notes(self):
        return self.get_children_by_type(Note)

    def get_divisions(self):
        duration_denominators = [note.quarter_duration.denominator for note in
                                 self.get_notes()]

        if len(duration_denominators) == 0:
            return 1
        elif len(duration_denominators) == 1:
            return duration_denominators[0]
        else:
            return lcm(duration_denominators)

    def update_divisions(self):
        # todo: it must be possible to set attributes like this:
        # self.attributes.divisions = 3
        attributes = self.get_children_by_type(XMLAttributes)[0]
        divisions = attributes.get_children_by_type(XMLDivisions)[0]
        divisions.value = self.get_divisions()


class Timwise(XMLScoreTimewise):
    """"""

    _auto_part_number = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._part_list = self.add_child(XMLPartList())

    def _generate_score_part(self):
        id = 'p' + str(self._auto_part_number)
        self._auto_part_number += 1
        return XMLScorePart(id=id)

    def get_measures(self):
        return self.get_children_by_type(type_=Measure)

    def get_parts(self):
        return self._part_list.get_children()

    def add_part(self, name='none', print_object='no'):
        new_score_part = self._generate_score_part()
        new_score_part.get_children_by_type(XMLPartName)[0].name = name
        new_score_part.get_children_by_type(XMLPartName)[0].print_object = print_object
        self._part_list.add_child(new_score_part)
        for measure in self.get_measures():
            measure.add_child(Part(id=new_score_part.id))

    def add_measure(self):
        new_measure = Measure(number=0)
        self.add_child(new_measure)
        new_measure.number = len(self.get_children()) - 1
        for part in self.get_parts():
            new_measure.add_child(XMLPartTimewise(id=part.id))
        return new_measure

    def add_note(self, measure_number, part_number, note):
        if not isinstance(note, Note):
            raise TypeError('add_note note must be of type Note not {}'.format(type(note)))
        measure = self.get_measures()[measure_number - 1]
        part = measure.get_part(part_number)
        part.add_child(note)
        duration = part.get_divisions() * note.quarter_duration
        note.duration = int(duration)
        part.update_divisions()
        note.update_type()
        note.update_dot()
