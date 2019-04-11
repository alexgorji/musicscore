import warnings

from quicktions import Fraction
from musicscore.musictree.treenote import TreeNote


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
        self._notes = []
        self._part = None

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
    def notes(self):
        return self._notes

    @property
    def part(self):
        return self._part

    @property
    def previous(self):
        if not self.part:
            raise Exception('beat has no part')
        index = self.part.beats.index(self)
        if index == 0:
            return None
        return self.part.beats[index - 1]

    @property
    def next(self):
        if not self.part:
            raise Exception('beat has no part')
        index = self.part.beats.index(self)
        if index == len(self.part.beats) - 1:
            return None
        return self.part.beats[index + 1]

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

    def add_note(self, note):
        if not isinstance(note, TreeNote):
            raise TypeError('{} must be of type TreeNote'.format(note))
        # if sum([note.quarter_duration for note in self.notes]) + note.quarter_duration > self.duration:
        #     raise Exception('note with quarter_duration {} cannot be added, otherwise beat duration would be exceeded')

        self.notes.append(note)

    def get_quantized_locations(self, subdivision):
        return _find_quantized_locations(self.duration, subdivision)

    def get_quantized_durations(self, durations):
        durations = [Fraction(duration).limit_denominator(1000) for duration in durations]

        if sum(durations) != self.duration:
            warnings.warn('TreeBeat.get_quantized_durations: sum of durations is not equal to beat  duration')

        def _get_positions():
            positions = [0]
            for index, duration in enumerate(durations):
                positions.append(positions[index] + duration)
            # positions.append(self.duration)
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
            quantized_duration = Fraction(
                quantized_positions[index + 1] - quantized_positions[index]).limit_denominator(
                int(best_div / self.duration))
            quantized_durations.append(quantized_duration)

        self._best_div = best_div

        return quantized_durations

    def quantize(self):
        quarter_durations = [note.quarter_duration for note in self.notes]
        if len(quarter_durations) > 1:
            quantized_durations = self.get_quantized_durations(quarter_durations)
            for note, quantized_duration in zip(self.notes, quantized_durations) :
                note.quarter_duration = quantized_duration