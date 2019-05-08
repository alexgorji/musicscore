from lxml import etree as et

import musicscore.musicxml.elements.timewise as timewise
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescorepart import TreeScorePart
from musicscore.musicxml.elements.scoreheader import PartList
from musicscore.musicxml.types.complextypes.scorepart import PartName


class TreeInstrumentPart(object):
    """"""

    def __init__(self, parent_score, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent_score = parent_score
        self._number = number
        self._voices = None

    @property
    def parent_score(self):
        return self._parent_score

    @property
    def number(self):
        return self._number


class TreeScoreTimewise(timewise.Score):
    """"""

    _auto_part_number = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._part_list = self.add_child(PartList())
        self.version = '3.0'
        self._finished = False
        self._pre_quantized = False
        self._quantized = False
        self._post_quantized = False
        self._max_division = None
        self._forbidden_divisions = None

    @property
    def max_division(self):
        return self._max_division

    @max_division.setter
    def max_division(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('max_division.value must be None or of type int not {}'.format(type(value)))

        self._max_division = value

    @property
    def forbidden_divisions(self):

        return self._forbidden_divisions

    @forbidden_divisions.setter
    def forbidden_divisions(self, value):
        if value is not None:
            for x in value:
                if not isinstance(x, int):
                    raise TypeError('forbidden_division must be of type int not{}'.format(type(value)))

        self._forbidden_divisions = value

    def _generate_score_part(self):
        id_ = 'p' + str(self._auto_part_number)
        self._auto_part_number += 1
        return TreeScorePart(id=id_)

    def get_score_parts(self):
        return self._part_list.get_children()

    def add_part(self, name='none', print_object='no'):
        new_score_part = self._generate_score_part()
        new_score_part.parent_score = self
        part_name = new_score_part.add_child(PartName(name=name))
        part_name.print_object = print_object
        self._part_list.add_child(new_score_part)
        for measure in self.get_children_by_type(TreeMeasure):
            p = new_score_part.add_part()
            measure.add_child(p)

    def add_measure(self, measure=None):
        new_measure = self._set_new_measure(measure)

        for score_part in self.get_score_parts():
            p = score_part.add_part()
            new_measure.add_child(p)
        return self.add_child(new_measure)

    def _set_new_measure(self, measure):
        if measure is None:
            new_measure = TreeMeasure()
            measures = self.get_children_by_type(TreeMeasure)
            if measures:
                new_measure.time = measures[-1].time.__copy__()
            else:
                new_measure.time.show = True
        else:
            new_measure = measure
        return new_measure

    def get_measure(self, number):
        return self.get_children_by_type(TreeMeasure)[number - 1]

    def add_chord(self, measure_number, part_number, chord):
        if not isinstance(chord, TreeChord):
            raise TypeError('add_note note must be of type TreeChord not {}'.format(type(chord)))

        measure = self.get_children_by_type(TreeMeasure)[measure_number - 1]
        part = measure.get_children_by_type(TreePart)[part_number - 1]
        part.add_chord(chord)
        return chord

    def add_title(self, text):
        pass


    def update_measures(self):
        measures = self.get_children_by_type(TreeMeasure)
        for index, measure in enumerate(measures):
            measure.number = str(index + 1)
            if measure.time.force_hide:
                measure.hide_time_signature()
            elif measure.time.force_show:
                measure.show_time_signature()
            elif index == 0:
                measure.show_time_signature()
            elif measure.time.values == measures[index - 1].time.values:
                measure.hide_time_signature()
            else:
                measure.show_time_signature()

    def fill_with_rest(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.fill_with_rest()

    def add_beats(self, list_of_beats=None):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.add_beats(list_of_beats)

    def get_beats(self):
        output = []
        for measure in self.get_children_by_type(TreeMeasure):
            output.extend(measure.get_beats())
        return output

    def quantize(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.quantize()

    def split_not_notatable(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.split_not_notatable()

    def update_tuplets(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.update_tuplets()

    def substitute_sextoles(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.substitute_sextoles()

    def update_types(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.update_types()

    def update_dots(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.update_dots()

    def group_beams(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.group_beams()

    def chord_to_notes(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.chord_to_notes()

    def update_divisions(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.update_divisions()

    def update_accidentals(self, mode='normal'):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.update_accidentals(mode=mode)

    def update_durations(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.update_durations()

    def finish(self):
        if not self._finished:
            self.update_measures()
            self.fill_with_rest()
            self.add_beats()
            self.quantize()
            self.split_not_notatable()
            self.update_tuplets()
            self.substitute_sextoles()
            self.update_types()
            self.update_dots()
            self.group_beams()
            self.chord_to_notes()
            self.update_divisions()
            self.update_accidentals(mode='normal')
            self.update_durations()
            self.close_dtd()
            # for measure in self.get_children_by_type(TreeMeasure):
            #     for part in measure.get_children_by_type(TreePart):
            #         part.finish()
            # self.close_dtd()
            self._finished = True

    def to_string(self):
        self.finish()
        xml = self._to_xml()
        return et.tounicode(xml, pretty_print=True)
