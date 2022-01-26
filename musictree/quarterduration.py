from quicktions import Fraction


class QuarterDuration:
    """
    Type for tree chord's duration. It has a quicktions.Fraction with limited denominator 1000 as its core.
    """

    def __init__(self, *value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if not isinstance(val, Fraction):
            try:
                if isinstance(val, tuple):
                    val = Fraction(*val)
                else:
                    val = Fraction(val)
            except TypeError as err:
                msg = err.args[0]
                msg += f' not {val.__class__.__name__} {val}'
                raise TypeError(msg)
        self._value = val.limit_denominator(1000)

    def __repr__(self):
        return f"{self.__class__.__name__}:value={self.value} at {id(self)}"

    def __str__(self):
        return f"{self.__class__.__name__}:value={self.value}"

    def __eq__(self, other):
        if other is not None:
            if not isinstance(other, QuarterDuration):
                other = self.__class__(other)
            return self.value.as_integer_ratio() == other.value.as_integer_ratio()
        else:
            return False

    def __ne__(self, other):
        if other is not None:
            if not isinstance(other, QuarterDuration):
                other = self.__class__(other)
            return self.value.as_integer_ratio() != other.value.as_integer_ratio()
        else:
            return True

    def __gt__(self, other):
        if other is None:
            raise TypeError("'>' not supported between instances of 'QuarterDuration' and 'NoneType'")
        if not isinstance(other, QuarterDuration):
            other = self.__class__(other)
        return self.value.as_integer_ratio() > other.value.as_integer_ratio()

    def __ge__(self, other):
        if other is None:
            raise TypeError("'>=' not supported between instances of 'QuarterDuration' and 'NoneType'")
        if not isinstance(other, QuarterDuration):
            other = self.__class__(other)
        return self.value.as_integer_ratio() >= other.value.as_integer_ratio()

    def __lt__(self, other):
        if other is None:
            raise TypeError("'<' not supported between instances of 'QuarterDuration' and 'NoneType'")
        if not isinstance(other, QuarterDuration):
            other = self.__class__(other)
        return self.value.as_integer_ratio() < other.value.as_integer_ratio()

    def __le__(self, other):
        if other is None:
            raise TypeError("'<=' not supported between instances of 'QuarterDuration' and 'NoneType'")
        if not isinstance(other, QuarterDuration):
            other = self.__class__(other)
        return self.value.as_integer_ratio() <= other.value.as_integer_ratio()

    def __add__(self, other):
        if other is None:
            raise TypeError("unsupported operand type(s) for +: 'QuarterDuration' and 'NoneType'")
        if not isinstance(other, QuarterDuration):
            other = self.__class__(other)
        return self.__class__(self.value + other.value)

    def __mul__(self, other):
        if other is None:
            raise TypeError("unsupported operand type(s) for *: 'QuarterDuration' and 'NoneType'")
        if not isinstance(other, QuarterDuration):
            other = self.__class__(other)
        return self.__class__(self.value * other.value)

    def __truediv__(self, other):
        if other is None:
            raise TypeError("unsupported operand type(s) for /: 'QuarterDuration' and 'NoneType'")
        other = self.__class__(other)
        return self.__class__(self.value / other.value)

    def __floordiv__(self, other):
        if other is None:
            raise TypeError("unsupported operand type(s) for //: 'QuarterDuration' and 'NoneType'")
        other = self.__class__(other)
        return self.__class__(self.value // other.value)

    def __mod__(self, other):
        if other is None:
            raise TypeError("unsupported operand type(s) for %: 'QuarterDuration' and 'NoneType'")
        other = self.__class__(other)
        return self.__class__(self.value % other.value)

    def __sub__(self, other):
        if other is None:
            raise TypeError("unsupported operand type(s) for -: 'QuarterDuration' and 'NoneType'")
        other = self.__class__(other)
        return self.__class__(self.value - other.value)

    def __pow__(self, power, modulo=None):
        return self.__class__(self.value.__pow__(power, modulo))

    def __float__(self):
        return float(self.value)


def _check_quarter_duration(val):
    if not isinstance(val, int) and not isinstance(val, float) and not isinstance(val, Fraction) and not isinstance(val,
                                                                                                                    QuarterDuration):
        raise TypeError

    if val < 0:
        raise ValueError()