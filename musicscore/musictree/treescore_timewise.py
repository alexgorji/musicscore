from lxml import etree as et

import musicscore.musicxml.elements.timewise as timewise
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescorepart import TreeScorePart
from musicscore.musicxml.elements.scoreheader import PartList, Credit, Defaults
from musicscore.musicxml.groups.layout import PageLayout, StaffLayout, SystemLayout
from musicscore.musicxml.groups.margins import LeftMargin, RightMargin, TopMargin, BottomMargin
from musicscore.musicxml.types.complextypes.credit import CreditType, CreditWords
from musicscore.musicxml.types.complextypes.defaults import Scaling
from musicscore.musicxml.types.complextypes.pagelayout import PageMargins, PageHeight, PageWidth
from musicscore.musicxml.types.complextypes.scaling import Tenths, Millimeters
from musicscore.musicxml.types.complextypes.scorepart import PartName
from musicscore.musicxml.types.complextypes.stafflayout import StaffDistance
from musicscore.musicxml.types.complextypes.systemlayout import SystemDistance
from musicscore.musicxml.elements.barline import Barline, BarStyle


class TreePageStyle(object):
    sizes = {'A4': (210, 297), 'A3': (297, 420)}

    def __init__(self, score, scale=1, size='A4', format='portrait', left_margin=20, right_margin=10, top_margin=15,
                 bottom_margin=15, system_distance=None, staff_distance=None):

        self._score = None
        self.score = score
        self.tenth = 40

        self._size = None
        self._format = 'portrait'

        self._defaults = None
        self._scaling = None

        self._page_layout = None
        self._page_height = None
        self._page_width = None
        self._page_margins = None

        self._left_margin = None
        self._right_margin = None
        self._top_margin = None
        self._bottom_margin = None

        self._system_layout = None
        self._system_margins = None
        self._system_distance = None
        self._staff_layout = None
        self._staff_distance = None

        self.scale = scale
        self.size = size
        self.format = format

        self.left_margin = left_margin
        self.right_margin = right_margin
        self.top_margin = top_margin
        self.bottom_margin = bottom_margin
        self.staff_distance = staff_distance
        self.system_distance = system_distance

    def millimeters_to_tenth(self, m):
        return round(m / self.millimeters * self.tenth)

    @property
    def millimeters(self):
        return self.scale * 7.2319

    def _add_defaults(self):
        self._defaults = self.score.add_child(Defaults())

    def _add_scaling(self):
        if not self._defaults:
            self._add_defaults()
        self._scaling = self._defaults.add_child(Scaling())
        self._scaling.add_child(Millimeters(self.millimeters))
        self._scaling.add_child(Tenths(self.tenth))

    def _add_page_layout(self):
        if not self._scaling:
            self._add_scaling()

        self._page_layout = self._defaults.add_child(PageLayout())

    def _add_staff_layout(self):
        if not self._scaling:
            self._add_scaling()

        self._staff_layout = self._defaults.add_child(StaffLayout())

    def _add_system_layout(self):
        if not self._scaling:
            self._add_scaling()

        self._system_layout = self._defaults.add_child(SystemLayout())

    def _add_page_margins(self):
        if not self._page_layout:
            self._add_page_layout()

        self._page_margins = self._page_layout.add_child(PageMargins(type_='both'))

    @property
    def score(self):
        '''
        system_layout = defaults.add_child(SystemLayout())
        system_margins = system_layout.add_child(SystemMargins())
        system_margins.add_child(LeftMargin(0))
        system_margins.add_child(RightMargin(0))
        system_layout.add_child(SystemDistance(121))
        system_layout.add_child(TopSystemDistance(300))
        '''
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, TreeScoreTimewise):
            raise TypeError('score.value must be of type TreeScoreTimewise not{}'.format(type(value)))
        self._score = value

    @property
    def page_height(self):
        return self._page_height

    @page_height.setter
    def page_height(self, value):
        value = self.millimeters_to_tenth(value)
        if self.page_height:
            self.page_height.value = value
        else:
            if not self._page_layout:
                self._add_page_layout()
            self._page_height = self._page_layout.add_child(PageHeight(value))

    @property
    def page_width(self):
        return self._page_width

    @page_width.setter
    def page_width(self, value):
        value = self.millimeters_to_tenth(value)
        if self.page_width:
            self.page_width.value = value
        else:
            if not self._page_layout:
                self._add_page_layout()
            self._page_width = self._page_layout.add_child(PageWidth(value))

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        if value == 'landscape':
            self.page_height, self.page_width = self.size[1], self.size[0]
        elif value == 'portrait':
            self.page_height, self.page_width = self.size[0], self.size[1]
        else:
            raise ValueError()

        self._format = value

    @property
    def left_margin(self):
        return self._left_margin

    @left_margin.setter
    def left_margin(self, value):
        value = self.millimeters_to_tenth(value)
        if self.left_margin:
            self.left_margin.value = value
        else:
            if not self._page_margins:
                self._add_page_margins()
            self._left_margin = self._page_margins.add_child(LeftMargin(value))

    @property
    def right_margin(self):
        return self._right_margin

    @right_margin.setter
    def right_margin(self, value):
        value = self.millimeters_to_tenth(value)
        if self.right_margin:
            self.right_margin.value = value
        else:
            if not self._page_margins:
                self._add_page_margins()
            self._right_margin = self._page_margins.add_child(RightMargin(value))

    @property
    def top_margin(self):
        return self._top_margin

    @top_margin.setter
    def top_margin(self, value):
        value = self.millimeters_to_tenth(value)
        if self.top_margin:
            self.top_margin.value = value
        else:
            if not self._page_margins:
                self._add_page_margins()
            self._top_margin = self._page_margins.add_child(TopMargin(value))

    @property
    def bottom_margin(self):
        return self._bottom_margin

    @bottom_margin.setter
    def bottom_margin(self, value):
        value = self.millimeters_to_tenth(value)
        if self.bottom_margin:
            self.bottom_margin.value = value
        else:
            if not self._page_margins:
                self._add_page_margins()
            self._bottom_margin = self._page_margins.add_child(BottomMargin(value))

    @property
    def staff_distance(self):
        return self._staff_distance

    @staff_distance.setter
    def staff_distance(self, value):
        if value:
            value = self.millimeters_to_tenth(value)
            if self.staff_distance:
                self.staff_distance.value = value
            else:
                if not self._staff_layout:
                    self._add_staff_layout()
                self._staff_distance = self._staff_layout.add_child(StaffDistance(value))

    @property
    def system_distance(self):
        return self._system_distance

    @system_distance.setter
    def system_distance(self, value):
        if value:
            value = self.millimeters_to_tenth(value)
            if self.system_distance:
                self.system_distance.value = value
            else:
                if not self._system_layout:
                    self._add_system_layout()
                self._system_distance = self._system_layout.add_child(SystemDistance(value))

    @property
    def size(self):
        (w, h) = self.sizes[self._size]
        # h = self.millimeters_to_tenth(h)
        # w = self.millimeters_to_tenth(w)
        return h, w

    @size.setter
    def size(self, value):
        self._size = value
        self.format = self._format
        # self.page_height = self.size[0]
        # self.page_width = self.size[1]

    @property
    def page_size(self):
        return self.size

    @page_size.setter
    def page_size(self, value):
        self.size = value


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
        self._page_style = TreePageStyle(score=self, **kwargs)
        self._accidental_mode = 'normal'

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

    def add_part(self, name='none', print_object='no'):
        new_score_part = self._generate_score_part()
        new_score_part.parent_score = self
        part_name = new_score_part.add_child(PartName(name=name))
        part_name.print_object = print_object
        self._part_list.add_child(new_score_part)
        for measure in self.get_children_by_type(TreeMeasure):
            part = new_score_part.add_part()
            measure.add_child(part)
            if measure.barline_style:
                bl = part.add_child(Barline())
                bl.add_child(BarStyle(measure.barline_style))

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
                    if remaining_duration < 1:
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
