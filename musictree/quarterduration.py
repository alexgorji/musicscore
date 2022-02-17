from quicktions import Fraction
import numbers


def _check_quarter_duration(val):
    if not isinstance(val, int) and not isinstance(val, float) and not isinstance(val, Fraction) and not isinstance(val, QuarterDuration):
        raise TypeError(f'Wrong type for quarter duration: {type(val)}')

    if val < 0:
        raise ValueError()


def is_writable(quarter_duration):
    if quarter_duration in [1 / 64, 1 / 32, 3 / 64, 1 / 16, 3 / 32, 1 / 8, 3 / 16, 1 / 4, 3 / 8, 1 / 2, 3 / 4, 1, 3 / 2, 2, 3, 4, 6, 8, 12]:
        return True
    else:
        return False


def _convert_other(other):
    if isinstance(other, QuarterDuration):
        return other.value

    return Fraction(other).limit_denominator(1000)


class QuarterDuration(numbers.Rational):

    def __init__(self, *value):
        self._value = None
        self.value = value

    @property
    def numerator(self):
        return self.value.numerator

    @property
    def denominator(self):
        return self.value.denominator

    @property
    def value(self):
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

    def as_integer_ratio(self):
        return self.value.as_integer_ratio()

    def get_beatwise_sections(self, beats, offset=0):
        output = [None, [], None]
        if offset:
            output[0] = beats[0].quarter_duration - offset
            beats.pop(0)
        remaining_value = self - output[0] if output[0] is not None else self
        out_of_reach = remaining_value - sum([b.quarter_duration for b in beats])
        if out_of_reach > 0:
            remaining_value -= out_of_reach
            output[2] = out_of_reach
        for beat in beats:
            if remaining_value >= beat.quarter_duration:
                current_value = beat.quarter_duration
                remaining_value -= current_value
            else:
                current_value = remaining_value
                remaining_value = 0
            if not output[1]:
                output[1] = [current_value]
            else:
                if is_writable(output[1][-1] + current_value):
                    output[1][-1] += current_value
                else:
                    output[1].append(current_value)
            if remaining_value == 0:
                break
        if output[0]:
            output = [[output[0], *output[1]], output[2]]
        else:
            output = [output[1], output[2]]

        # Add conditions for other beat groupings
        if offset == 0 and sum(output[0]) == 5:
            output[0] = [QuarterDuration(3), QuarterDuration(2)]
        elif offset == 0 and sum(output[0]) == 6:
            output[0] = [QuarterDuration(6)]

        return output

    def __repr__(self):
        return f'QuarterDuration: {repr(self.value)} {id(self)}'

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


class QuarterDurationMixin:
    def __init__(self, quarter_duration=None):
        self._quarter_duration = None
        self.quarter_duration = quarter_duration

    def _set_quarter_duration(self, val):
        _check_quarter_duration(val)
        if isinstance(val, QuarterDuration):
            self._quarter_duration = val
        else:
            self._quarter_duration = QuarterDuration(val)

    @property
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, val):
        if val is not None:
            self._set_quarter_duration(val)
        else:
            self._quarter_duration = None
