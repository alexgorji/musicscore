from lxml import etree as et

import musicscore.musicxml.elements.timewise as timewise
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepagestyle import TreePageStyle
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescorepart import TreeScorePart
from musicscore.musicxml.elements import partwise
from musicscore.musicxml.elements.note import Stem
from musicscore.musicxml.elements.scoreheader import PartList, Credit
from musicscore.musicxml.types.complextypes.credit import CreditType, CreditWords
from musicscore.musicxml.types.complextypes.encoding import Supports
from musicscore.musicxml.types.complextypes.identification import Encoding
from musicscore.musicxml.types.complextypes.scorepart import PartName, Identification, PartAbbreviation
from musicscore.musicxml.elements.barline import Barline, BarStyle


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
        self._page_style = TreePageStyle(score=self, **kwargs)
        self._accidental_mode = 'normal'

        self._identifications_added = False

    @property
    def max_division(self):
        return self._max_division

    @max_division.setter
    def max_division(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('max_division.value must be None or of type int not {}'.format(type(value)))

        self._max_division = value

    @property
    def accidental_mode(self):
        return self._accidental_mode

    @accidental_mode.setter
    def accidental_mode(self, value):
        self._accidental_mode = value

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

    @property
    def page_style(self):
        return self._page_style

    def _generate_score_part(self):
        id_ = 'p' + str(self._auto_part_number)
        self._auto_part_number += 1
        return TreeScorePart(id=id_)

    def get_score_parts(self):
        return self._part_list.get_children()

    def get_score_part(self, id):
        for score_part in self.get_score_parts():
            if score_part.id == id:
                return score_part
        return None

    def add_score_part(self, score_part):
        score_part.parent_score = self
        instrument = score_part.instrument
        if instrument is not None:
            part_name = score_part.add_child(PartName(name=instrument.name))
            part_name.print_object = 'yes'
            score_part.add_child(PartAbbreviation(value=instrument.abbreviation))
        else:
            part_name = score_part.add_child(PartName(name='none'))
            part_name.print_object = 'no'

        return self._part_list.add_child(score_part)

    @property
    def number_of_parts(self):
        return len(self._part_list.get_children_by_type(TreeScorePart))

    def add_part(self, instrument=None):
        new_score_part = self._generate_score_part()
        new_score_part.instrument = instrument
        self.add_score_part(new_score_part)

        for measure in self.get_children_by_type(TreeMeasure):
            part = new_score_part.add_part()
            measure.add_child(part)
            if measure.barline_style:
                bl = part.add_child(Barline())
                bl.add_child(BarStyle(measure.barline_style))

    #
    # def insert_part(self, number, name='none', print_object='no'):
    #     def rearange_parts():
    #         print()

    def add_measure(self, measure=None):
        new_measure = self._set_new_measure(measure)

        for score_part in self.get_score_parts():
            p = score_part.add_part()
            new_measure.add_child(p)
        return self.add_child(new_measure)

    # def add_ruler(self, unit=1):
    #     if not self._finished:
    #         raise Exception('ruler can only be added to finished scores')
    #
    #     ruler_part = self.insert_part('ruler', part_number=1)
    #     remaining_time = self.duration
    #     while remaining_time > 0.01:
    #         ruler_chord = ruler_part.add_chord(TreeChord(quarter_duration=unit, midis=[76]))
    #         ruler_chord.head = 'none'
    #         ruler_chord.stem = Stem(default_y=11, direction='down')
    #         remaining_time -= ruler_chord.duration
    #
    #     # measure_1.staff_style = StaffStyle(number_of_lines=1)
    #     # measure_1.time_signature.hide = True
    #     # print measure_1.staff_style.number_of_lines
    #     # part_node.children[0].content.staff_style = StaffStyle(number_of_lines = 1, staff_distance = 70)
    #     # for measure_node in part_node.children:
    #     #     measure_node.content.staff_style = StaffStyle(staff_distance=70)
    #
    #     # measure_1.notes[0].clef = Clef(sign='none')

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

    def _add_identifications(self):
        identification = self.add_child(Identification())
        encoding = identification.add_child(Encoding())
        encoding.add_child(Supports(attribute='new-page', element='print', type_='yes', value_='yes'))
        encoding.add_child(Supports(attribute='new-system', element='print', type_='yes', value_='yes'))
        # encoding.add_child(Supports(element='accidental', type_='yes'))
        # encoding.add_child(Supports(element='beam', type_='yes'))
        # encoding.add_child(Supports(element='stem', type_='yes'))
        self._identifications_added = True

    # def set_time_signatures(self, duration=None, times=None):
    #     if self.get_children_by_type(TreeMeasure):
    #         raise Exception('for setting time signatures score should be empty')
    #
    #     def make_measure(duration=None):
    #         def get_time():
    #             if duration % 1 == 0:
    #                 time = (int(duration), 4)
    #                 return time
    #             elif (duration * 2) % 1 == 0:
    #                 time = (int(duration * 2), 8)
    #                 return time
    #             else:
    #                 raise ValueError('duration {} is not dividable'.format(duration))
    #
    #         if not duration:
    #             time = (4, 4)
    #         else:
    #             time = get_time()
    #
    #         return TreeMeasure(time)
    #
    #     if not times:
    #         times = {}
    #
    #     if duration:
    #         duration = float(duration)
    #         current_measure_number = 1
    #         remaining_duration = duration
    #
    #         while True:
    #             if current_measure_number in times.keys():
    #                 measure = TreeMeasure(time=times[current_measure_number])
    #             else:
    #                 measure = TreeMeasure(time=(4, 4))
    #             measure_duration = measure.quarter_duration
    #             if measure_duration > remaining_duration:
    #                 measure = make_measure(duration=remaining_duration)
    #                 self.add_measure(measure)
    #                 break
    #             else:
    #                 self.add_measure(measure)
    #                 remaining_duration -= measure.quarter_duration
    #                 if remaining_duration < 1:
    #                     break
    #                 current_measure_number += 1
    #     else:
    #         try:
    #             number_of_measures = list(times.keys())[-1]
    #             current_time = (4, 4)
    #             for measure_number in range(1, number_of_measures + 1):
    #                 try:
    #                     current_time = times[measure_number]
    #                 except KeyError:
    #                     pass
    #                 self.add_measure(TreeMeasure(time=current_time))
    #         except IndexError:
    #             pass

    def set_time_signatures(self, durations=None, times=None, barline_style=None):
        global current_time
        if self.get_children_by_type(TreeMeasure):
            raise Exception('for setting time signatures score should be empty')

        def make_measure(duration=None):
            def get_time():
                if duration % 1 == 0:
                    time = (int(duration), 4)
                    return time
                elif (duration * 2) % 1 == 0:
                    time = (int(duration * 2), 8)
                    return time
                else:
                    raise ValueError('duration {} is not dividable'.format(duration))

            if not duration:
                time = (4, 4)
            else:
                time = get_time()

            return TreeMeasure(time)

        if not times:
            times = {}

        current_time = (4, 4)

        def set_times(current_measure_number, duration):
            global current_time
            duration = float(duration)
            remaining_duration = duration

            while True:
                if current_measure_number in times.keys():
                    current_time = times[current_measure_number]

                measure = TreeMeasure(time=current_time)

                measure_duration = measure.quarter_duration
                if measure_duration > remaining_duration:
                    measure = make_measure(duration=remaining_duration)
                    self.add_measure(measure)
                    break
                else:
                    self.add_measure(measure)
                    current_measure_number += 1
                    remaining_duration -= measure.quarter_duration
                    if remaining_duration == 0:
                        break
            if barline_style:
                self.get_children_by_type(TreeMeasure)[-1].barline_style = barline_style
            return current_measure_number

        if durations:
            if not hasattr(durations, '__iter__'):
                durations = [durations]
            elif isinstance(durations, str):
                raise TypeError()
            else:
                durations = durations

            current_measure_number = 1
            for duration in durations:
                current_measure_number = set_times(current_measure_number, duration)

            if list(times.keys()) != [] and current_measure_number < list(times.keys())[-1]:
                current_time = (4, 4)
                for key in times.keys():
                    if key <= current_measure_number:
                        current_time = times[key]

                for measure_number in range(current_measure_number, list(times.keys())[-1] + 1):
                    try:
                        current_time = times[measure_number]
                    except KeyError:
                        pass
                    self.add_measure(TreeMeasure(time=current_time))

        else:
            try:
                number_of_measures = list(times.keys())[-1]
                current_time = (4, 4)
                for measure_number in range(1, number_of_measures + 1):
                    try:
                        current_time = times[measure_number]
                    except KeyError:
                        pass
                    self.add_measure(TreeMeasure(time=current_time))
            except IndexError:
                pass

    def get_measure(self, number):
        if number == 0:
            raise ValueError('number can be positiv or negative integer but not 0')
        if number < 0:
            number += 1
        return self.get_children_by_type(TreeMeasure)[number - 1]

    def add_chord(self, measure_number, part_number, chord):
        if not isinstance(chord, TreeChord):
            raise TypeError('add_note note must be of type TreeChord not {}'.format(type(chord)))

        measure = self.get_children_by_type(TreeMeasure)[measure_number - 1]
        part = measure.get_children_by_type(TreePart)[part_number - 1]
        part.add_chord(chord)
        return chord

    def add_title(self, text, page=None, font_size=None, default_x=None, default_y=None, justify=None, valign=None,
                  **kwargs):
        if not page:
            page = 1
        if not font_size:
            font_size = 24
        if not default_x:
            default_x = int(self.page_style.page_width.value / 2)
        if not default_y:
            default_y = self.page_style.page_height.value - 43
        if not justify:
            justify = 'center'
        if not valign:
            valign = 'top'

        c = self.add_child(Credit(page=page))
        c.add_child(CreditType('title'))
        c.add_child(CreditWords(text, default_x=default_x, default_y=default_y, font_size=font_size, justify=justify,
                                valign=valign, **kwargs))

    def add_subtitle(self, text, page=None, font_size=None, default_x=None, default_y=None, justify=None, valign=None,
                     **kwargs):
        if not page:
            page = 1
        if not font_size:
            font_size = 18
        if not default_x:
            default_x = int(self.page_style.page_width.value / 2)
        if not default_y:
            default_y = self.page_style.page_height.value - 93
        if not justify:
            justify = 'center'
        if not valign:
            valign = 'top'

        c = self.add_child(Credit(page=page))
        c.add_child(CreditType('subtitle'))
        c.add_child(CreditWords(text, default_x=default_x, default_y=default_y, font_size=font_size, justify=justify,
                                valign=valign, **kwargs))

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

    def adjoin_ties(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.adjoin_ties()

    def adjoin_rests(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.adjoin_rests()

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
            self.adjoin_ties()
            self.adjoin_rests()
            self.update_tuplets()
            self.substitute_sextoles()
            self.update_types()
            self.update_dots()
            self.group_beams()
            self.chord_to_notes()
            self.update_divisions()
            self.update_accidentals(mode=self.accidental_mode)
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

    def to_partwise(self):
        if not self._finished:
            raise Exception('timewise score must be finished before converting.')

        output = partwise.Score()
        output.version = self.version
        partwise_parts = []

        def get_ids():
            return [partwise_part.id for partwise_part in partwise_parts]

        for child in self.get_children():

            if isinstance(child, timewise.Measure):
                timewise_measure = child

                for timewise_part in timewise_measure.get_children_by_type(timewise.Part):
                    if timewise_part.id not in get_ids():
                        new_part = partwise.Part(id=timewise_part.id)
                        partwise_parts.append(new_part)
                    partwise_part = [p for p in partwise_parts if p.id == timewise_part.id][0]
                    new_measure = partwise.Measure()
                    for attribute in new_measure._ATTRIBUTES:
                        try:
                            new_measure.set_attribute(str(attribute), timewise_measure.get_attribute(str(attribute)))
                        except KeyError:
                            pass
                    for musicdata in timewise_part.get_children():
                        new_measure.add_child(musicdata)

                    partwise_part.add_child(new_measure)

            else:
                output.add_child(child)
        for partwise_part in partwise_parts:
            output.add_child(partwise_part)

        output.close_dtd()
        return output

    def extend(self, score):
        if not score.get_score_parts():
            raise ValueError('score {} cannot be empty'.format(score))

        if not self.get_score_parts():
            for score_part in score.get_score_parts():
                new_score_part = TreeScorePart(id=score_part.id)
                self.add_score_part(new_score_part)
                for part in new_score_part._parts:
                    new_score_part.add_part(part)

        else:
            my_ids = [score_part.id for score_part in self.get_score_parts()]
            other_ids = [score_part.id for score_part in score.get_score_parts()]
            difference = set.symmetric_difference(set(my_ids), set(other_ids))
            if difference:
                raise ValueError('two scores must have score_parts with same ids. Difference is {}'.format(difference))

        for measure in score.get_children_by_type(TreeMeasure):
            self.add_child(measure)
            for part in measure.get_children_by_type(TreePart):
                score_part = self.get_score_part(part.id)
                score_part.add_part(part)

        if not self._identifications_added:
            self._add_identifications()
