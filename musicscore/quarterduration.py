from typing import List, Union
from quicktions import Fraction
import numbers

__all__ = ['BEATWISE_EXCEPTIONS', 'QuarterDuration']

from musicscore.exceptions import QuarterDurationIsNotWritable

#: {offset: {quarter_duration: return value(s), ... }, ...}
BEATWISE_EXCEPTIONS = {0: {5: (3, 2), 6: (6,)}}

_note_simple_types = {
    (1, 12): '32nd',
    (1, 11): '32nd',
    (2, 11): '16th',
    (4, 11): 'eighth',
    (8, 11): 'quarter',
    (1, 10): '32nd',
    (1, 9): '32nd',
    (2, 9): '16th',
    (4, 9): 'eighth',
    (8, 9): 'quarter',
    (1, 8): '32nd',
    (1, 7): '16th',
    (2, 7): 'eighth',
    (4, 7): 'quarter',
    (1, 6): '16th',
    (1, 5): '16th',
    (2, 5): 'eighth',
    (4, 5): 'quarter',
    (8, 5): 'half',
    (1, 4): '16th',
    (2, 4): 'eighth',
    (1, 3): 'eighth',
    (2, 3): 'quarter',
    (4, 3): 'half',
    (1, 2): 'eighth',
    (1, 1): 'quarter',
    (2, 1): 'half',
    (4, 1): 'whole',
    (8, 1): 'breve',
}


class QuarterDuration(numbers.Rational):
    """
    A Class specifically designed for durations measured in quarters. The core of this class is a value of type quicktions.Fraction with a
    denominator limit of 1000, thus it can manage conversion of floats to fractions without usual inaccuracies of quintuples etc. See
    value property for more information.
    QuarterDuration has all needed magic methods for numeral comparison and conversion.
    """

    def __init__(self, *value):
        self._value = None
        self.value = value

    @property
    def numerator(self):
        """
        :return: Fraction's numerator.
        :rtype: int

        >>> QuarterDuration(1, 6).numerator
        1
        """
        return self.value.numerator

    @property
    def denominator(self):
        """
        :return: Fraction's denominator.
        :rtype: int

        >>> QuarterDuration(1, 6).denominator
        6
        """
        return self.value.denominator

    @property
    def value(self):
        """
        :return: QuarterDuration's value
        :rtype: quicktions.Fraction() with limit_denominator(1000)

        >>> QuarterDuration(3, 7).value
        Fraction(3, 7)
        >>> QuarterDuration(0.2).value
        Fraction(1, 5)
        >>> QuarterDuration(Fraction(1, 5)).value
        Fraction(1, 5)
        >>> QuarterDuration(1/5).value
        Fraction(1, 5)
        """
        return self._value

    @value.setter
    def value(self, val):
        if val is None or val == ():
            self._value = None
        elif isinstance(val, Fraction):
            self._value = val
        elif isinstance(val, str):
            self._value = Fraction(val).limit_denominator(1000)
        elif hasattr(val, '__iter__'):
            if len(val) == 1:
                self._value = Fraction(val[0]).limit_denominator(1000)
            elif len(val) == 2:
                self._value = Fraction(*val).limit_denominator(1000)
            else:
                raise ValueError

    def _get_type_and_dots(self):
        type = _note_simple_types.get(self.as_integer_ratio())
        if type:
            return type, 0
        else:
            qd = QuarterDuration(self.value * 2 / 3)
            type = _note_simple_types.get(qd.as_integer_ratio())
            if type:
                return type, 1
            else:
                qd = QuarterDuration(self.value * 4 / 7)
                type = _note_simple_types.get(qd.as_integer_ratio())
                if type:
                    return type, 2
                else:
                    raise QuarterDurationIsNotWritable(f'quarter duration {self} is not writable.')

    def as_integer_ratio(self):
        """
        :return: (numerator, denominator)
        :rtype: tuple

        >>> QuarterDuration(1, 5).as_integer_ratio()
        (1, 5)
        """
        return self.value.as_integer_ratio()

    def get_beatwise_sections(self, beats: List['Beat'], offset: Union[int, float, 'QuarterDuration', 'Fraction'] = 0):
        """
        :param beats:
        :param offset: offset in the first beat
        :return: [sections as list of QuarterDurations, leftover as QuarterDruation] leftover is the remaining quarter_duration which
                 exceeds the sum of all beats quarter durations. If there is no left over the second value in the list is None.
                 offset=0.5, beats=[Beat(1), Beat(1), Beat(1), Beat(1)] => [[0.5, 3], None]
                 See tests for more examples. In BEATWISE_EXCEPTIONS exceptions can be declared.
        """

        def _check_for_exception():
            exception = BEATWISE_EXCEPTIONS.get(offset)
            if exception:
                out = exception.get(sum(output[0]))
                if out:
                    output[0] = [QuarterDuration(value) for value in out]
                return output

        output = [None, [], None]
        if offset:
            output[0] = beats[0].quarter_duration - offset
            beats.pop(0)
        leftover = self - output[0] if output[0] is not None else self
        out_of_reach = leftover - sum(b.quarter_duration for b in beats)
        if out_of_reach > 0:
            leftover -= out_of_reach
            output[2] = out_of_reach
        for beat in beats:
            if leftover >= beat.quarter_duration:
                current_value = beat.quarter_duration
                leftover -= current_value
            else:
                current_value = leftover
                leftover = 0
            if not output[1]:
                output[1] = [current_value]
            else:
                if _is_writable(output[1][-1] + current_value):
                    output[1][-1] += current_value
                else:
                    output[1].append(current_value)
            if leftover == 0:
                break
        if output[0]:
            output = [[output[0], *output[1]], output[2]]
        else:
            output = [output[1], output[2]]

        exception = _check_for_exception()
        if exception:
            return exception

        return output

    def get_type(self):
        return self._get_type_and_dots()[0]

    def get_number_of_dots(self):
        return self._get_type_and_dots()[1]

    def __repr__(self):
        return f'{self.value.numerator}/{self.value.denominator}'

    def __str__(self):
        return f'QuarterDuration: {str(self.value)}'

    def __abs__(self):
        return QuarterDuration(self.value.__abs__())

    def __add__(self, other):
        return QuarterDuration(self.value.__add__(_convert_other(other)))

    def __ceil__(self):
        return QuarterDuration(self.value.__ceil__())

    def __floor__(self):
        return QuarterDuration(self.value.__floor__())

    def __floordiv__(self, other):
        return QuarterDuration(self.value.__floordiv__(_convert_other(other)))

    def __gt__(self, other):
        return self.value.__gt__(_convert_other(other))

    def __ge__(self, other):
        return self.value.__ge__(_convert_other(other))

    def __hash__(self):
        return self.value.__hash__()

    def __le__(self, other):
        return self.value.__le__(_convert_other(other))

    def __lt__(self, other):
        return QuarterDuration(self.value.__lt__(_convert_other(other)))

    def __mod__(self, other):
        return QuarterDuration(self.value.__mod__(_convert_other(other)))

    def __mul__(self, other):
        return QuarterDuration(self.value.__mul__(_convert_other(other)))

    def __neg__(self):
        return self.value.__neg__()

    def __pos__(self):
        return self.value.__pos__()

    def __pow__(self, power, modulo=None):
        return QuarterDuration(self.value.__pos__(power, modulo))

    def __radd__(self, other):
        return QuarterDuration(self.value.__radd__(_convert_other(other)))

    def __rfloordiv__(self, other):
        return QuarterDuration(self.value.__rfloordiv__(_convert_other(other)))

    def __rmod__(self, other):
        return QuarterDuration(self.value.__rmod__(_convert_other(other)))

    def __rmul__(self, other):
        return QuarterDuration(self.value.__rmul__(_convert_other(other)))

    def __round__(self, n=None):
        return QuarterDuration(self.value.__round__(n))

    def __rpow__(self, other):
        return QuarterDuration(self.value.__rpow__(_convert_other(other)))

    def __rtruediv__(self, other):
        return QuarterDuration(self.value.__rtruediv__(_convert_other(other)))

    def __truediv__(self, other):
        return QuarterDuration(self.value.__truediv__(_convert_other(other)))

    def __trunc__(self):
        return self.value.__trunc__()

    def __eq__(self, other):
        return self.value.__eq__(_convert_other(other))

    def __copy__(self):
        return self.__class__(self.value)

    def __deepcopy__(self, memodict={}):
        return self.__class__(self.value)


def _is_writable(quarter_duration: Union[float, int, Fraction, 'QuarterDuration']):
    """
    Function to check if a quarter duration is writable or must be split into two durations.

    :param quarter_duration:
    :return: boolean

    >>> _is_writable(5)
    False
    >>> _is_writable(7/8)
    False
    >>> _is_writable(3/8)
    True
    """
    writables = {1 / 64,
                 1 / 32,
                 3 / 64,
                 1 / 16,
                 3 / 32,
                 1 / 8,
                 3 / 16,
                 1 / 4,
                 3 / 8,
                 1 / 2,
                 3 / 4,
                 1,
                 3 / 2,
                 2,
                 3,
                 4,
                 6,
                 8,
                 12}

    if quarter_duration in writables:
        return True
    else:
        return False


def _convert_other(other):
    if isinstance(other, QuarterDuration):
        return other.value

    return Fraction(other).limit_denominator(1000)


class QuarterDurationMixin:
    """
    Mixin for all Classes with a quarter_duration. Used in :obj:`~musicscore.note.Note`, :obj:`~musicscore.chord.Chord` and
    :obj:`~musicscore.beat.Beat`
    """

    def __init__(self, quarter_duration=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quarter_duration = None
        self.quarter_duration = quarter_duration

    def _set_quarter_duration(self, val):
        if isinstance(val, QuarterDuration):
            self._quarter_duration = val
        else:
            _check_quarter_duration_value(val)
            self._quarter_duration = QuarterDuration(val)

    @property
    def quarter_duration(self) -> QuarterDuration:
        """
        Duration measured in quarters.

        val type: Optional[int, float, Fraction, QuarterDuration]
        """
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, val):
        if val is not None:
            self._set_quarter_duration(val)
        else:
            self._quarter_duration = None


def _check_quarter_duration_value(val):
    if not isinstance(val, int) and not isinstance(val, float) and not isinstance(val, Fraction) and not isinstance(val,
                                                                                                                    QuarterDuration):
        raise TypeError(f'Wrong type for quarter duration {val}: {type(val)}')

    if val < 0:
        raise ValueError()

    return True