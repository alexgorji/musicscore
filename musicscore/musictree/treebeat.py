import math
import warnings

from quicktions import Fraction

from musicscore.basic_functions import flatten
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treechordflags1 import TreeChordFlag1, FingerTremoloFlag1
from musicscore.musicxml.elements.note import TimeModification
from musicscore.musicxml.types.complextypes.timemodification import ActualNotes, NormalNotes, NormalType


class BeatException(BaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class WrongPositionInBeat(BeatException):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


def _find_nearest_quantized_value(quantized_values, values):
    output = []
    for value in values:
        nearest_quantized = min(enumerate(quantized_values), key=lambda x: abs(x[1] - value))[1]
        delta = nearest_quantized - value
        output.append((nearest_quantized, delta))
    return output


def _find_q_delta(quantized_locations, values):
    qs = _find_nearest_quantized_value(quantized_locations, values)
    d = 0
    for q in qs:
        d += abs(q[1])
    return d


def _find_quantized_locations(duration, subdivision):
    output = range(subdivision + 1)
    fr = duration / subdivision
    output = [x * fr for x in output]
    return output


class TreeBeat(object):
    def __init__(self, duration=1, max_division=None, forbidden_divisions=None):
        self._duration = None
        self._max_division = None
        self._forbidden_divisions = None
        self._best_div = None
        self._permitted_durations = (4, 2, 1, 0.5)
        self._chords = []
        self.parent_tree_part_voice = None

        self.duration = duration
        self.max_division = max_division
        self.forbidden_divisions = forbidden_divisions

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if self._duration is None:
            if value not in self._permitted_durations:
                raise ValueError('beat_duration can only be in {}'.format(self._permitted_durations))
        else:
            raise Exception('duration can be set by initialization')

        self._duration = Fraction(value)

    @property
    def max_division(self):
        if self._max_division is None:
            parent_max_division = self.parent_tree_part_voice.max_division
            if parent_max_division:
                self._max_division = math.floor(parent_max_division * self.duration)
                if self._max_division == 0:
                    self._max_division = 1

        if self._max_division is None:
            if self.duration == 0.5:
                self._max_division = 4
            else:
                self._max_division = 8

        return self._max_division

    @max_division.setter
    def max_division(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('max_division.value must be None or of type int not {}'.format(type(value)))
        self._max_division = value

    @property
    def forbidden_divisions(self):
        if self._forbidden_divisions is None:
            self._forbidden_divisions = self.parent_tree_part_voice.forbidden_divisions

        if self._forbidden_divisions is None:
            self._forbidden_divisions = []

        return self._forbidden_divisions

    @forbidden_divisions.setter
    def forbidden_divisions(self, value):
        if value is not None:
            for x in value:
                if not isinstance(x, int):
                    raise TypeError('forbidden_division must be of type int  not{}'.format(type(value)))
        # max_division = int(max_division / 2)
        # forbidden_divisions = [div // 2 for div in forbidden_divisions if div // 2 != 0]
        # forbidden_divisions = list(set(forbidden_divisions))
        self._forbidden_divisions = value

    @property
    def best_div(self):
        return self._best_div

    @property
    def chords(self):
        return self._chords

    @property
    def tree_part_voice(self):
        return self.parent_tree_part_voice

    @property
    def previous(self):
        if not self.tree_part_voice:
            raise Exception('beat has no voice')
        index = self.tree_part_voice.beats.index(self)
        if index == 0:
            return None
        return self.tree_part_voice.beats[index - 1]

    @property
    def next(self):
        if not self.tree_part_voice:
            raise Exception('beat has no voice')
        index = self.tree_part_voice.beats.index(self)
        if index == len(self.tree_part_voice.beats) - 1:
            return None
        return self.tree_part_voice.beats[index + 1]

    @property
    def offset(self):
        if self.previous:
            output = self.previous.offset + self.previous.duration
            return output
        else:
            return 0

    @property
    def end_position(self):
        return self.offset + self.duration

    def add_chord(self, chord):
        if not isinstance(chord, TreeChord):
            raise TypeError('{} must be of type TreeChord'.format(chord))
        chord.parent_beat = self
        self.chords.append(chord)
        if chord.position_in_beat > self.duration:
            self.chords.remove(chord)
            raise WrongPositionInBeat()

    def remove_chords(self):
        self._chords = []

    def clear_chords(self):
        self._chords = []

    def get_quantized_locations(self, subdivision):
        return _find_quantized_locations(self.duration, subdivision)

    def get_quantized_durations(self, durations):
        diff = self.duration - sum(durations)
        if diff != 0:
            for index, dur in enumerate(durations):
                durations[index] = dur + diff / len(durations)
        if sum(durations) != self.duration:
            warnings.warn('TreeBeat.get_quarter_durations: sum of durations {} is not equal to beat duration {}'.format(
                sum(durations), self.duration))

        def _get_positions():
            positions = [0]
            for index, duration in enumerate(durations):
                positions.append(positions[index] + duration)
            return positions

        def _get_permitted_divs():
            output = list(range(1, self.max_division + 1))
            for f in self.forbidden_divisions:
                if f in output:
                    output.remove(f)
            return output

        permitted_divs = _get_permitted_divs()
        positions = _get_positions()

        best_div = permitted_divs.pop(0)
        last_q_delta = _find_q_delta(self.get_quantized_locations(subdivision=best_div), positions)

        for div in permitted_divs:
            current_q_delta = _find_q_delta(self.get_quantized_locations(subdivision=div), positions)

            if current_q_delta < last_q_delta:
                best_div = div
                last_q_delta = current_q_delta

            elif (current_q_delta == last_q_delta) and (div < best_div):
                best_div = div

        quantized_positions = [f[0] for f in
                               _find_nearest_quantized_value(self.get_quantized_locations(subdivision=best_div),
                                                             positions)]
        quantized_durations = []

        for index, duration in enumerate(durations):
            quarter_duration = Fraction(
                quantized_positions[index + 1] - quantized_positions[index]).limit_denominator(
                int(best_div / self.duration))
            quantized_durations.append(quarter_duration)

        self._best_div = best_div
        return quantized_durations

    def quantize(self):
        quarter_durations = [chord.quarter_duration for chord in self.chords]
        if len([d for d in quarter_durations if d != 0]) > 1:
            quarter_durations = self.get_quantized_durations(quarter_durations)
            for chord, quarter_duration in zip(self.chords, quarter_durations):
                chord.quarter_duration = quarter_duration
                chord._offset = None

    def split_not_notatable(self):
        # print(self.offset, [ch.quarter_duration for ch in self.chords])
        output = []
        for chord in self.chords:
            split = None
            if chord.quarter_duration == Fraction(5, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(3, 2)
            elif chord.quarter_duration == Fraction(7, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(4, 3)
            elif chord.quarter_duration == Fraction(9, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(4, 5)
            elif chord.quarter_duration == Fraction(10, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(4, 6)
            elif chord.quarter_duration == Fraction(11, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(4, 7)
            elif chord.quarter_duration == Fraction(13, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 5)
            elif chord.quarter_duration == Fraction(14, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 6)
            elif chord.quarter_duration == Fraction(15, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 7)
            elif chord.quarter_duration == Fraction(16, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 8)
            elif chord.quarter_duration == Fraction(17, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 9)
            elif chord.quarter_duration == Fraction(18, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 10)
            elif chord.quarter_duration == Fraction(19, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 11)
            elif chord.quarter_duration == Fraction(20, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 12)
            elif chord.quarter_duration == Fraction(21, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 13)
            elif chord.quarter_duration == Fraction(22, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 14)
            elif chord.quarter_duration == Fraction(23, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 15)
            elif chord.quarter_duration == Fraction(24, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 16)
            elif chord.quarter_duration == Fraction(25, 1):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 17)
            elif chord.quarter_duration == Fraction(3, 2):
                if chord.position_in_beat == 0.5:
                    split = chord.split(1, 2)
            elif chord.quarter_duration == Fraction(5, 2):
                if chord.position_in_beat == 0:
                    split = chord.split(2, 3)
                elif chord.position_in_beat == 0.5:
                    split = chord.split(1, 4)
            elif chord.quarter_duration == Fraction(7, 2):
                if chord.position_in_beat == 0:
                    split = chord.split(4, 3)
                elif chord.position_in_beat == 0.5:
                    split = chord.split(1, 6)
            elif chord.quarter_duration == Fraction(9, 2):
                if chord.position_in_beat == 0:
                    split = chord.split(8, 1)

            elif chord.quarter_duration == Fraction(1, 4):
                if chord.position_in_beat == Fraction(3, 8):
                    split = chord.split(1, 1)
            elif chord.quarter_duration == Fraction(3, 8):
                if chord.position_in_beat == Fraction(3, 8):
                    split = chord.split(1, 2)
            elif chord.quarter_duration == Fraction(5, 6) and self.best_div == 6:
                if chord.position_in_beat == Fraction(0, 6):
                    split = chord.split(4, 1)
                elif chord.position_in_beat == Fraction(1, 6):
                    split = chord.split(1, 4)

            elif chord.quarter_duration == Fraction(5, 7):
                if chord.position_in_beat == Fraction(0, 7):
                    split = chord.split(3, 2)
                elif chord.position_in_beat == Fraction(1, 7):
                    split = chord.split(3, 2)
                elif chord.position_in_beat == Fraction(2, 7):
                    split = chord.split(2, 3)

            elif chord.quarter_duration == Fraction(5, 8):
                if chord.position_in_beat == Fraction(0, 8):
                    split = chord.split(4, 1)
                elif chord.position_in_beat == Fraction(1, 8):
                    split = chord.split(3, 2)
                elif chord.position_in_beat == Fraction(2, 8):
                    split = chord.split(2, 3)
                elif chord.position_in_beat == Fraction(3, 8):
                    split = chord.split(1, 4)
                else:
                    raise Exception('something wrong with split')


            # elif chord.quarter_duration == Fraction(7,8):
            #     if chord.position_in_beat == Fraction(0,8):
            #         split = chord.split(Fraction(4,8), Fraction(3,8))
            #     elif chord.position_in_beat == Fraction(1,8):
            #         split = chord.split(Fraction(3,8), Fraction(4,8))

            elif chord.quarter_duration == Fraction(5, 9):
                if chord.position_in_beat == Fraction(0, 9):
                    split = chord.split(4, 1)
                elif chord.position_in_beat == Fraction(1, 9):
                    split = chord.split(1, 4)
                elif chord.position_in_beat == Fraction(2, 9):
                    split = chord.split(1, 4)
                elif chord.position_in_beat == Fraction(3, 9):
                    split = chord.split(1, 4)
                elif chord.position_in_beat == Fraction(4, 9):
                    split = chord.split(4, 1)

            elif chord.quarter_duration == Fraction(7, 9):
                if chord.position_in_beat == Fraction(0, 9):
                    split = chord.split(6, 1)
                elif chord.position_in_beat == Fraction(1, 9):
                    split = chord.split(2, 5)
                elif chord.position_in_beat == Fraction(2, 9):
                    split = chord.split(1, 6)

            elif chord.quarter_duration == Fraction(5, 10) and self.best_div == 10:
                if chord.position_in_beat == Fraction(0, 10):
                    split = chord.split(3, 2)
                elif chord.position_in_beat == Fraction(1, 10):
                    split = chord.split(3, 2)
                elif chord.position_in_beat == Fraction(2, 10):
                    split = chord.split(2, 3)
                elif chord.position_in_beat == Fraction(3, 10):
                    split = chord.split(3, 2)
                elif chord.position_in_beat == Fraction(4, 10):
                    split = chord.split(2, 3)
                elif chord.position_in_beat == Fraction(5, 10):
                    split = chord.split(3, 2)

            elif chord.quarter_duration == Fraction(6, 10) and self.best_div == 10:
                if chord.position_in_beat == Fraction(0, 10):
                    split = chord.split(3, 3)
                elif chord.position_in_beat == Fraction(3, 10):
                    split = chord.split(3, 3)
                elif chord.position_in_beat == Fraction(4, 10):
                    split = chord.split(3, 3)

            elif chord.quarter_duration == Fraction(7, 10):
                if chord.position_in_beat == Fraction(0, 10):
                    split = chord.split(3, 4)
                elif chord.position_in_beat == Fraction(1, 10):
                    split = chord.split(3, 4)
                elif chord.position_in_beat == Fraction(2, 10):
                    split = chord.split(1, 6)
                elif chord.position_in_beat == Fraction(3, 10):
                    split = chord.split(4, 3)

            elif chord.quarter_duration == Fraction(9, 10):
                if chord.position_in_beat == Fraction(0, 10):
                    split = chord.split(3, 6)
                elif chord.position_in_beat == Fraction(1, 10):
                    split = chord.split(3, 6)
            # elif chord.quarter_duration == Fraction(5, 11):
            #     if chord.position_in_beat == Fraction(0, 11):
            #         split = chord.split(Fraction(4, 11), Fraction(1, 11))
            #     elif chord.position_in_beat == Fraction(1, 11):
            #         split = chord.split(Fraction(3, 11), Fraction(2, 11))
            #     elif chord.position_in_beat == Fraction(2, 11):
            #         split = chord.split(Fraction(2, 11), Fraction(3, 11))
            #     elif chord.position_in_beat == Fraction(3, 11):
            #         split = chord.split(Fraction(1, 11), Fraction(4, 11))
            #     elif chord.position_in_beat == Fraction(4, 11):
            #         split = chord.split(Fraction(4, 11), Fraction(1, 11))
            #     elif chord.position_in_beat == Fraction(5, 11):
            #         split = chord.split(Fraction(3, 11), Fraction(2, 11))
            #     elif chord.position_in_beat == Fraction(6, 11):
            #         split = chord.split(Fraction(3, 11), Fraction(2, 11))
            #
            # elif chord.quarter_duration == Fraction(7, 11):
            #     if chord.position_in_beat == Fraction(0, 11):
            #         split = chord.split(Fraction(4, 11), Fraction(3, 11))
            #     elif chord.position_in_beat == Fraction(1, 11):
            #         split = chord.split(Fraction(3, 11), Fraction(4, 11))
            #     elif chord.position_in_beat == Fraction(2, 11):
            #         split = chord.split(Fraction(4, 11), Fraction(3, 11))
            #     elif chord.position_in_beat == Fraction(3, 11):
            #         split = chord.split(Fraction(3, 11), Fraction(4, 11))
            #     elif chord.position_in_beat == Fraction(4, 11):
            #         split = chord.split(Fraction(4, 11), Fraction(3, 11))
            #
            # elif chord.quarter_duration == Fraction(10, 11):
            #     if chord.position_in_beat == Fraction(0, 11):
            #         split = chord.split(Fraction(4, 11), Fraction(6, 11))
            #     elif chord.position_in_beat == Fraction(1, 11):
            #         split = chord.split(Fraction(4, 11), Fraction(6, 11))
            #
            # elif chord.quarter_duration == Fraction(9, 11):
            #     if chord.position_in_beat == Fraction(0, 11):
            #         split = chord.split(Fraction(8, 11), Fraction(1, 11))
            #     elif chord.position_in_beat == Fraction(1, 11):
            #         split = chord.split(Fraction(1, 11), Fraction(8, 11))
            #     elif chord.position_in_beat == Fraction(2, 11):
            #         split = chord.split(Fraction(1, 11), Fraction(8, 11))
            #
            # elif chord.quarter_duration == Fraction(5, 12):
            #     if chord.position_in_beat == Fraction(0, 12):
            #         split = chord.split(Fraction(4, 12), Fraction(1, 12))
            #     elif chord.position_in_beat == Fraction(1, 12):
            #         split = chord.split(Fraction(3, 12), Fraction(2, 12))
            #     elif chord.position_in_beat == Fraction(2, 12):
            #         split = chord.split(Fraction(2, 12), Fraction(3, 12))
            #     elif chord.position_in_beat == Fraction(3, 12):
            #         split = chord.split(Fraction(1, 12), Fraction(4, 12))
            #     elif chord.position_in_beat == Fraction(4, 12):
            #         split = chord.split(Fraction(4, 12), Fraction(1, 12))
            #     elif chord.position_in_beat == Fraction(5, 12):
            #         split = chord.split(Fraction(3, 12), Fraction(2, 12))
            #     elif chord.position_in_beat == Fraction(6, 12):
            #         split = chord.split(Fraction(2, 12), Fraction(3, 12))
            #     elif chord.position_in_beat == Fraction(7, 12):
            #         split = chord.split(Fraction(1, 12), Fraction(4, 12))
            #
            # elif chord.quarter_duration == Fraction(6, 12):
            #     if chord.position_in_beat == Fraction(5, 12):
            #         split = chord.split(Fraction(3, 12), Fraction(3, 12))
            #
            # elif chord.quarter_duration == Fraction(7, 12):
            #     if chord.position_in_beat == Fraction(0, 12):
            #         split = chord.split(Fraction(4, 12), Fraction(3, 12))
            #     elif chord.position_in_beat == Fraction(1, 12):
            #         split = chord.split(Fraction(3, 12), Fraction(4, 12))
            #     elif chord.position_in_beat == Fraction(2, 12):
            #         split = chord.split(Fraction(4, 12), Fraction(3, 12))
            #     elif chord.position_in_beat == Fraction(3, 12):
            #         split = chord.split(Fraction(3, 12), Fraction(4, 12))
            #     elif chord.position_in_beat == Fraction(4, 12):
            #         split = chord.split(Fraction(4, 12), Fraction(3, 12))
            #     elif chord.position_in_beat == Fraction(5, 12):
            #         split = chord.split(Fraction(3, 12), Fraction(4, 12))
            #
            # elif chord.quarter_duration == Fraction(9, 12) and self.best_div == 12:
            #     if chord.position_in_beat == Fraction(0, 12):
            #         split = chord.split(Fraction(6, 12), Fraction(3, 12))
            #     if chord.position_in_beat == Fraction(1, 12):
            #         split = chord.split(Fraction(3, 12), Fraction(6, 12))
            #     if chord.position_in_beat == Fraction(2, 12):
            #         split = chord.split(Fraction(3, 12), Fraction(6, 12))
            #     if chord.position_in_beat == Fraction(3, 12):
            #         split = chord.split(Fraction(6, 12), Fraction(3, 12))
            #
            # elif chord.quarter_duration == Fraction(10, 12) and self.best_div == 12:
            #     if chord.position_in_beat == Fraction(0, 12):
            #         split = chord.split(Fraction(6, 12), Fraction(4, 12))
            #     if chord.position_in_beat == Fraction(1, 12):
            #         split = chord.split(Fraction(6, 12), Fraction(4, 12))
            #     if chord.position_in_beat == Fraction(2, 12):
            #         split = chord.split(Fraction(6, 12), Fraction(4, 12))
            #
            # elif chord.quarter_duration == Fraction(11, 12):
            #     if chord.position_in_beat == Fraction(0, 12):
            #         split = chord.split(Fraction(8, 12), Fraction(3, 12))
            #
            #     elif chord.position_in_beat == Fraction(1, 12):
            #         split = chord.split(Fraction(3, 12), Fraction(8, 12))
            if split:
                output.extend(split)
            else:
                output.append(chord)
        self.remove_chords()
        for ch in output:
            try:
                self.add_chord(ch)
            except WrongPositionInBeat:
                number_of_next_beats = (self.chords[-1].position_in_beat + self.chords[
                    -1].quarter_duration) / self.duration
                if number_of_next_beats != int(number_of_next_beats):
                    raise Exception()
                next_beat = self.next
                while number_of_next_beats > 1:
                    next_beat = next_beat.next
                    number_of_next_beats -= 1
                if next_beat.chords:
                    raise Exception()
                next_beat.add_chord(ch)
        # self._chords = output

    def implement_flags_1(self):
        # print('implement flags for', self.offset)
        # print('chords', self.chords)
        # print([ch.quarter_duration for ch in self.chords])

        def check_implement_output(chords):
            if not isinstance(chords, list):
                raise Exception('output of implement can only be a list of chords')

            # if len(chords) not in [1, 2]:
            #     raise Exception('output of implement can have 1 or 2 chords')

            for ch in chords:
                if not isinstance(ch, TreeChord):
                    raise Exception('output of implement can only be a list of chords')

        flag_types = set([flag.__class__ for flag in flatten([chord.flags for chord in self.chords]) if
                          isinstance(flag, TreeChordFlag1)])

        while flag_types:
            flag_type = flag_types.pop()
            output = []
            for chord in self.chords:
                try:
                    chord_flag = [flag for flag in chord.flags if isinstance(flag, flag_type)][0]
                    new_chords = chord_flag.implement(chord, self)
                    check_implement_output(new_chords)
                    diff = sum([ch.quarter_duration for ch in new_chords]) - self.duration
                    if len(new_chords) == 1:
                        output.extend(new_chords)
                    else:
                        if diff > 0 and (isinstance(chord_flag, FingerTremoloFlag1) or
                                         chord.position_in_beat + new_chords[0].quarter_duration >= self.duration):
                            next_beat = self.next

                            if not next_beat.chords:
                                next_beat.add_chord(new_chords[-1])
                            else:
                                raise Exception('next_beat is not empty.')

                            output.extend(new_chords[:-1])
                        else:
                            output.extend(new_chords)

                except IndexError:
                    output.append(chord)

            self._chords = output
            self.split_not_notatable()

    #
    # def adjoin_rests(self):
    #     _adjoin = True
    #     if len(self.chords) > 1:
    #         for chord in self.chords:
    #             if not chord.is_rest or not chord.is_adjoinable:
    #                 _adjoin = False
    #                 break
    #
    #         if _adjoin:
    #             first_chord = self.chords[0]
    #             first_chord.quarter_duration = self.duration
    #             for chord in self.chords[1:]:
    #                 chord.parent_tree_part_voice.chords.remove(chord)
    #
    #             self.remove_chords()
    #             self.add_chord(first_chord)

    # chord_iterator = iter(self.chords)

    #
    #
    # def _adjoin(current_chord, next_chord):
    #
    #     def _chords_are_adjoinable():
    #         condition = current_chord.is_adjoinable and next_chord.is_adjoinable
    #         return condition
    #
    #     def _chords_are_rest():
    #         condition = current_chord.is_rest and next_chord.is_rest
    #         # _print_condition('_chords_are_not_rest', condition)
    #         return condition
    #
    #     # def _chords_have_right_positions():
    #     #     # print 'in _chords_have_right_positions', current_chord.name, next_chord.name
    #     #     condition = current_chord.offset % (
    #     #         1) == 0 and next_chord.offset % 1 == 0
    #     #     # _print_condition('_chords_have_right_positions', condition)
    #     #     return condition
    #
    #     # def _result_is_notatable():
    #     #     condition = current_chord.quarter_duration + next_chord.quarter_duration in notatables
    #     #     # _print_condition('_result_is_notatable', condition)
    #     #     return condition
    #
    #     if _chords_are_adjoinable() and _chords_are_rest():
    #         current_chord.quarter_duration += next_chord.quarter_duration
    #         next_chord.marked = True
    #
    #         try:
    #             next_chord = chord_iterator.__next__()
    #             next_chord = _adjoin(current_chord, next_chord)
    #         except StopIteration:
    #             pass
    #
    #     return next_chord
    #
    # adjoin = True
    #
    # try:
    #     current_chord = chord_iterator.__next__()
    #     next_chord = chord_iterator.__next__()
    # except StopIteration:
    #     adjoin = False
    #
    # while adjoin:
    #     try:
    #         next_chord = _adjoin(current_chord, next_chord)
    #         current_chord = next_chord
    #         next_chord = chord_iterator.__next__()
    #     except StopIteration:
    #         break
    #
    # beat_new_chords = []
    # for chord in self.chords:
    #     try:
    #         if chord.marked:
    #             # chord.parent_tree_part_voice.chords.remove(chord)
    #             pass
    #         else:
    #             beat_new_chords.append(chord)
    #     except AttributeError:
    #         beat_new_chords.append(chord)
    #
    # if self.chords != beat_new_chords:
    #     print([ch.quarter_duration for ch in self.chords])
    #     print([ch.quarter_duration for ch in beat_new_chords])
    #     self.remove_chords()
    #     for ch in beat_new_chords:
    #         self.add_chord(ch)
    #     self.split_not_notatable()

    def update_tuplets(self):
        tuplet_divisions = [3, 5, 6, 7, 9, 10]
        non_grace_chords = [chord for chord in self.chords if
                            chord.quarter_duration != 0 and not chord.is_finger_tremolo]

        if self.best_div in tuplet_divisions:
            for i in range(len(non_grace_chords)):
                if i == 0:
                    non_grace_chords[0].add_tuplet('start')
                elif i == len(non_grace_chords) - 1:
                    non_grace_chords[-1].add_tuplet('stop')
                else:
                    non_grace_chords[i].add_tuplet('continue')

    def substitute_sextoles(self):
        six_divisions = (
            [Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(1, 6)],
            [Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(1, 3), Fraction(1, 6)],
            [Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(1, 2)],
            [Fraction(1, 6), Fraction(1, 3), Fraction(1, 3), Fraction(1, 6)],
            [Fraction(1, 6), Fraction(1, 3), Fraction(1, 6), Fraction(1, 6), Fraction(1, 6)],
            [Fraction(1, 6), Fraction(1, 3), Fraction(1, 2)],
            # [Fraction(1,6), Fraction(1,2), Fraction(1,3)],
            [Fraction(1, 6), Fraction(2, 3), Fraction(1, 6)],

            [Fraction(1, 3), Fraction(1, 6), Fraction(1, 3), Fraction(1, 6)],
            [Fraction(1, 3), Fraction(1, 6), Fraction(1, 2)],
            # [Fraction(1,3), Fraction(1,2), Fraction(1,6)],
            [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)],
            [Fraction(1, 2), Fraction(1, 6), Fraction(1, 6), Fraction(1, 6)]
        )

        if self.best_div == 6:
            non_grace_chords = [chord for chord in self.chords if chord.quarter_duration != 0]
            chords_quarter_durations = [chord.quarter_duration for chord in non_grace_chords]
            if chords_quarter_durations not in six_divisions:
                for chord in non_grace_chords:
                    tm = chord.get_children_by_type(TimeModification)[0]
                    tm.get_children_by_type(ActualNotes)[0].value = 3
                    tm.get_children_by_type(NormalNotes)[0].value = 2
                    tm.get_children_by_type(NormalType)[0].value = 'eighth'
