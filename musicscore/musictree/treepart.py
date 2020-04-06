import warnings

from lxml import etree as et
from quicktions import Fraction

from musicscore.basic_functions import lcm, substitute, flatten
from musicscore.musictree.exceptions import MusicTreeError
from musicscore.musictree.treebeat import TreeBeat
from musicscore.musictree.treechord import TreeChord, TreeBackup, TreeNote
from musicscore.musictree.treechordflags2 import TreeChordFlag2
from musicscore.musictree.treechordflags3 import TreeChordFlag3
from musicscore.musictree.treeclef import TreeClef
from musicscore.musicxml.elements import timewise as timewise
from musicscore.musicxml.elements.fullnote import Pitch, Rest
from musicscore.musicxml.elements.note import Beam, Type, Tie, Notations
from musicscore.musicxml.groups.common import Voice
from musicscore.musicxml.groups.musicdata import Direction, Attributes
from musicscore.musicxml.types.complextypes.attributes import Divisions, Staves
from musicscore.musicxml.types.complextypes.direction import DirectionType, Sound
from musicscore.musicxml.types.complextypes.directiontype import Metronome
from musicscore.musicxml.types.complextypes.metronome import BeatUnit, PerMinute
from musicscore.musicxml.types.complextypes.notations import Slur


class TreePartVoice(object):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._number = None
        self.number = number
        self._max_division = None
        self._forbidden_divisions = None
        self._chords = []
        self._beats = None
        self._filled_with_rest = False
        self._preliminary_rests_adjoined = False
        self._beats_added = False
        self._quantized = False

        self._not_notatable_split = False
        self._parent_tree_staff = None
        self._ties_adjoined = False
        self._rests_adjoined = False
        self._tuplets_updated = False
        self._sextoles_substituted = False
        self._types_updated = False
        self._dots_updated = False
        self._flags_1_implemented = False
        self._flags_2_implemented = False
        self._flags_3_implemented = False
        self._flags_4_implemented = False
        self._xml_chords = None

    # // private methods
    def _add_chords_to_beats(self):
        if len(self.beats) == 1:
            current_beat = self.beats[0]
            for chord in self.chords:
                current_beat.add_chord(chord)
        else:
            beats = iter(self.beats)
            current_beat = beats.__next__()
            next_beat = beats.__next__()

            for chord in self.chords:
                while True and (chord.offset < current_beat.offset or chord.offset >= next_beat.offset):
                    try:
                        current_beat = next_beat
                        next_beat = beats.__next__()
                    except StopIteration:
                        break

                current_beat.add_chord(chord)

    def _correct_deviations(self):

        def _get_expected_durations():
            output = [self.beats[0].duration]
            for beat in self.beats[1:]:
                if beat.chords == []:
                    output[-1] += beat.duration
                else:
                    output.append(beat.duration)
            return output

        expected_durations = _get_expected_durations()
        for index, beat in enumerate([beat for beat in self.beats if beat.chords]):
            delta = expected_durations[index] - sum([chord.quarter_duration for chord in beat.chords])
            beat.chords[-1].quarter_duration += delta

    def _group_beats(self, grouping_list):
        # todo test grouping list
        if False:
            raise Exception()
        else:
            chords = [chord for chord in self.chords if not chord.is_finger_tremolo]
            grouped_chords = []
            group_positions = [0]
            for group in grouping_list:
                # todo list of beat_types

                beat_type = self.parent_part.up.time.beat_type
                if isinstance(beat_type, list):
                    raise NotImplementedError()

                group_positions.append(group_positions[-1] + group * (4. / beat_type.value))
            current_chord_index = 0
            group_positions.pop(0)
            for group_position in group_positions:
                current_grouped_chords = []
                while current_chord_index < len(chords) and chords[current_chord_index].offset < group_position:
                    current_grouped_chords.append(chords[current_chord_index])
                    current_chord_index = current_chord_index + 1

                grouped_chords.append(current_grouped_chords)
            return grouped_chords

    def _split_chords_beatwise(self):
        for beat in self.beats:
            if beat.chords:
                first_chord = beat.chords[0]
                if beat.offset < first_chord.offset:
                    previous_chord = first_chord.previous_in_part_voice
                    tail_duration = (previous_chord.end_position - beat.offset)
                    ratios = [previous_chord.quarter_duration - tail_duration, tail_duration]

                    split = previous_chord.split(ratios)
                    self._chords = substitute(self._chords, previous_chord, split)
                    beat.chords.insert(0, split[1])
                    split[1].parent_beat = beat
                    split[0]._head = True
                    split[1]._tail = True
                    # print([chord.quarter_duration for chord in split])

        for beat in self.beats:
            if beat.chords and len([chord for chord in beat.chords if chord.quarter_duration != 0]) != 1:
                last_chord = beat.chords[-1]
                if last_chord.end_position > beat.end_position:
                    head_duration = (beat.end_position - last_chord.offset)
                    ratios = [head_duration, last_chord.quarter_duration - head_duration]
                    # print(ratios)
                    split = last_chord.split(ratios)
                    self._chords = substitute(self._chords, last_chord, split)
                    beat.next.chords.insert(0, split[1])
                    split[1].parent_beat = beat.next
                    split[0]._head = True
                    split[1]._tail = True

    # //public_properties
    @property
    def beats(self):
        return self._beats

    @property
    def chords(self):
        return self._chords

    @property
    def forbidden_divisions(self):
        if self._forbidden_divisions is None:
            self._forbidden_divisions = self.parent_part.forbidden_divisions

        return self._forbidden_divisions

    @forbidden_divisions.setter
    def forbidden_divisions(self, value):
        if value is not None:
            for x in value:
                if not isinstance(x, int):
                    raise TypeError('forbidden_division must be of type int not{}'.format(type(value)))

        self._forbidden_divisions = value

    @property
    def max_division(self):
        if self._max_division is None:
            self._max_division = self.parent_part.max_division
        return self._max_division

    @max_division.setter
    def max_division(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('max_division.value must be None or of type int not {}'.format(type(value)))

        self._max_division = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise TypeError('number.value must be of type int not{}'.format(type(value)))
        self._number = value

    @property
    def parent_part(self):
        return self.parent_tree_part_staff.parent_part

    @property
    def previous(self):
        parts = self.parent_part.parent_score_part.get_parts()
        index = parts.index(self.parent_part)
        if index > 0:
            previous_part = parts[index - 1]
        else:
            return None
        try:
            return previous_part.get_voice(self.number)
        except KeyError:
            return None

    @property
    def remaining_duration(self):
        measure = self.parent_part.up
        if self.chords:
            return measure.quarter_duration - self.chords[-1].end_position
        return measure.quarter_duration

    @property
    def parent_tree_part_staff(self):
        return self._parent_tree_staff

    @parent_tree_part_staff.setter
    def parent_tree_part_staff(self, val):
        if not isinstance(val, TreePartStaff):
            raise TypeError('parent_tree_staff.value must be of type TreePartStaff not{}'.format(type(val)))
        self._parent_tree_staff = val

    @property
    def __name__(self):
        return self.parent_part.__name__ + '.' + str(self.number)

    # //public methods
    # add
    def add_beats(self, list_of_beats=None):
        if not self._preliminary_rests_adjoined:
            raise Exception('preliminary_adjoin_rests() first')

        if not self._beats_added:
            self.set_beats(list_of_beats)
            self._add_chords_to_beats()
            self._split_chords_beatwise()
            self._correct_deviations()
            self._beats_added = True
        # else:
        #     warnings.warn('beats already added to {}. No action took place.'.format(self))

    def add_chord(self, chord):
        def _append_chord(chord):
            all_chords = chord.get_pre_grace_chords() + [chord] + chord.get_post_grace_chords()
            for ch in all_chords:
                self.chords.append(ch)
                ch.parent_tree_part_voice = self
                if ch.manual_voice_number:
                    ch.add_child(Voice(str(ch.manual_voice_number)))
                else:
                    ch.add_child(Voice(str(self.number)))

        # print('treepart add_chord, chord.tie_orientation', chord.tie_orientation)
        remain = chord.quarter_duration - self.remaining_duration
        if self.remaining_duration == 0:
            return chord

        elif remain > 0:
            split = chord.split([chord.quarter_duration - remain, remain])
            first_chord = split[0]
            _append_chord(first_chord)
            first_chord._head = True
            split[1]._tail = True
            split[1].zero_mode = 'remove'
            return split[1]
        else:
            _append_chord(chord)
            return None

    # get
    def get_beats(self):
        return self.beats

    # remove
    def remove_chords(self):
        self._chords = []

    # set
    def set_beats(self, list_of_beats=None):
        if not self.parent_part.up:
            raise Exception('voice must have a part as child of a measure to be able to set beats')

        if list_of_beats is None:
            list_of_beats = []
            for time_signature in self.parent_part.up.time.get_time_signatures():
                (beats, beat_type) = time_signature
                for b in range(beats.value):
                    tree_beat = TreeBeat(duration=4. / beat_type.value)
                    list_of_beats.append(tree_beat)
                    tree_beat.parent_tree_part_voice = self
        else:
            duration = 0
            for beat in list_of_beats:
                beat.parent_tree_part_voice = self
                duration += beat.duration
            if self.parent_part.up.quarter_duration != duration:
                raise ValueError('sum of beat durations must be equal to measure duration')

        self._beats = list_of_beats

    # update
    def update_tuplets(self):
        if not self._rests_adjoined:
            raise Exception('adjoin_rests() first')

        if not self._tuplets_updated:
            for beat in self.beats:
                beat.update_tuplets()
            self._tuplets_updated = True
        # else:
        #     warnings.warn('types of chords in {} already updated. No action took place.'.format(self))

    def update_types(self):
        if not self._sextoles_substituted:
            raise Exception('substitute_sextoles() first')

        if not self._types_updated:
            for chord in self.chords:
                chord.update_type()
            self._types_updated = True
        # else:
        #     warnings.warn('types of chords in {} already updated. No action took place.'.format(self))

    def update_dots(self):
        if not self._types_updated:
            raise Exception('update_types() first')

        if not self._dots_updated:
            for chord in self.chords:
                if chord.quarter_duration != 0:
                    chord.update_dot()
            self._dots_updated = True
        # else:
        #     warnings.warn('types of chords in {} already updated. No action took place.'.format(self))

    # other
    # def adjoin_rests_in_beat(self):
    #     for beat in self.beats:
    #         beat.adjoin_rests()
    def adjoin_rests(self):
        if not self._ties_adjoined:
            raise Exception('adjoin_ties() first')
        # self._rests_adjoined = True
        if not self._rests_adjoined:
            # notatables = [1, 1.5, 2, 3, 4, 6, 8]
            notatables = [1, 2, 3, 4, 6, 8]

            chord_iterator = iter(self.chords)

            def _adjoin(current_chord, next_chord):

                def _chords_are_adjoinable():
                    condition = current_chord.is_adjoinable and next_chord.is_adjoinable
                    return condition

                def _chords_are_rest():
                    condition = current_chord.is_rest and next_chord.is_rest
                    # _print_condition('_chords_are_not_rest', condition)
                    return condition

                def _chords_have_right_positions():
                    # print 'in _chords_have_right_positions', current_chord.name, next_chord.name
                    condition = current_chord.offset % (
                        1) == 0 and next_chord.offset % 1 == 0
                    # _print_condition('_chords_have_right_positions', condition)
                    return condition

                def _result_is_notatable():
                    condition = current_chord.quarter_duration + next_chord.quarter_duration in notatables
                    # _print_condition('_result_is_notatable', condition)
                    return condition

                if _chords_are_adjoinable() and _chords_are_rest() and _chords_have_right_positions() and _result_is_notatable() and next_chord.parent_beat.best_div != 6:

                    current_chord.quarter_duration += next_chord.quarter_duration

                    next_chord.marked = True

                    try:
                        next_chord = chord_iterator.__next__()
                        next_chord = _adjoin(current_chord, next_chord)
                    except StopIteration:
                        pass

                return next_chord

            adjoin = True
            current_chord = chord_iterator.__next__()
            try:
                next_chord = chord_iterator.__next__()
            except StopIteration:
                adjoin = False

            while adjoin:
                try:
                    next_chord = _adjoin(current_chord, next_chord)
                    current_chord = next_chord
                    next_chord = chord_iterator.__next__()
                except StopIteration:
                    break

            voice_new_chords = []
            for chord in self.chords:
                try:
                    if chord.marked:
                        chord.parent_beat.chords.remove(chord)
                    else:
                        voice_new_chords.append(chord)
                except AttributeError:
                    voice_new_chords.append(chord)

            self._chords = voice_new_chords

            self._rests_adjoined = True
        # else:
        #     warnings.warn('rests in {} already adjoin_rests. No action took place.'.format(self))

    def adjoin_ties(self):
        if not self._flags_1_implemented:
            raise Exception('implement_flags() first')

        if not self._ties_adjoined:
            notatables = [1, 1.5, 2, 3, 4, 6, 8]
            # notatables = [1, 2, 3, 4, 6, 8]

            # chord_iterator = iter(reversed(self.chords))
            chord_iterator = iter(self.chords)

            def _adjoin(current_chord, next_chord):

                def _chords_are_adjoinable():
                    condition = current_chord.is_adjoinable and next_chord.is_adjoinable
                    return condition

                def _current_chord_is_all_tied():
                    condition = current_chord.is_tied_to_next
                    return condition

                def _chords_are_not_rest():
                    condition = not current_chord.is_rest and not next_chord.is_rest
                    # _print_condition('_chords_are_not_rest', condition)
                    return condition

                def _chords_have_right_positions():
                    # print 'in _chords_have_right_positions', current_chord.name, next_chord.name
                    if current_chord.quarter_duration == 0.5:
                        if current_chord.parent_beat.best_div in [6, 12]:
                            condition = False
                        else:
                            condition = current_chord.offset % (
                                1) in [0, 0.5] and next_chord.offset % 1 == 0
                    else:
                        condition = current_chord.offset % (
                            1) == 0 and next_chord.offset % 1 == 0
                    # _print_condition('_chords_have_right_positions', condition)
                    return condition

                def _result_is_notatable():
                    condition = current_chord.quarter_duration + next_chord.quarter_duration in notatables
                    # _print_condition('_result_is_notatable', condition)
                    return condition

                if _chords_are_adjoinable() and _current_chord_is_all_tied() and _chords_are_not_rest() and _chords_have_right_positions() and _result_is_notatable() and next_chord.parent_beat.best_div != 6:

                    current_chord.quarter_duration += next_chord.quarter_duration

                    if 'stop' in next_chord.tie_types and 'start' not in next_chord.tie_types:
                        current_chord.remove_tie('start')

                    try:
                        notations = next_chord.get_children_by_type(Notations)
                        slurs = []
                        for notation in notations:
                            slurs.extend(notation.get_children_by_type(Slur))
                        for slur in slurs:
                            current_chord.add_slur_object(slur)
                    except IndexError:
                        pass

                    next_chord.marked = True

                    try:
                        next_chord = chord_iterator.__next__()
                        next_chord = _adjoin(current_chord, next_chord)
                    except StopIteration:
                        pass

                return next_chord

            adjoin = True
            current_chord = chord_iterator.__next__()
            try:
                next_chord = chord_iterator.__next__()
            except StopIteration:
                adjoin = False

            while adjoin:
                try:
                    next_chord = _adjoin(current_chord, next_chord)
                    current_chord = next_chord
                    next_chord = chord_iterator.__next__()
                except StopIteration:
                    break

            voice_new_chords = []
            for chord in self.chords:

                try:
                    if chord.marked:
                        chord.parent_beat.chords.remove(chord)
                    else:
                        voice_new_chords.append(chord)
                except AttributeError as err:
                    voice_new_chords.append(chord)

            self._chords = voice_new_chords

            self._ties_adjoined = True
        # else:
        #     warnings.warn('ties of chords in {} already adjoined. No action took place.'.format(self))

    def clear_zero_heads_tails(self):
        for chord in self.chords:
            if chord.quarter_duration == 0 and (chord._head or chord._tail):
                chord.remove_from_score()

    def fill_with_rest(self):
        if not self._filled_with_rest:
            if self.remaining_duration > 0:
                if self.chords and self.chords[-1].midis[0].value == 0:
                    self.chords[-1].quarter_duration += Fraction(self.remaining_duration)
                else:
                    rest = TreeChord(midis=0, quarter_duration=self.remaining_duration)
                    rest.zero_mode = 'remove'
                    self.add_chord(rest)
            self._filled_with_rest = True

    def group_beams(self, grouping_list=None):

        def _generate_grouping_list():
            grouping_list = []
            for (beats, beat_type) in self.parent_part.up.time.get_time_signatures():
                if beats.value % 3 == 0 and beat_type.value != 4:
                    for x in range(beats.value // 3):
                        grouping_list.append(3)
                else:
                    for x in range(beats.value):
                        grouping_list.append(1)
            return grouping_list

        def _set_beams(grouped_chords):

            global begin_beam, continue_end_beam

            def add_beam(chord, chord_group, chord_group_index, number):
                global begin_beam, continue_end_beam
                beam = chord.add_child(Beam(None, number=number))
                if chord_group_index != len(chord_group) - 1:
                    if begin_beam:
                        beam.value = 'begin'
                    elif continue_end_beam:
                        if chord_group_index == len(chord_group) - 1:
                            beam.value = 'end'
                        else:
                            beam.value = 'continue'
                elif len(chord_group) > 1 and chord_group[chord_group_index - 1] != []:
                    beam.value = 'end'

            for chord_group in grouped_chords:
                begin_beam = True
                continue_end_beam = False

                for i in range(len(chord_group)):
                    chord = chord_group[i]
                    type = chord.get_children_by_type(Type)[0].value
                    numbers = {'eighth': 1, '16th': 2, '32nd': 3, '64th': 4, '128th': 5}
                    if type in numbers and chord.quarter_duration != 0:
                        for index in range(numbers[type]):
                            add_beam(chord, chord_group, i, number=index + 1)
                        if begin_beam:
                            begin_beam = False
                            continue_end_beam = True
                        elif continue_end_beam and i == len(chord_group) - 1:
                            begin_beam = True
                            continue_end_beam = False
                        # beam = chord.add_child(Beam(None))
                        # if i != len(group) - 1:
                        #     if begin_beam:
                        #         beam.value = 'begin'
                        #         begin_beam = False
                        #         continue_end_beam = True
                        #
                        #     elif continue_end_beam:
                        #         if i == len(group) - 1:
                        #             beam.value = 'end'
                        #             begin_beam = True
                        #             continue_end_beam = False
                        #         else:
                        #             beam.value = 'continue'
                        # elif len(group) > 1 and group[i - 1] != []:
                        #     beam.value = 'end'

                    elif i != 0:
                        # print('treepart group_beams, elif')
                        try:
                            beam = chord_group[i - 1].beam

                            if beam.value == 'begin':
                                chord_group[i - 1].remove_child(beam)
                                begin_beam = True
                                continue_end_beam = False
                            elif beam.value == 'continue':
                                chord_group[i - 1].beam.value = 'end'
                                begin_beam = True
                                continue_end_beam = False
                        except AttributeError:
                            pass

        if grouping_list is None:
            grouping_list = _generate_grouping_list()
            grouped_chords = self._group_beats(grouping_list)
            _set_beams(grouped_chords)
        else:
            raise NotImplementedError('group_beams with values other than None')

    def implement_flags_1(self):
        if not self._not_notatable_split:
            raise Exception('split_not_notatable() first')
        if not self._flags_1_implemented:
            self.remove_chords()
            for beat in self.beats:
                beat.implement_flags_1()
                self._chords.extend(beat.chords)
            self._flags_1_implemented = True

    def implement_flags_2(self):
        def check_implement_output(chords):
            if not isinstance(chords, list):
                raise Exception('output of implement can only be a list of chords')

            for ch in chords:
                if not isinstance(ch, TreeChord):
                    raise Exception('output of implement can only be a list of chords')

        if not self._flags_2_implemented:
            flag_types = set([flag.__class__ for flag in flatten([chord.flags for chord in self.chords]) if
                              isinstance(flag, TreeChordFlag2)])

            while flag_types:
                flag_type = flag_types.pop()
                output = []
                for chord in self.chords:
                    try:
                        chord_flag = [flag for flag in chord.flags if isinstance(flag, flag_type)][0]
                        # print(chord)
                        new_chords = chord_flag.implement(chord)
                        check_implement_output(new_chords)
                        output.extend(new_chords)

                    except IndexError:
                        output.append(chord)

                self.remove_chords()
                for chord in output:
                    try:
                        v = chord.get_children_by_type(Voice)[0]
                        chord.remove_child(v)
                    except IndexError:
                        pass
                    if self.add_chord(chord) is not None:
                        raise Exception()
        self._flags_2_implemented = True

    def implement_flags_3(self):
        def check_implement_output(chords):
            if not isinstance(chords, list):
                raise Exception('output of implement can only be a list of chords')

            # if len(chords) not in [1, 2]:
            #     raise Exception('output of implement can have 1 or 2 chords')

            for ch in chords:
                if not isinstance(ch, TreeChord):
                    raise Exception('output of implement can only be a list of chords not {}'.format(type(ch)))

        if not self._flags_3_implemented:
            flag_types = set([flag.__class__ for flag in flatten([chord.flags for chord in self.chords]) if
                              isinstance(flag, TreeChordFlag3)])

            while flag_types:
                flag_type = flag_types.pop()
                output = []
                for chord in self.chords:
                    try:
                        chord_flag = [flag for flag in chord.flags if isinstance(flag, flag_type)][0]
                        new_chords = chord_flag.implement(chord)
                        check_implement_output(new_chords)
                        output.extend(new_chords)

                    except IndexError:
                        output.append(chord)

                self.remove_chords()
                for chord in output:
                    try:
                        v = chord.get_children_by_type(Voice)[0]
                        chord.remove_child(v)
                    except IndexError:
                        pass
                    tmp = self.add_chord(chord)
                    # if tmp is not None:
                    #     print(tmp.quarter_duration)
                    #     raise Exception()

        self._flags_3_implemented = True

    def preliminary_adjoin_rests(self):
        if not self._filled_with_rest:
            raise Exception('fill_with_rest() first')

        if not self._preliminary_rests_adjoined:
            for ch in self.chords:
                ch.marked = False

            chord_iterator = iter(self.chords)

            def _adjoin(current_chord, next_chord):
                def _chords_are_adjoinable():
                    condition = current_chord.is_adjoinable and next_chord.is_adjoinable
                    return condition

                def _chords_are_rest():
                    condition = current_chord.is_rest and next_chord.is_rest
                    # _print_condition('_chords_are_not_rest', condition)
                    return condition

                if _chords_are_adjoinable() and _chords_are_rest():
                    current_chord.quarter_duration += next_chord.quarter_duration
                    next_chord.marked = True

                    try:
                        next_chord = chord_iterator.__next__()
                        next_chord = _adjoin(current_chord, next_chord)
                    except StopIteration:
                        pass

                return next_chord

            adjoin = True
            current_chord = chord_iterator.__next__()
            try:
                next_chord = chord_iterator.__next__()
            except StopIteration:
                adjoin = False

            while adjoin:
                try:
                    next_chord = _adjoin(current_chord, next_chord)
                    current_chord = next_chord
                    next_chord = chord_iterator.__next__()
                except StopIteration:
                    break

            voice_new_chords = [ch for ch in self.chords if not ch.marked]

            self._chords = voice_new_chords
            self._preliminary_rests_adjoined = True

    def split_not_notatable(self):
        if not self._quantized:
            raise Exception('quantize() first')
        # self._not_notatable_split = False
        if not self._not_notatable_split:
            self._chords = []
            for beat in self.beats:
                beat.split_not_notatable()
                self._chords.extend(beat.chords)
            self._not_notatable_split = True

        # else:
        #     warnings.warn('types of chords in {} already updated. No action took place.'.format(self))

    def substitute_sextoles(self):
        if not self._tuplets_updated:
            raise Exception('update_tuplets() first')

        if not self._sextoles_substituted:
            for beat in self.beats:
                beat.substitute_sextoles()
            self._sextoles_substituted = True
        # else:
        #     warnings.warn('all sextoles in  {} already checked. No action took place.'.format(self))

    def quantize(self):
        if not self._beats_added:
            raise Exception('add_beats() first')
        if not self._quantized:
            for beat in self.beats:
                beat.quantize()
            self._quantized = True
        # else:
        #     warnings.warn('{} already quantized. No action took place.'.format(self))


class TreePartStaff(object):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._number = None
        self._parent_part = None
        self._tree_part_voices = {}
        self.number = number

    # //public properties
    @property
    def chords(self):
        output = []
        for tree_part_voice in self.tree_part_voices.values():
            output.extend(tree_part_voice.chords)
        return output

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, val):
        if not isinstance(val, int):
            raise TypeError('number.value must be of type int not{}'.format(type(val)))
        self._number = val

    @property
    def parent_part(self):
        return self._parent_part

    @parent_part.setter
    def parent_part(self, val):
        if not isinstance(val, TreePart):
            raise TypeError('parent_part.value must be of type TreePart not{}'.format(type(val)))
        self._parent_part = val

    @property
    def tree_part_voices(self):
        return self._tree_part_voices

    # //public methods
    # add
    def add_tree_part_voice(self, tree_part_voice):
        if not isinstance(tree_part_voice, TreePartVoice):
            raise TypeError()
        if tree_part_voice.number in self.tree_part_voices.keys():
            raise AttributeError()
        tree_part_voice.parent_tree_part_staff = self
        self.tree_part_voices[tree_part_voice.number] = tree_part_voice
        return tree_part_voice

    # get
    def get_previous_measure_last_notes(self):
        previous_measure_last_notes = []
        try:
            previous_measure = self.parent_part.up.previous
        except AttributeError:
            previous_measure = None
        if previous_measure:
            previous_part = [p for p in previous_measure.get_children_by_type(TreePart) if p.id == self.parent_part.id][
                0]
            previous_staff = previous_part.get_tree_part_staff(staff_number=self.number)
            previous_measure_last_chords = []
            for tree_part_voice in previous_staff.tree_part_voices.values():
                previous_measure_last_chords.append(tree_part_voice.chords[-1])

            previous_measure_last_notes = []
            for chord in previous_measure_last_chords:
                previous_measure_last_notes.extend(chord.get_notes())
        return previous_measure_last_notes

    def get_tree_part_voice(self, voice_number):
        try:
            return self.tree_part_voices[voice_number]
        except KeyError:
            return self.set_tree_part_voice(voice_number)

    get_voice = get_tree_part_voice

    # set
    def set_tree_part_voice(self, voice_number):
        tree_part_voice = TreePartVoice(voice_number)
        return self.add_tree_part_voice(tree_part_voice)

    # update
    def update_accidentals(self, mode):
        notes = [note for chord in self.chords for note in chord.get_notes()]

        def _get_previous_measure_last_signed_notes():
            previous_measure_last_notes = self.get_previous_measure_last_notes()
            return [n for n in previous_measure_last_notes if
                    isinstance(n.event, Pitch) and n.pitch.alter and n.pitch.alter.value != 0]

        def get_accidental_info(note):
            try:
                return note.pitch.step.value, note.pitch.alter.value
            except AttributeError:
                return note.pitch.step.value, 0

        def is_in_repetition(chord):
            if chord.is_tied_to_previous:
                return False

            previous = chord.previous_in_part_voice
            while previous:
                if previous.is_tied_to_previous:
                    previous = previous.previous_in_part_voice
                else:
                    break

            if previous and chord.has_same_pitches(chord.previous_in_part_voice):
                return True

        def force_hide_accidentals():
            notes = [note for chord in self.chords for note in chord.get_notes()]
            for note in notes:
                if note.accidental._force_show:
                    note.accidental.show = True
                elif note.accidental._force_hide:
                    note.accidental.show = False

        if mode == 'normal':
            _hide_accidental = []
            _set_natural = set()
            pitched_notes = [note for chord in self.chords for note in chord.get_notes() if
                             isinstance(note.event, Pitch)]
            _first_chord_natural = [note.pitch.step.value for note in
                                    _get_previous_measure_last_signed_notes()]
            for note in pitched_notes:
                if note.pitch.alter and note.pitch.alter.value != 0 and (
                        note.pitch.step.value, note.pitch.alter.value) not in _hide_accidental:
                    if 'stop' not in [t.type for t in note.get_children_by_type(Tie)]:
                        note.accidental.show = True
                        _hide_accidental.append(get_accidental_info(note))
                    _set_natural.add(note.pitch.step.value)
                elif not note.pitch.alter or note.pitch.alter.value == 0:
                    if note.pitch.step.value in _set_natural:
                        for item in _hide_accidental:
                            if item[0] == note.pitch.step.value:
                                _hide_accidental.remove(item)

                        _set_natural.remove(note.pitch.step.value)
                        note.accidental.show = True
                    elif note.offset == 0:
                        if note.pitch.step.value in _first_chord_natural and 'stop' not in [t.type for t in
                                                                                            note.get_children_by_type(
                                                                                                Tie)]:
                            note.accidental.show = True
        elif mode == 'modern':
            _first_chord_natural = [note.pitch.step.value for note in _get_previous_measure_last_signed_notes()]
            _set_natural = set()
            for index, chord in enumerate(self.chords):
                # first chord
                if index == 0:
                    for note in chord.notes:
                        if isinstance(note.event, Rest):
                            break
                        # natural
                        elif not note.pitch.alter or (note.pitch.alter and note.pitch.alter.value == 0):
                            if note.pitch.step.value in _first_chord_natural and 'stop' not in \
                                    [t.type for t in note.get_children_by_type(Tie)]:
                                note.accidental.show = True
                        # non natural
                        else:
                            _set_natural.add(note.pitch.step.value)
                            if 'stop' not in [t.type for t in note.get_children_by_type(Tie)]:
                                note.accidental.show = True

                else:
                    # other chords
                    for note in chord.notes:
                        if isinstance(note.event, Rest):
                            break
                        # natural
                        if not note.pitch.alter or (note.pitch.alter and note.pitch.alter.value == 0):
                            if note.pitch.step.value in _set_natural:
                                note.accidental.show = True
                                _set_natural.remove(note.pitch.step.value)
                        # non natural
                        else:
                            if note.is_finger_tremolo:
                                note.accidental.show = True
                            elif is_in_repetition(chord):
                                break
                            elif 'stop' not in [t.type for t in
                                                note.get_children_by_type(Tie)]:
                                note.accidental.show = True

                            _set_natural.add(note.pitch.step.value)
        else:
            raise MusicTreeError('mode {} is not known to update accidentals'.format(mode))

        force_hide_accidentals()

    # others
    def fill_with_rest(self):
        def _fill_voices():
            highest_voice_number = max(self.tree_part_voices.keys())
            for key in range(1, highest_voice_number + 1):
                if key not in self.tree_part_voices.keys():
                    self.set_tree_part_voice(key)

        if not self.tree_part_voices:
            self.set_tree_part_voice(1)
        _fill_voices()
        for voice in self.tree_part_voices.values():
            voice.fill_with_rest()


class TreePart(timewise.Part):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attributes = self.add_child(Attributes())
        attributes.add_child(Divisions(1))
        self._max_division = None
        self._forbidden_divisions = None
        self._tree_part_staves = {}
        self._chords_notated = False
        self._divisions_updated = False
        self._finished = False
        self._accidental_mode = 'normal'
        self._parent_score_part = None

    # // private methods
    def _get_attributes(self):
        try:
            return self.get_children_by_type(Attributes)[0]
        except IndexError:
            return None

    def _get_staves_object(self):
        attributes = self._get_attributes()
        try:
            return attributes.get_children_by_type(Staves)[0]
        except (AttributeError, IndexError):
            return None

    # properties
    @property
    def accidental_mode(self):
        return self._accidental_mode

    @accidental_mode.setter
    def accidental_mode(self, value):
        self._accidental_mode = value

    @property
    def chords(self):
        output = []
        for tree_part_voice in self.tree_part_voices:
            output.extend(tree_part_voice.chords)
        return output

    @property
    def forbidden_divisions(self):
        if self._forbidden_divisions is None:
            self._forbidden_divisions = self.parent_score_part.forbidden_divisions

        return self._forbidden_divisions

    @forbidden_divisions.setter
    def forbidden_divisions(self, value):
        if value is not None:
            for x in value:
                if not isinstance(x, int):
                    raise TypeError('forbidden_division must be of type int not{}'.format(type(value)))

        self._forbidden_divisions = value

    @property
    def max_division(self):
        if self._max_division is None:
            self._max_division = self.parent_score_part.max_division
        return self._max_division

    @max_division.setter
    def max_division(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('max_division.value must be None or of type int not {}'.format(type(value)))

        self._max_division = value

    @property
    def notes(self):
        return self.get_children_by_type(TreeNote)

    @property
    def parent_score_part(self):
        return self._parent_score_part

    @parent_score_part.setter
    def parent_score_part(self, val):
        self._parent_score_part = val

    @property
    def staves(self):
        staves = self._get_staves_object()
        if staves:
            return staves.value
        else:
            return None

    @staves.setter
    def staves(self, val):
        if not isinstance(val, int):
            raise TypeError('staves.value must be of type int not{}'.format(type(val)))
        staff = self._get_staves_object()
        attributes = self._get_attributes()
        if staff is None:
            if attributes is None:
                attributes = self.add_child(Attributes())
            attributes.add_child(Staves(val))
        else:
            staff.value = val

    @property
    def tree_part_staves(self):
        return self._tree_part_staves

    @property
    def tree_part_voices(self):
        return [tree_part_voice for tree_part_staff in self.tree_part_staves.values() for tree_part_voice in
                tree_part_staff.tree_part_voices.values()]

    # @property
    # def xml_chords(self):
    #     output = []
    #     for tree_part_voice in self.tree_part_voices:
    #         output.extend(tree_part_voice.xml_chords)
    #     return output

    @property
    def __name__(self):
        index = self.up.get_children_by_type(self.__class__).index(self)
        return self.up.__name__ + '.' + str(index + 1)

    # add
    def add_beats(self, list_of_beats=None):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.add_beats(list_of_beats)

    def add_chord(self, chord, voice_number=1, staff_number=None):
        def _set_staves():
            chord.staff_number = staff_number
            clef = chord.get_clef()
            if clef and clef.number is None:
                clef.number = staff_number
            if self.staves is None or self.staves < staff_number:
                self.staves = staff_number

        measure = self.up
        if not measure:
            raise Exception('parent measure needed before adding chord to part')

        if not isinstance(chord, TreeChord):
            raise TypeError()
        tree_part_staff = self.get_tree_part_staff(staff_number)
        tree_part_voice = tree_part_staff.get_tree_part_voice(voice_number)
        if staff_number is not None:
            _set_staves()

        return tree_part_voice.add_chord(chord)

    def add_clef(self, clef):
        self._get_attributes().add_child(clef)

    def add_metronome(self, beat_unit='quarter', per_minute=60, **kwargs):
        d = self.add_child(Direction())
        dt = d.add_child(DirectionType())
        m = dt.add_child(Metronome(**kwargs))
        m.add_child(BeatUnit(beat_unit))
        m.add_child(PerMinute(str(per_minute)))
        d.add_child(Sound(tempo=per_minute))

    def add_tree_part_staff(self, tree_part_staff):
        if not isinstance(tree_part_staff, TreePartStaff):
            raise TypeError()
        if tree_part_staff.number in self.tree_part_staves.keys():
            raise AttributeError()
        self.tree_part_staves[tree_part_staff.number] = tree_part_staff
        tree_part_staff.parent_part = self
        return tree_part_staff

    # def add_voice(self, voice):
    #     self.voices[voice.number] = voice

    # // public methods

    # get
    def get_beats(self):
        output = []
        for tree_part_voice in self.tree_part_voices:
            output.extend(tree_part_voice.get_beats())
        return output

    def get_clefs(self):
        return self._get_attributes().get_children_by_type(TreeClef)

    def get_divisions(self):
        duration_denominators = [chord.quarter_duration.denominator for chord in
                                 self.chords]

        if len(duration_denominators) == 0:
            return 1
        elif len(duration_denominators) == 1:
            return duration_denominators[0]
        else:
            return lcm(duration_denominators)

    def get_previous_measure_last_notes(self):
        previous_measure_last_notes = []
        try:
            previous_measure = self.up.previous
        except AttributeError:
            previous_measure = None
        if previous_measure:
            part = [p for p in previous_measure.get_children_by_type(TreePart) if p.id == self.id][0]
            previous_measure_last_chords = []
            for tree_part_voice in part.tree_part_voices:
                previous_measure_last_chords.append(tree_part_voice.chords[-1])

            previous_measure_last_notes = []
            for chord in previous_measure_last_chords:
                previous_measure_last_notes.extend(chord.notes)
        return previous_measure_last_notes

    def get_tree_part_staff(self, staff_number):
        if staff_number is None:
            staff_number = 1
        try:
            return self.tree_part_staves[staff_number]
        except KeyError:
            return self.set_tree_part_staff(staff_number)

    get_staff = get_tree_part_staff

    # remove
    def remove_chord(self, chord):
        if not isinstance(chord, TreeChord):
            raise TypeError()

        tree_voice = self.get_voice(chord.parent_tree_part_voice.number)
        xml_voice = chord.get_children_by_type(Voice)[0]
        chord.remove_child(xml_voice)
        tree_voice.chords.remove(chord)

    # set
    def set_tree_part_staff(self, staff_number):
        tree_part_staff = TreePartStaff(staff_number)
        return self.add_tree_part_staff(tree_part_staff)

    # update
    def update_accidentals(self, mode):
        notes = [note for chord in self.chords for note in chord.get_notes()]
        self._accidental_mode = mode
        for tree_part_staff in self.tree_part_staves.values():
            tree_part_staff.update_accidentals(mode)

    def update_divisions(self):
        if not self._chords_notated:
            raise Exception('chord_to_notes() first')

        if not self._divisions_updated:
            attributes = self.get_children_by_type(Attributes)[0]
            divisions = attributes.get_children_by_type(Divisions)[0]
            divisions.value = self.get_divisions()
            self._divisions_updated = True
        else:
            warnings.warn('divisions in {} are already updated. No action took place.'.format(self))

    def update_dots(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.update_dots()

    def update_durations(self):
        for note in self.get_children_by_type(TreeNote):
            if note.quarter_duration != 0:
                note.update_duration(self.get_divisions())
        for backup in self.get_children_by_type(TreeBackup):
            backup.update_duration(self.get_divisions())

    def update_tuplets(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.update_tuplets()

    def update_types(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.update_types()

    # others
    def adjoin_ties(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.adjoin_ties()

    def adjoin_rests(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.adjoin_rests()

    # def adjoin_rests_in_beat(self):
    #     for voice in self.voices:
    #         voice.adjoin_rests_in_beat()
    def implement_flags_1(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.implement_flags_1()

    def implement_flags_2(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.implement_flags_2()

    def implement_flags_3(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.implement_flags_3()

    def group_beams(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.group_beams()

    def chords_to_notes(self):
        def _add_backup():
            self.add_child(TreeBackup(quarter_duration=tree_part_staff.parent_part.up.quarter_duration))

        for tree_part_voice in self.tree_part_voices:
            if not tree_part_voice._dots_updated:
                raise Exception('update_dots() first')

        if not self.up.previous and self.parent_score_part and self.parent_score_part.instrument:
            clefs = self.parent_score_part.instrument.standard_clefs
            if clefs:
                first_chords = [tree_part_voice.chords[0] for tree_part_voice in self.tree_part_voices]
                first_clefs = [chord.get_clef() for chord in first_chords if chord.get_clef()]
                if not first_clefs:
                    for clef in clefs:
                        if clef not in self.get_clefs():
                            self.add_clef(clef)
                    # for clef in clefs:
                    #     self.add_clef(clef)

        if not self._chords_notated:
            for staff_index, tree_part_staff in enumerate(self.tree_part_staves.values()):
                if staff_index != 0:
                    _add_backup()
                for voice_index, tree_part_voice in enumerate(tree_part_staff.tree_part_voices.values()):
                    if voice_index != 0:
                        _add_backup()
                    for chord in tree_part_voice.chords:
                        for direction in chord.get_children_by_type(Direction):
                            self.add_child(direction)
                        for attributes in chord.get_children_by_type(Attributes):
                            self.add_child(attributes)
                        for note in chord.notes:
                            self.add_child(note)
            self._chords_notated = True
        else:
            warnings.warn('chord in {} are already notated. No action took place.'.format(self))

    def fill_with_rest(self):
        if not self.tree_part_staves:
            self.set_tree_part_staff(1)
        for tree_part_staff in self.tree_part_staves.values():
            tree_part_staff.fill_with_rest()

    def preliminary_adjoin_rests(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.preliminary_adjoin_rests()

    def quantize(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.quantize()
            tree_part_voice.clear_zero_heads_tails()

    def split_not_notatable(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.split_not_notatable()

    def substitute_sextoles(self):
        for tree_part_voice in self.tree_part_voices:
            tree_part_voice.substitute_sextoles()

    def finish(self):
        if not self._finished:
            self.fill_with_rest()

            self.preliminary_adjoin_rests()

            self.add_beats()

            self.quantize()

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

            self.chords_to_notes()

            self.update_divisions()

            self.update_accidentals(mode=self.accidental_mode)

            self.update_durations()

            self.close_dtd()

            self._finished = True

    def to_string(self):
        self.finish()
        xml = self._to_xml()
        return et.tounicode(xml, pretty_print=True)
