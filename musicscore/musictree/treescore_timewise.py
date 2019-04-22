from lxml import etree as et

import musicscore.musicxml.elements.timewise as timewise
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musicxml.elements.scoreheader import PartList
from musicscore.musicxml.types.complextypes.partlist import ScorePart
from musicscore.musicxml.types.complextypes.scorepart import PartName


class TreeScoreTimewise(timewise.Score):
    """"""

    _auto_part_number = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._part_list = self.add_child(PartList())
        self.version = '3.0'
        self._finished = False

    def _generate_score_part(self):
        id_ = 'p' + str(self._auto_part_number)
        self._auto_part_number += 1
        return ScorePart(id=id_)

    def get_score_parts(self):
        return self._part_list.get_children()

    def add_part(self, name='none', print_object='no'):
        new_score_part = self._generate_score_part()
        part_name = new_score_part.add_child(PartName(name=name))
        part_name.print_object = print_object
        self._part_list.add_child(new_score_part)
        for measure in self.get_children_by_type(TreeMeasure):
            p = measure.add_child(TreePart(id=new_score_part.id))
            # p.set_beats()

    def add_measure(self, measure=None):
        new_measure = self._set_new_measure(measure)

        for score_part in self.get_score_parts():
            new_measure.add_child(TreePart(id=score_part.id))
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

    def finish(self):
        if not self._finished:
            self.update_measures()
            for measure in self.get_children_by_type(TreeMeasure):
                for part in measure.get_children_by_type(TreePart):
                    part.finish()
            self.close_dtd()
            self._finished = True

    def to_string(self):
        self.finish()
        xml = self._to_xml()
        return et.tounicode(xml, pretty_print=True)

