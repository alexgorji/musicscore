from musicscore.musicxml.elements.xml_timewise import XMLMeasureTimewise, XMLPartTimewise, XMLScoreTimewise
from musicscore.musicxml.elements.xml_score_header import XMLScorePart, XMLPartList


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
        return self.get_children_by_type(type_=XMLMeasureTimewise)

    def add_part(self, name='none', print_object='no'):
        new_score_part = self._generate_score_part()
        new_score_part.get_children()[0].name = name
        new_score_part.get_children()[0].print_object = print_object
        self._part_list.add_child(new_score_part)
        for measure in self.get_measures():
            measure.add_child(XMLPartTimewise(id=new_score_part.id))


    def add_measure(self):
        new_measure = XMLMeasureTimewise(number=0)
        self.add_child(new_measure)
        new_measure.number = self.get_children().index(new_measure)
        return new_measure
