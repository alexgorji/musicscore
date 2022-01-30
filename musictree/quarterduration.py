import math
from fractions import Fraction
import numbers
import operator


def _check_quarter_duration(val):
    if not isinstance(val, int) and not isinstance(val, float) and not isinstance(val, Fraction):
        raise TypeError

    if val < 0:
        raise ValueError()


def is_writable(quarter_duration):
    if quarter_duration in [1 / 64, 1 / 32, 3 / 64, 1 / 16, 3 / 32, 1 / 8, 3 / 16, 1 / 4, 3 / 8, 1 / 2, 3 / 4, 1, 3 / 2, 2, 3, 4, 6, 8, 12]:
        return True
    else:
        return False


def get_beatwise_sections(quarter_duration, beats, offset=0):
    output = [None, [], None]
    if offset:
        output[0] = beats[0].quarter_duration - offset
        beats.pop(0)
    remaining_value = quarter_duration - output[0] if output[0] is not None else quarter_duration
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
    return output


class QuarterDuration(Fraction):
    def limit_denominator(self, max_denominator=1000):
        """Closest Fraction to self with denominator at most max_denominator.

        >>> Fraction('3.141592653589793').limit_denominator(10)
        Fraction(22, 7)
        >>> Fraction('3.141592653589793').limit_denominator(100)
        Fraction(311, 99)
        >>> Fraction(4321, 8765).limit_denominator(10000)
        Fraction(4321, 8765)

        """
        # Algorithm notes: For any real number x, define a *best upper
        # approximation* to x to be a rational number p/q such that:
        #
        #   (1) p/q >= x, and
        #   (2) if p/q > r/s >= x then s > q, for any rational r/s.
        #
        # Define *best lower approximation* similarly.  Then it can be
        # proved that a rational number is a best upper or lower
        # approximation to x if, and only if, it is a convergent or
        # semiconvergent of the (unique shortest) continued fraction
        # associated to x.
        #
        # To find a best rational approximation with denominator <= M,
        # we find the best upper and lower approximations with
        # denominator <= M and take whichever of these is closer to x.
        # In the event of a tie, the bound with smaller denominator is
        # chosen.  If both denominators are equal (which can happen
        # only when max_denominator == 1 and self is midway between
        # two integers) the lower bound---i.e., the floor of self, is
        # taken.

        if max_denominator < 1:
            raise ValueError("max_denominator should be at least 1")
        if self._denominator <= max_denominator:
            return Fraction(self)

        p0, q0, p1, q1 = 0, 1, 1, 0
        n, d = self._numerator, self._denominator
        while True:
            a = n // d
            q2 = q0 + a * q1
            if q2 > max_denominator:
                break
            p0, q0, p1, q1 = p1, q1, p0 + a * p1, q2
            n, d = d, n - a * d

        k = (max_denominator - q0) // q1
        bound1 = Fraction(p0 + k * p1, q0 + k * q1)
        bound2 = Fraction(p1, q1)
        if abs(bound2 - self) <= abs(bound1 - self):
            return bound2
        else:
            return bound1

    def _operator_fallbacks(monomorphic_operator, fallback_operator):
        """Generates forward and reverse operators given a purely-rational
        operator and a function from the operator module.

        Use this like:
        __op__, __rop__ = _operator_fallbacks(just_rational_op, operator.op)

        In general, we want to implement the arithmetic operations so
        that mixed-mode operations either call an implementation whose
        author knew about the types of both arguments, or convert both
        to the nearest built in type and do the operation there. In
        Fraction, that means that we define __add__ and __radd__ as:

            def __add__(self, other):
                # Both types have numerators/denominator attributes,
                # so do the operation directly
                if isinstance(other, (int, Fraction)):
                    return Fraction(self.numerator * other.denominator +
                                    other.numerator * self.denominator,
                                    self.denominator * other.denominator)
                # float and complex don't have those operations, but we
                # know about those types, so special case them.
                elif isinstance(other, float):
                    return float(self) + other
                elif isinstance(other, complex):
                    return complex(self) + other
                # Let the other type take over.
                return NotImplemented

            def __radd__(self, other):
                # radd handles more types than add because there's
                # nothing left to fall back to.
                if isinstance(other, numbers.Rational):
                    return Fraction(self.numerator * other.denominator +
                                    other.numerator * self.denominator,
                                    self.denominator * other.denominator)
                elif isinstance(other, Real):
                    return float(other) + float(self)
                elif isinstance(other, Complex):
                    return complex(other) + complex(self)
                return NotImplemented


        There are 5 different cases for a mixed-type addition on
        Fraction. I'll refer to all of the above code that doesn't
        refer to Fraction, float, or complex as "boilerplate". 'r'
        will be an instance of Fraction, which is a subtype of
        Rational (r : Fraction <: Rational), and b : B <:
        Complex. The first three involve 'r + b':

            1. If B <: Fraction, int, float, or complex, we handle
               that specially, and all is well.
            2. If Fraction falls back to the boilerplate code, and it
               were to return a value from __add__, we'd miss the
               possibility that B defines a more intelligent __radd__,
               so the boilerplate should return NotImplemented from
               __add__. In particular, we don't handle Rational
               here, even though we could get an exact answer, in case
               the other type wants to do something special.
            3. If B <: Fraction, Python tries B.__radd__ before
               Fraction.__add__. This is ok, because it was
               implemented with knowledge of Fraction, so it can
               handle those instances before delegating to Real or
               Complex.

        The next two situations describe 'b + r'. We assume that b
        didn't know about Fraction in its implementation, and that it
        uses similar boilerplate code:

            4. If B <: Rational, then __radd_ converts both to the
               builtin rational type (hey look, that's us) and
               proceeds.
            5. Otherwise, __radd__ tries to find the nearest common
               base ABC, and fall back to its builtin type. Since this
               class doesn't subclass a concrete type, there's no
               implementation to fall back to, so we need to try as
               hard as possible to return an actual value, or the user
               will get a TypeError.

        """

        def forward(a, b):
            if isinstance(b, (int, Fraction)):
                return monomorphic_operator(a, b)
            elif isinstance(b, float):
                return fallback_operator(float(a), b)
            elif isinstance(b, complex):
                return fallback_operator(complex(a), b)
            else:
                return NotImplemented

        forward.__name__ = '__' + fallback_operator.__name__ + '__'
        forward.__doc__ = monomorphic_operator.__doc__

        def reverse(b, a):
            if isinstance(a, numbers.Rational):
                # Includes ints.
                return monomorphic_operator(a, b)
            elif isinstance(a, numbers.Real):
                return fallback_operator(float(a), float(b))
            elif isinstance(a, numbers.Complex):
                return fallback_operator(complex(a), complex(b))
            else:
                return NotImplemented

        reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
        reverse.__doc__ = monomorphic_operator.__doc__

        return forward, reverse

    def _add(a, b):
        """a + b"""
        da, db = a.denominator, b.denominator
        output = QuarterDuration(a.numerator * db + b.numerator * da,
                        da * db)
        return output

    __add__, __radd__ = _operator_fallbacks(_add, operator.add)

    def _sub(a, b):
        """a - b"""
        da, db = a.denominator, b.denominator
        return QuarterDuration(a.numerator * db - b.numerator * da,
                        da * db)

    __sub__, __rsub__ = _operator_fallbacks(_sub, operator.sub)

    def _mul(a, b):
        """a * b"""
        return QuarterDuration(a.numerator * b.numerator, a.denominator * b.denominator)

    __mul__, __rmul__ = _operator_fallbacks(_mul, operator.mul)

    def _div(a, b):
        """a / b"""
        return QuarterDuration(a.numerator * b.denominator,
                        a.denominator * b.numerator)

    __truediv__, __rtruediv__ = _operator_fallbacks(_div, operator.truediv)

    def _floordiv(a, b):
        """a // b"""
        return (a.numerator * b.denominator) // (a.denominator * b.numerator)

    __floordiv__, __rfloordiv__ = _operator_fallbacks(_floordiv, operator.floordiv)

    def _divmod(a, b):
        """(a // b, a % b)"""
        da, db = a.denominator, b.denominator
        div, n_mod = divmod(a.numerator * db, da * b.numerator)
        return div, QuarterDuration(n_mod, da * db)

    __divmod__, __rdivmod__ = _operator_fallbacks(_divmod, divmod)

    def _mod(a, b):
        """a % b"""
        da, db = a.denominator, b.denominator
        return QuarterDuration((a.numerator * db) % (b.numerator * da), da * db)

    __mod__, __rmod__ = _operator_fallbacks(_mod, operator.mod)

    def __pow__(a, b):
        """a ** b

        If b is not an integer, the result will be a float or complex
        since roots are generally irrational. If b is an integer, the
        result will be rational.

        """
        if isinstance(b, numbers.Rational):
            if b.denominator == 1:
                power = b.numerator
                if power >= 0:
                    return QuarterDuration(a._numerator ** power,
                                    a._denominator ** power,
                                    _normalize=False)
                elif a._numerator >= 0:
                    return QuarterDuration(a._denominator ** -power,
                                    a._numerator ** -power,
                                    _normalize=False)
                else:
                    return QuarterDuration((-a._denominator) ** -power,
                                    (-a._numerator) ** -power,
                                    _normalize=False)
            else:
                # A fractional power will generally produce an
                # irrational number.
                return float(a) ** float(b)
        else:
            return float(a) ** b

    def __rpow__(b, a):
        """a ** b"""
        if b._denominator == 1 and b._numerator >= 0:
            # If a is an int, keep it that way if possible.
            return a ** b._numerator

        if isinstance(a, numbers.Rational):
            return QuarterDuration(a.numerator, a.denominator) ** b

        if b._denominator == 1:
            return a ** b._numerator

        return a ** float(b)

    def __pos__(a):
        """+a: Coerces a subclass instance to Fraction"""
        return QuarterDuration(a._numerator, a._denominator, _normalize=False)

    def __neg__(a):
        """-a"""
        return QuarterDuration(-a._numerator, a._denominator, _normalize=False)

    def __abs__(a):
        """abs(a)"""
        return QuarterDuration(abs(a._numerator), a._denominator, _normalize=False)

    def __trunc__(a):
        """trunc(a)"""
        if a._numerator < 0:
            return -(-a._numerator // a._denominator)
        else:
            return a._numerator // a._denominator

    def __floor__(a):
        """math.floor(a)"""
        return a.numerator // a.denominator

    def __ceil__(a):
        """math.ceil(a)"""
        # The negations cleverly convince floordiv to return the ceiling.
        return -(-a.numerator // a.denominator)

    def __round__(self, ndigits=None):
        """round(self, ndigits)

        Rounds half toward even.
        """
        if ndigits is None:
            floor, remainder = divmod(self.numerator, self.denominator)
            if remainder * 2 < self.denominator:
                return floor
            elif remainder * 2 > self.denominator:
                return floor + 1
            # Deal with the half case:
            elif floor % 2 == 0:
                return floor
            else:
                return floor + 1
        shift = 10 ** abs(ndigits)
        # See _operator_fallbacks.forward to check that the results of
        # these operations will always be Fraction and therefore have
        # round().
        if ndigits > 0:
            return QuarterDuration(round(self * shift), shift)
        else:
            return QuarterDuration(round(self / shift) * shift)
    def __eq__(a, b):
        """a == b"""
        if type(b) is int:
            return a._numerator == b and a._denominator == 1
        if isinstance(b, numbers.Rational):
            return (a._numerator == b.numerator and
                    a._denominator == b.denominator)
        if isinstance(b, numbers.Complex) and b.imag == 0:
            b = b.real
        if isinstance(b, float):
            if math.isnan(b) or math.isinf(b):
                # comparisons with an infinity or nan should behave in
                # the same way for any finite a, so treat a as zero.
                return 0.0 == b
            else:
                return a == a.from_float(b).limit_denominator(1000)
        else:
            # Since a doesn't know how to compare with b, let's give b
            # a chance to compare itself with a.
            return NotImplemented

    def _richcmp(self, other, op):
        """Helper for comparison operators, for internal use only.

        Implement comparison between a Rational instance `self`, and
        either another Rational instance or a float `other`.  If
        `other` is not a Rational instance or a float, return
        NotImplemented. `op` should be one of the six standard
        comparison operators.

        """
        # convert other to a Rational instance where reasonable.
        if isinstance(other, numbers.Rational):
            return op(self._numerator * other.denominator,
                      self._denominator * other.numerator)
        if isinstance(other, float):
            if math.isnan(other) or math.isinf(other):
                return op(0.0, other)
            else:
                return op(self, self.from_float(other).limit_denominator(1000))
        else:
            return NotImplemented

    def __lt__(a, b):
        """a < b"""
        return a._richcmp(b, operator.lt)

    def __gt__(a, b):
        """a > b"""
        return a._richcmp(b, operator.gt)

    def __le__(a, b):
        """a <= b"""
        return a._richcmp(b, operator.le)

    def __ge__(a, b):
        """a >= b"""
        return a._richcmp(b, operator.ge)

    def __bool__(a):
        """a != 0"""
        # bpo-39274: Use bool() because (a._numerator != 0) can return an
        # object which is not a bool.
        return bool(a._numerator)


#     """
#     Type for tree chord's duration. It has a quicktions.Fraction with limited denominator 1000 as its core.
#     """
#
#     def __init__(self, *args):
#         super().__init__(1)
#         # if len(args) == 2:
#         #     self.numerator, self.denominator = args
#         # if len(args) == 1:
#         #     if isinstance(args[1], str):
#         #         super(QuarterDuration, self).__init__(args[1])
#         #     print(args[1])
#         #
#         # super().__init__(*args)
#         # print(args)
#         # if len(args) == 1:
#         #     print(args[0])
#         #     super().__init__(args[0])
#         # else:
#         #     super().__init__(*args)
#         self.limit_denominator = 1000
#
#     def get_beatwise_sections(self, beats, offset=0):
#         output = [None, [], None]
#         remaining_value = self
#         for beat in beats:
#             if remaining_value >= beat.quarter_duration:
#                 current_value = beat.quarter_duration
#                 print(current_value)
#                 print(remaining_value)
#                 remaining_value -= current_value
#             else:
#                 current_value = remaining_value
#                 remaining_value = 0
#             if not output[1]:
#                 output[1] = current_value
#             else:
#                 if is_writable(output[1] + current_value):
#                     output[1] += current_value
#                 else:
#                     output[1].append(current_value)
#
#         return output
#     #
#     # def __repr__(self):
#     #     return f"{self.__class__.__name__}:value={self.value} at {id(self)}"
#     #
#     # def __str__(self):
#     #     return f"{self.__class__.__name__}:value={self.value}"
#     #
#     # def __eq__(self, other):
#     #     if other is not None:
#     #         if not isinstance(other, QuarterDuration):
#     #             other = self.__class__(other)
#     #         return self.value == other.value
#     #     else:
#     #         return False
#     #
#     # def __ne__(self, other):
#     #     if other is not None:
#     #         if not isinstance(other, QuarterDuration):
#     #             other = self.__class__(other)
#     #         return self.value != other.value
#     #     else:
#     #         return True
#     #
#     # def __gt__(self, other):
#     #     if other is None:
#     #         raise TypeError("'>' not supported between instances of 'QuarterDuration' and 'NoneType'")
#     #     if not isinstance(other, QuarterDuration):
#     #         other = self.__class__(other)
#     #     return self.value > other.value
#     #
#     # def __ge__(self, other):
#     #     if other is None:
#     #         raise TypeError("'>=' not supported between instances of 'QuarterDuration' and 'NoneType'")
#     #     if not isinstance(other, QuarterDuration):
#     #         other = self.__class__(other)
#     #     return self.value >= other.value
#     #
#     # def __lt__(self, other):
#     #     if other is None:
#     #         raise TypeError("'<' not supported between instances of 'QuarterDuration' and 'NoneType'")
#     #     if not isinstance(other, QuarterDuration):
#     #         other = self.__class__(other)
#     #     return self.value < other.value
#     #
#     # def __le__(self, other):
#     #     if other is None:
#     #         raise TypeError("'<=' not supported between instances of 'QuarterDuration' and 'NoneType'")
#     #     if not isinstance(other, QuarterDuration):
#     #         other = self.__class__(other)
#     #     return self.value <= other.value
#     #
#     # def __add__(self, other):
#     #     if other is None:
#     #         raise TypeError("unsupported operand type(s) for +: 'QuarterDuration' and 'NoneType'")
#     #     if not isinstance(other, QuarterDuration):
#     #         other = self.__class__(other)
#     #     return self.__class__(self.value + other.value)
#     #
#     # def __mul__(self, other):
#     #     if other is None:
#     #         raise TypeError("unsupported operand type(s) for *: 'QuarterDuration' and 'NoneType'")
#     #     if not isinstance(other, QuarterDuration):
#     #         other = self.__class__(other)
#     #     return self.__class__(self.value * other.value)
#     #
#     # def __truediv__(self, other):
#     #     if other is None:
#     #         raise TypeError("unsupported operand type(s) for /: 'QuarterDuration' and 'NoneType'")
#     #     other = self.__class__(other)
#     #     return self.__class__(self.value / other.value)
#     #
#     # def __floordiv__(self, other):
#     #     if other is None:
#     #         raise TypeError("unsupported operand type(s) for //: 'QuarterDuration' and 'NoneType'")
#     #     other = self.__class__(other)
#     #     return self.__class__(self.value // other.value)
#     #
#     # def __mod__(self, other):
#     #     if other is None:
#     #         raise TypeError("unsupported operand type(s) for %: 'QuarterDuration' and 'NoneType'")
#     #     other = self.__class__(other)
#     #     return self.__class__(self.value % other.value)
#     #
#     # def __sub__(self, other):
#     #     if other is None:
#     #         raise TypeError("unsupported operand type(s) for -: 'QuarterDuration' and 'NoneType'")
#     #     other = self.__class__(other)
#     #     return self.__class__(self.value - other.value)
#     #
#     # def __pow__(self, power, modulo=None):
#     #     return self.__class__(self.value.__pow__(power, modulo))
#     #
#     # def __float__(self):
#     #     return float(self.value)
#     #
#     # def __radd__(self, other):
#     #     return self + other

class QuarterDurationMixin:
    def __init__(self, quarter_duration=None):
        self._quarter_duration = None
        self.quarter_duration = quarter_duration

    @property
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, val):
        if val is not None:
            self._set_quarter_duration(val)
        else:
            self._quarter_duration = None

    def _set_quarter_duration(self, val):
        _check_quarter_duration(val)
        if isinstance(val, Fraction):
            self._quarter_duration = val
        else:
            self._quarter_duration = Fraction(val).limit_denominator(1000)
