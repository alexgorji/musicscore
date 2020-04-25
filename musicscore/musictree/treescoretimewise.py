from lxml import etree as et

import musicscore.musicxml.elements.timewise as timewise
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treeinstruments import TreeInstrument
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepagestyle import TreePageStyle
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescorepart import TreeScorePart
from musicscore.musicxml.elements import partwise
from musicscore.musicxml.elements.barline import Barline, BarStyle
from musicscore.musicxml.elements.scoreheader import PartList, Credit, Defaults
from musicscore.musicxml.types.complextypes.appearance import LineWidth
from musicscore.musicxml.types.complextypes.credit import CreditType, CreditWords
from musicscore.musicxml.types.complextypes.defaults import Appearance, WordFont
from musicscore.musicxml.types.complextypes.encoding import Supports
from musicscore.musicxml.types.complextypes.identification import Encoding
from musicscore.musicxml.types.complextypes.scorepart import Identification


class TreeScoreTimewise(timewise.Score):
    """"""

    _auto_part_number = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._part_list = self.add_child(PartList())
        self.version = '3.0'
        self._tuplet_line_width = None
        self._finished = False
        self._pre_quantized = False
        self._quantized = False
        self._post_quantized = False
        self._max_division = None
        self._forbidden_divisions = None
        self._page_style = TreePageStyle(score=self, **kwargs)
        self._accidental_mode = 'normal'
        self._title = None
        self._subtitle = None
        self._composer = None

        self._identifications_added = False

    # private methods

    def _add_identifications(self):
        identification = self.add_child(Identification())
        encoding = identification.add_child(Encoding())
        encoding.add_child(Supports(attribute='new-page', element='print', type_='yes', value_='yes'))
        encoding.add_child(Supports(attribute='new-system', element='print', type_='yes', value_='yes'))
        self._identifications_added = True

    def _generate_score_part(self):
        id_ = 'p' + str(self._auto_part_number)
        self._auto_part_number += 1
        return TreeScorePart(id=id_)

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

    # public properties
    @property
    def accidental_mode(self):
        return self._accidental_mode

    @accidental_mode.setter
    def accidental_mode(self, value):
        self._accidental_mode = value

    @property
    def composer(self):
        return self._composer

    @property
    def defaults(self):
        try:
            return self.get_children_by_type(Defaults)[0]
        except IndexError:
            return None

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

    def make_defaults(self):
        if self.defaults is None:
            self.add_child(Defaults())
        else:
            raise Exception('defaults already exists')

    @property
    def max_division(self):
        return self._max_division

    @max_division.setter
    def max_division(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('max_division.value must be None or of type int not {}'.format(type(value)))

        self._max_division = value

    @property
    def number_of_parts(self):
        return len(self._part_list.get_children_by_type(TreeScorePart))

    @property
    def page_style(self):
        return self._page_style

    @property
    def subtitle(self):
        return self._subtitle

    @property
    def title(self):
        return self._title

    @property
    def tuplet_line_width(self):
        return self._tuplet_line_width

    @tuplet_line_width.setter
    def tuplet_line_width(self, val):

        if not isinstance(val, float):
            raise TypeError('tuplet_line_width.value must be of type float not{}'.format(type(val)))
        self._tuplet_line_width = val

        if self.defaults is None:
            self.make_defaults()

        try:
            appearance = self.defaults.get_children_by_type(Appearance)[0]
        except IndexError:
            appearance = self.defaults.add_child(Appearance())

        try:
            line_width = [lw for lw in appearance.get_children_by_type(LineWidth) if lw.type == 'tuplet bracket'][0]
        except IndexError:
            line_width = appearance.add_child(LineWidth(type='tuplet bracket'))

        line_width.value = val

    @property
    def word_font(self):
        try:
            return self.defaults.get_children_by_type(WordFont)[0]
        except (AttributeError, IndexError):
            return None

    # public methods
    # add
    def add_beats(self, list_of_beats=None):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.add_beats(list_of_beats)

    def add_chord(self, measure_number, part_number, chord):
        if not isinstance(chord, TreeChord):
            raise TypeError('add_note note must be of type TreeChord not {}'.format(type(chord)))

        measure = self.get_children_by_type(TreeMeasure)[measure_number - 1]
        part = measure.get_children_by_type(TreePart)[part_number - 1]
        part.add_chord(chord)
        return chord

    def add_composer(self, text, page=None, font_size=None, default_x=None, default_y=None, justify=None, valign=None,
                     **kwargs):
        if not page:
            page = 1
        if not font_size:
            font_size = 12
        if not default_x:
            default_x = int(self.page_style.page_width.value - 50)
        if not default_y:
            default_y = self.page_style.page_height.value - 143
        if not justify:
            justify = 'right'
        if not valign:
            valign = 'top'

        c = self.add_child(Credit(page=page))
        c.add_child(CreditType('composer'))

        self._composer = c.add_child(
            CreditWords(text, default_x=default_x, default_y=default_y, font_size=font_size, justify=justify,
                        valign=valign, **kwargs))

    def add_measure(self, measure=None):
        new_measure = self._set_new_measure(measure)

        for score_part in self.get_score_parts():
            p = score_part.add_part()
            new_measure.add_child(p)
        return self.add_child(new_measure)

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

    def add_text(self, text, page=None, font_size=None, default_x=None, default_y=None, justify=None, valign=None,
                 **kwargs):

        if not page:
            page = 1
        if not font_size:
            font_size = 12
        if not default_x:
            default_x = 50
        if not default_y:
            default_y = self.page_style.page_height.value - 143
        if not justify:
            justify = 'left'
        if not valign:
            valign = 'top'

        c = self.add_child(Credit(page=page))
        self._title = c.add_child(
            CreditWords(text, default_x=default_x, default_y=default_y, font_size=font_size, justify=justify,
                        valign=valign, **kwargs))

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
        self._title = c.add_child(
            CreditWords(text, default_x=default_x, default_y=default_y, font_size=font_size, justify=justify,
                        valign=valign, **kwargs))

    def add_score_part(self, score_part):
        score_part.parent_score = self
        return self._part_list.add_child(score_part)

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
        self._subtitle = c.add_child(
            CreditWords(text, default_x=default_x, default_y=default_y, font_size=font_size, justify=justify,
                        valign=valign, **kwargs))

    def add_instrument(self, instrument):
        if not isinstance(instrument, TreeInstrument):
            raise TypeError()
        self.add_part(instrument=instrument)

    def add_word_font(self, **kwargs):
        if self.defaults is None:
            self.make_defaults()

        self.defaults

    # get
    def get_beats(self):
        output = []
        for measure in self.get_children_by_type(TreeMeasure):
            output.extend(measure.get_beats())
        return output

    def get_measure(self, number):
        if number == 0:
            raise ValueError('number can be positiv or negative integer but not 0')
        if number < 0:
            number += 1
        return self.get_children_by_type(TreeMeasure)[number - 1]

    def get_score_part(self, id):
        for score_part in self.get_score_parts():
            if score_part.id == id:
                return score_part
        return None

    def get_score_parts(self):
        return self._part_list.get_children_by_type(TreeScorePart)

    # remove
    def remove_subtitle(self):
        subtitle_credit = [c for c in self.get_children_by_type(Credit) if
                           c.get_children_by_type(CreditType)[0].value == 'subtitle']
        try:
            self.remove_child(subtitle_credit[0])
        except IndexError:
            pass

    def remove_title(self):
        title_credit = [c for c in self.get_children_by_type(Credit) if
                        c.get_children_by_type(CreditType)[0].value == 'title']
        try:
            self.remove_child(title_credit[0])
        except IndexError:
            pass

    # set

    def set_time_signatures(self, quarter_durations=None, times=None, barline_style=None):
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
                self.get_children_by_type(TreeMeasure)[-1].set_barline_style(barline_style)
            return current_measure_number

        if quarter_durations:
            if not hasattr(quarter_durations, '__iter__'):
                quarter_durations = [quarter_durations]
            elif isinstance(quarter_durations, str):
                raise TypeError()
            else:
                quarter_durations = quarter_durations

            current_measure_number = 1
            for duration in quarter_durations:
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

    # update
    def update_accidentals(self, mode='normal'):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.update_accidentals(mode=mode)

    def update_divisions(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.update_divisions()

    def update_dots(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.update_dots()

    def update_durations(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.update_durations()

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

    def update_tuplets(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.update_tuplets()

    def update_types(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.update_types()

    # other
    def adjoin_rests(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.adjoin_rests()

    def adjoin_ties(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.adjoin_ties()

    def chord_to_notes(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.chords_to_notes()

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

        # if not self._identifications_added:
        #     self._add_identifications()

    def fill_with_rest(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.fill_with_rest()

    def finish(self):
        if not self._finished:
            self.update_measures()
            self.fill_with_rest()
            self.preliminary_adjoin_rests()
            self.add_beats()
            self.quantize()
            # self.adjoin_rests_in_beat()
            self.split_not_notatable()
            self.implement_flags_1()
            self.adjoin_ties()
            self.adjoin_rests()
            self.update_tuplets()
            self.substitute_sextoles()
            self.implement_flags_2()
            self.update_types()
            self.update_dots()
            self.group_beams()
            self.implement_flags_3()
            self.chord_to_notes()
            self.update_divisions()
            self.update_accidentals(mode=self.accidental_mode)
            self.update_durations()
            self.close_dtd()
            self._finished = True

    def group_beams(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.group_beams()

    def implement_flags_1(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.implement_flags_1()

    def implement_flags_2(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.implement_flags_2()

    def implement_flags_3(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.implement_flags_3()

    def make_word_font(self, **kwargs):
        if self.defaults is None:
            self.make_defaults()
        if self.word_font is None:
            self.defaults.add_child(WordFont(**kwargs))
        else:
            raise Exception('word-font already exists')

    def preliminary_adjoin_rests(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.preliminary_adjoin_rests()

    def quantize(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.quantize()

    def recalculate_x(self):
        for credit in self.get_children_by_type(Credit):
            for credit_words in credit.get_children_by_type(CreditWords):
                x_factor = self.page_style.page_width.value / self.page_style.previous_page_width_value
                credit_words.default_x *= x_factor

    def recalculate_y(self):
        for credit in self.get_children_by_type(Credit):
            for credit_words in credit.get_children_by_type(CreditWords):
                y_factor = self.page_style.page_height.value / self.page_style.previous_page_height_value
                credit_words.default_y *= y_factor

    def split_not_notatable(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.split_not_notatable()

    def substitute_sextoles(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                part.substitute_sextoles()

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
