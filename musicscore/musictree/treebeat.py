import warnings

from quicktions import Fraction

from musicscore.basic_functions import substitute
from musicscore.musictree.treechord import TreeChord
from musicscore.musicxml.types.complextypes.notations import Tuplet


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
        self._tree_part_voice = None

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
        return self._max_division

    @max_division.setter
    def max_division(self, value):
        if value is None:
            if self.duration == 0.5:
                value = 4
            else:
                value = 8

        if not isinstance(value, int):
            raise TypeError('subdivision.value must be of type int not{}'.format(type(value)))
        self._max_division = value

    @property
    def forbidden_divisions(self):
        return self._forbidden_divisions

    @forbidden_divisions.setter
    def forbidden_divisions(self, value):
        if value is not None:
            for x in value:
                if not isinstance(x, int):
                    raise TypeError('forbidden_division must be of type int  not{}'.format(type(value)))
        else:
            value = []
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
        return self._tree_part_voice

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

    def get_quantized_locations(self, subdivision):
        return _find_quantized_locations(self.duration, subdivision)

    def get_quantized_durations(self, durations):

        if sum(durations) != self.duration:
            warnings.warn('TreeBeat.get_quarter_durations: sum of durations is not equal to beat  duration')

        def _get_positions():
            positions = [0]
            for index, duration in enumerate(durations):
                positions.append(positions[index] + duration)
            return positions

        def _get_permitted_divs():
            output = list(range(1, self.max_division + 1))
            for f in self.forbidden_divisions:
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
        if len(quarter_durations) > 1:
            quarter_durations = self.get_quantized_durations(quarter_durations)
            for chord, quarter_duration in zip(self.chords, quarter_durations):
                chord.quarter_duration = quarter_duration

    def _update_tuplets(self):
        # to be used with check_notatability
        tuplet_divisions = [3, 5, 6, 7, 9, 10]

        if self.best_div in tuplet_divisions:
            for i in range(len(self.chords)):
                if i == 0:
                    self.chords[0].add_tuplet('start')
                elif i == len(self.chords) - 1:
                    self.chords[-1].add_tuplet('stop')
                else:
                    self.chords[i].add_tuplet('continue')

    def check_notatability(self):
        for chord in self.chords:
            split = None
            if chord.quarter_duration == Fraction(1, 4):
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
                    split = chord.split(4, 1)
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
                self._chords = substitute(self._chords, chord, split)

        self._update_tuplets()

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
            chords_quarter_durations = [chord.quarter_duration for chord in self.chords]
            if chords_quarter_durations not in six_divisions:
                for chord in self.chords:
                    position = chord.tuplet.position
                    chord.tuplet = Tuplet(3, position=position)
