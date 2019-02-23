from musicscore.musicxml.elements.xml_timewise import XMLMeasureTimewise, XMLPartTimewise, XMLScoreTimewise
from musicscore.musicxml.elements.xml_score_header import XMLScorePart, XMLPartList, XMLPartName
from musicscore.musicxml.elements.xml_note import XMLNote
from musicscore.musicxml.types.simple_type import PositiveDecimal
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
        PositiveDecimal(value)
        self._quarter_duration = value


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
        duration_denominators = [Fraction(note.quarter_duration).limit_denominator(20).denominator for note in
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
