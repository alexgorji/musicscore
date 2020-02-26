import warnings

from lxml import etree as et
from quicktions import Fraction

from musicscore.basic_functions import lcm, substitute, flatten
from musicscore.musictree.exceptions import MusicTreeError
from musicscore.musictree.treebeat import TreeBeat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treechordflags2 import TreeChordFlag2
from musicscore.musictree.treechordflags3 import TreeChordFlag3
from musicscore.musictree.treenote import TreeNote, TreeBackup
from musicscore.musicxml.elements import timewise as timewise
from musicscore.musicxml.elements.fullnote import Pitch, Rest
from musicscore.musicxml.elements.note import Beam, Type, Tie, Notations
from musicscore.musicxml.groups.common import Voice
from musicscore.musicxml.groups.musicdata import Direction, Attributes
from musicscore.musicxml.types.complextypes.attributes import Divisions
from musicscore.musicxml.types.complextypes.direction import DirectionType, Sound
from musicscore.musicxml.types.complextypes.directiontype import Metronome
from musicscore.musicxml.types.complextypes.metronome import BeatUnit, PerMinute
from musicscore.musicxml.types.complextypes.notations import Slur


class XMLChord(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._notes = []
        self._parent_voice = None

    def add_note(self, note):
        if self.notes:
            if note.offset != self.offset:
                raise ValueError('notes of XMLChord must have the same offset')
            note_voice_number = note.get_children_by_type(Voice)[0].value

            if note_voice_number != self.voice_number:
                raise ValueError('notes of XMLChord must have the same voice number {} and {}'.format(note_voice_number,
                                                                                                      self.voice_number))
        self._notes.append(note)

    @property
    def notes(self):
        return self._notes

    @property
    def parent_voice(self):
        return self._parent_voice

    @parent_voice.setter
    def parent_voice(self, value):
        if not isinstance(value, TreePartVoice):
            raise TypeError()
        self._parent_voice = value

    @property
    def offset(self):
        if self.notes:
            return self.notes[-1].offset
        else:
            return None

    @property
    def voice_number(self):
        if self.notes:
            return self.notes[-1].get_children_by_type(Voice)[0].value

    @property
    def previous(self):
        index = self.parent_voice.xml_chords.index(self)
        if index == 0:
            return None
        return self.parent_voice.xml_chords[index - 1]

    @property
    def is_tied_to_previous(self):
        for note in self.notes:
            if 'stop' in [t.type for t in note.get_children_by_type(Tie)]:
                return True
        return False

    def has_same_pitches(self, xml_chord):
        if len(self.notes) == len(xml_chord.notes):
            for note_1, note_2 in zip(self.notes, xml_chord.notes):
                if isinstance(note_1.event, Rest) or isinstance(note_2.event, Rest):
                    return False
                pitch_1 = note_1.pitch.dump()
                pitch_2 = note_2.pitch.dump()
                if len(pitch_1) == len(pitch_2):
                    for i in range(1, len(pitch_1)):
                        if pitch_1[i].value != pitch_2[i].value:
                            return False
                    return True
        return False


class TreePartVoice(object):
    def __init__(self, number=1, *args, **kwargs):
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
        self._flags_implemented = False
        self._not_notatable_split = False
        self._ties_adjoined = False
        self._rests_adjoined = False
        self._tuplets_updated = False
        self._sextoles_substituted = False
        self._types_updated = False
        self._dots_updated = False
        self._flags2_implemented = False
        self._flags3_implemented = False
        self.parent_part = None
        self._xml_chords = None

    @property
    def __name__(self):
        # return self.parent_part.__name__ + ' ' + 'v:' + str(self.number)

        return self.parent_part.__name__ + '.' + str(self.number)

    @property
    def chords(self):
        return self._chords

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise TypeError('number.value must be of type int not{}'.format(type(value)))
        self._number = value

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
    def next(self):
        parts = self.parent_part.parent_score_part.get_parts()
        index = parts.index(self.parent_part)
        if index < len(parts):
            next_part = parts[index + 1]
        else:
            return None
        try:
            return next_part.get_voice(self.number)
        except KeyError:
            return None

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

    def add_chord(self, chord):
        def _append_chord(chord):
            all_chords = chord.get_pre_grace_chords() + [chord] + chord.get_post_grace_chords()
            for ch in all_chords:
                self.chords.append(ch)
                ch.parent_voice = self
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

    def remove_chords(self):
        self._chords = []

    @property
    def remaining_duration(self):
        measure = self.parent_part.up
        if self.chords:
            return measure.quarter_duration - self.chords[-1].end_position
        return measure.quarter_duration

    @property
    def xml_chords(self):
        if not self._xml_chords:
            xml_chords = []
            for note in [note for note in self.parent_part.get_children_by_type(TreeNote)]:
                offset_voices = [(xml_chord.offset, xml_chord.voice_number) for xml_chord in xml_chords]
                note_offset_voice = (note.offset, note.get_children_by_type(Voice)[0].value)
                if note_offset_voice in offset_voices:
                    index = offset_voices.index(note_offset_voice)
                    xml_chord = xml_chords[index]
                    xml_chord.add_note(note)
                else:
                    xml_chord = XMLChord()
                    xml_chord.parent_voice = self
                    xml_chord.add_note(note)
                    xml_chords.append(xml_chord)
            self._xml_chords = xml_chords

        return self._xml_chords

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
                    tree_beat.parent_voice = self
        else:
            duration = 0
            for beat in list_of_beats:
                beat.parent_voice = self
                duration += beat.duration
            if self.parent_part.up.quarter_duration != duration:
                raise ValueError('sum of beat durations must be equal to measure duration')

        self._beats = list_of_beats

    @property
    def beats(self):
        return self._beats

    def get_beats(self):
        return self.beats

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

    def _split_chords_beatwise(self):

        for beat in self.beats:
            if beat.chords:
                first_chord = beat.chords[0]
                if beat.offset < first_chord.offset:
                    previous_chord = first_chord.previous
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

    def quantize(self):
        if not self._beats_added:
            raise Exception('add_beats() first')
        if not self._quantized:
            for beat in self.beats:
                beat.quantize()
            self._quantized = True
        # else:
        #     warnings.warn('{} already quantized. No action took place.'.format(self))

    def clear_zero_heads_tails(self):
        for chord in self.chords:
            if chord.quarter_duration == 0 and (chord._head or chord._tail):
                chord.remove_from_score()

    # def adjoin_rests_in_beat(self):
    #     for beat in self.beats:
    #         beat.adjoin_rests()

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

    def implement_flags(self):
        if not self._not_notatable_split:
            raise Exception('split_not_notatable() first')
        if not self._flags_implemented:
            self.remove_chords()
            for beat in self.beats:
                beat.implement_flags()
                self._chords.extend(beat.chords)
            self._flags_implemented = True

    def adjoin_ties(self):
        if not self._flags_implemented:
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

    def update_tuplets(self):
        if not self._rests_adjoined:
            raise Exception('adjoin_rests() first')

        if not self._tuplets_updated:
            for beat in self.beats:
                beat.update_tuplets()
            self._tuplets_updated = True
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

    def implement_flags_2(self):
        def check_implement_output(chords):
            if not isinstance(chords, list):
                raise Exception('output of implement can only be a list of chords')

            # if len(chords) not in [1, 2]:
            #     raise Exception('output of implement can have 1 or 2 chords')

            for ch in chords:
                if not isinstance(ch, TreeChord):
                    raise Exception('output of implement can only be a list of chords')

        if not self._flags2_implemented:
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
        self._flags2_implemented = True

    def implement_flags_3(self):
        def check_implement_output(chords):
            if not isinstance(chords, list):
                raise Exception('output of implement can only be a list of chords')

            # if len(chords) not in [1, 2]:
            #     raise Exception('output of implement can have 1 or 2 chords')

            for ch in chords:
                if not isinstance(ch, TreeChord):
                    raise Exception('output of implement can only be a list of chords not {}'.format(type(ch)))

        if not self._flags3_implemented:
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

        self._flags3_implemented = True


class TreePart(timewise.Part):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attributes = self.add_child(Attributes())
        attributes.add_child(Divisions(1))
        self._max_division = None
        self._forbidden_divisions = None
        self._voices = {}
        self._chords_notated = False
        self._divisions_updated = False
        self._finished = False
        self.parent_score_part = None
        self._accidental_mode = 'normal'

    @property
    def __name__(self):
        index = self.up.get_children_by_type(self.__class__).index(self)
        return self.up.__name__ + '.' + str(index + 1)

    @property
    def chords(self):
        output = []
        for voice in self.voices.values():
            output.extend(voice.chords)
        return output

    @property
    def voices(self):
        return self._voices

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
    def accidental_mode(self):
        return self._accidental_mode

    @accidental_mode.setter
    def accidental_mode(self, value):
        self._accidental_mode = value

    @property
    def xml_chords(self):
        output = []
        for voice in self.voices.values():
            output.extend(voice.xml_chords)
        return output

    def get_divisions(self):
        duration_denominators = [chord.quarter_duration.denominator for chord in
                                 self.chords]

        if len(duration_denominators) == 0:
            return 1
        elif len(duration_denominators) == 1:
            return duration_denominators[0]
        else:
            return lcm(duration_denominators)

    @property
    def notes(self):
        return self.get_children_by_type(TreeNote)

    def set_voice(self, voice_number):
        self.voices[voice_number] = TreePartVoice(voice_number)
        self.voices[voice_number].parent_part = self
        return self.voices[voice_number]

    def get_voice(self, voice_number):
        try:
            return self.voices[voice_number]
        except KeyError:
            return self.set_voice(voice_number)

    def add_chord(self, chord, voice_number=1):
        measure = self.up
        if not measure:
            raise Exception('parent measure needed before adding chord to part')

        if not isinstance(chord, TreeChord):
            raise TypeError()

        voice = self.get_voice(voice_number)
        return voice.add_chord(chord)

    def remove_chord(self, chord):
        if not isinstance(chord, TreeChord):
            raise TypeError()

        tree_voice = self.get_voice(chord.parent_voice.number)
        xml_voice = chord.get_children_by_type(Voice)[0]
        chord.remove_child(xml_voice)
        tree_voice.chords.remove(chord)

    def get_beats(self):
        output = []
        for voice in self.voices.values():
            output.extend(voice.get_beats())
        return output

    def group_beams(self):
        for voice in self.voices.values():
            voice.group_beams()

    def chords_to_notes(self):
        for voice in self.voices.values():
            if not voice._dots_updated:
                raise Exception('update_dots() first')

        if not self.up.previous and self.parent_score_part and self.parent_score_part.instrument:
            clef = self.parent_score_part.instrument.standard_clef
            if clef:
                first_chords = [voice.chords[0] for voice in self.voices.values()]
                first_clefs = [chord.get_clef() for chord in first_chords if chord.get_clef()]
                if not first_clefs:
                    first_chords[0].add_clef(clef)

        if not self._chords_notated:
            for index, voice in enumerate(self.voices.values()):
                if index != 0:
                    self.add_child(TreeBackup(quarter_duration=voice.parent_part.up.quarter_duration))
                for chord in voice.chords:
                    for direction in chord.get_children_by_type(Direction):
                        self.add_child(direction)
                    for attributes in chord.get_children_by_type(Attributes):
                        self.add_child(attributes)
                    for note in chord._notes:
                        self.add_child(note)
            self._chords_notated = True
        else:
            warnings.warn('chord in {} are already notated. No action took place.'.format(self))

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

    def get_previous_measure_last_notes(self):
        previous_measure_last_notes = []
        try:
            previous_measure = self.up.previous
        except AttributeError:
            previous_measure = None
        if previous_measure:
            part = [p for p in previous_measure.get_children_by_type(TreePart) if p.id == self.id][0]
            voices = part.voices.values()
            previous_measure_last_chords = []
            for voice in voices:
                previous_measure_last_chords.append(voice.chords[-1])

            previous_measure_last_notes = []
            for chord in previous_measure_last_chords:
                previous_measure_last_notes.extend(chord._notes)
        return previous_measure_last_notes

    def update_accidentals(self, mode):
        self._accidental_mode = mode

        def _get_previous_measure_last_signed_notes():
            previous_measure_last_notes = self.get_previous_measure_last_notes()
            return [n for n in previous_measure_last_notes if
                    isinstance(n.event, Pitch) and n.pitch.alter and n.pitch.alter.value != 0]

        def get_accidental_info(note):
            try:
                return (note.pitch.step.value, note.pitch.alter.value)
            except AttributeError:
                return (note.pitch.step.value, 0)

        def is_in_repetition(xml_chord):
            if xml_chord.is_tied_to_previous:
                return False

            previous = xml_chord.previous
            while previous:
                if previous.is_tied_to_previous:
                    previous = previous.previous
                else:
                    break

            if previous and xml_chord.has_same_pitches(xml_chord.previous):
                return True

        if mode == 'normal':
            _hide_accidental = []
            _set_natural = set()
            pitched_notes = [note for note in self.get_children_by_type(TreeNote) if isinstance(note.event, Pitch)]
            _first_chord_natural = [note.pitch.step.value for note in
                                    _get_previous_measure_last_signed_notes()]

            for note in pitched_notes:
                if note.pitch.alter and note.pitch.alter.value != 0 and (
                        note.pitch.step.value, note.pitch.alter.value) not in _hide_accidental:
                    if 'stop' not in [t.type for t in note.get_children_by_type(Tie)]:
                        note.accidental.show = True
                        _hide_accidental.append(get_accidental_info(note))
                    _set_natural.add(note.pitch.step.value)
                elif (
                        not note.pitch.alter or note.pitch.alter.value == 0):
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
            for index, xml_chord in enumerate(self.xml_chords):
                # first xml_chord
                if index == 0:
                    for note in xml_chord.notes:
                        if isinstance(note.event, Rest):
                            break
                        # natural
                        elif not note.pitch.alter or (note.pitch.alter and note.pitch.alter.value == 0):
                            if note.pitch.step.value in _first_chord_natural and 'stop' not in [t.type for t in
                                                                                                note.get_children_by_type(
                                                                                                    Tie)]:
                                note.accidental.show = True
                        # non natural
                        else:
                            _set_natural.add(note.pitch.step.value)
                            if 'stop' not in [t.type for t in note.get_children_by_type(Tie)]:
                                note.accidental.show = True

                else:
                    # other xml_chords
                    for note in xml_chord.notes:
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
                            elif is_in_repetition(xml_chord):
                                break
                            elif 'stop' not in [t.type for t in
                                                note.get_children_by_type(Tie)]:
                                note.accidental.show = True

                            _set_natural.add(note.pitch.step.value)
        else:
            raise MusicTreeError('mode {} is not known to update accidentals'.format(mode))

    def fill_with_rest(self):
        if self.voices == {}:
            self.set_voice(1)
        for voice in self.voices.values():
            voice.fill_with_rest()

    def preliminary_adjoin_rests(self):
        for voice in self.voices.values():
            voice.preliminary_adjoin_rests()

    def add_beats(self, list_of_beats=None):
        for voice in self.voices.values():
            voice.add_beats(list_of_beats)

    def quantize(self):
        for voice in self.voices.values():
            voice.quantize()
            voice.clear_zero_heads_tails()

    # def adjoin_rests_in_beat(self):
    #     for voice in self.voices.values():
    #         voice.adjoin_rests_in_beat()

    def split_not_notatable(self):
        for voice in self.voices.values():
            voice.split_not_notatable()

    def implement_flags(self):
        for voice in self.voices.values():
            voice.implement_flags()

    def adjoin_ties(self):
        for voice in self.voices.values():
            voice.adjoin_ties()

    def adjoin_rests(self):
        for voice in self.voices.values():
            voice.adjoin_rests()

    def update_tuplets(self):
        for voice in self.voices.values():
            voice.update_tuplets()

    def substitute_sextoles(self):
        for voice in self.voices.values():
            voice.substitute_sextoles()

    def update_types(self):
        for voice in self.voices.values():
            voice.update_types()

    def update_dots(self):
        for voice in self.voices.values():
            voice.update_dots()

    def implement_flags_2(self):
        for voice in self.voices.values():
            voice.implement_flags_2()

    def implement_flags_3(self):
        for voice in self.voices.values():
            voice.implement_flags_3()

    def update_durations(self):
        for note in self.get_children_by_type(TreeNote):
            if note.quarter_duration != 0:
                note.update_duration(self.get_divisions())
        for backup in self.get_children_by_type(TreeBackup):
            backup.update_duration(self.get_divisions())

    def add_metronome(self, beat_unit='quarter', per_minute=60, **kwargs):
        d = self.add_child(Direction())
        dt = d.add_child(DirectionType())
        m = dt.add_child(Metronome(**kwargs))
        m.add_child(BeatUnit(beat_unit))
        m.add_child(PerMinute(str(per_minute)))
        d.add_child(Sound(tempo=per_minute))

    def add_voice(self, voice):
        self.voices[voice.number] = voice

    def finish(self):
        if not self._finished:
            self.fill_with_rest()

            self.preliminary_adjoin_rests()

            self.add_beats()

            self.quantize()

            self.split_not_notatable()

            self.implement_flags()

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
