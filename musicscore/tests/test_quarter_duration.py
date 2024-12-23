from fractions import Fraction
from math import ceil, floor
from unittest import TestCase

from musicscore.beat import Beat
from musicscore.exceptions import QuarterDurationIsNotWritable
from musicscore.quarterduration import QuarterDuration, _check_quarter_duration_value


class TestQuarterDuration(TestCase):
    def test_quarter_duration_init(self):
        qd = QuarterDuration(3, 2)
        assert (qd.numerator, qd.denominator) == (3, 2)
        assert qd == 1.5
        assert qd == QuarterDuration(3, 2)
        qd = QuarterDuration(1.2)
        assert qd.as_integer_ratio() == (6, 5)
        assert qd == QuarterDuration(6, 5)
        assert qd == 1.2

    def test_quarter_duration_operands(self):
        qd = QuarterDuration(2)
        assert qd == 2
        assert qd <= 2
        assert qd >= 2
        assert not qd == 3
        assert qd < 3
        assert qd != 3
        assert qd > 1
        qd = QuarterDuration(1, 6)
        assert qd == Fraction(1, 6)
        assert qd == 1 / 6
        assert qd <= 1 / 6
        assert qd >= 1 / 6
        assert QuarterDuration(1, 3) == 1 / 3
        assert QuarterDuration(6 / 5) == 6 / 5
        assert QuarterDuration(6, 5) == 1.2
        assert QuarterDuration(1.2) == QuarterDuration(6, 5)
        assert QuarterDuration(Fraction(6 / 5)) == 6 / 5
        assert [
            QuarterDuration(7, 20),
            [QuarterDuration(3, 2), QuarterDuration(1)],
            QuarterDuration(23, 20),
        ] == [0.35, [1.5, 1], 1.15]
        assert [
            QuarterDuration(0.35),
            [QuarterDuration(1.5), QuarterDuration(1)],
            QuarterDuration(1.15),
        ] == [0.35, [1.5, 1], 1.15]

    def test_add_etc(self):
        assert isinstance(1 / 6 + QuarterDuration(1, 6), QuarterDuration)
        assert QuarterDuration(3, 4) + 0.25 == 1
        assert 1 / 6 + QuarterDuration(1, 6) == QuarterDuration(1, 3)
        assert QuarterDuration(1, 6) + 1 / 6 == QuarterDuration(1, 3)

        assert 1 / 6 + QuarterDuration(1, 6) == 1 / 3
        assert QuarterDuration(1, 6) + 1 / 6 == 1 / 3
        assert QuarterDuration(1, 6) + QuarterDuration(1, 6) == QuarterDuration(1, 3)
        assert QuarterDuration(1, 6) + QuarterDuration(1, 6) == 1 / 3
        assert QuarterDuration(1, 6) * 2 == 1 / 3
        assert 2 * QuarterDuration(1, 6) == 1 / 3

    def test_rtruediv(self):
        assert 2 / (1 / 2) == 4
        assert 2 / QuarterDuration(1, 2) == 4

    def test_split_quarter_duration(self):
        """
        Test if _get_beatwise_sections can split quarter duration to writable sections.
        """
        assert QuarterDuration(4)._get_beatwise_sections(
            beats=[Beat(1), Beat(1), Beat(1), Beat(1)]
        ) == [[4], None]
        assert QuarterDuration(3.5)._get_beatwise_sections(
            beats=[Beat(1), Beat(1), Beat(1), Beat(1)]
        ) == [[3, 0.5], None]
        assert QuarterDuration(3.5)._get_beatwise_sections(
            offset=0.5, beats=[Beat(1), Beat(1), Beat(1), Beat(1)]
        ) == [[0.5, 3], None]
        assert QuarterDuration(4)._get_beatwise_sections(
            offset=0.5, beats=[Beat(1), Beat(1), Beat(1), Beat(1)]
        ) == [[0.5, 3], 0.5]
        assert QuarterDuration(4)._get_beatwise_sections(
            offset=0.25, beats=[Beat(1), Beat(1), Beat(1)]
        ) == [[0.75, 2], 1.25]
        assert QuarterDuration(4)._get_beatwise_sections(
            offset=0.5, beats=[Beat(1), Beat(1.5), Beat(1.5), Beat(0.5)]
        ) == [[0.5, 3, 0.5], None]
        assert QuarterDuration(3)._get_beatwise_sections(
            offset=0.5, beats=[Beat(1), Beat(1), Beat(0.5), Beat(0.5)]
        ) == [[0.5, 2], 0.5]
        assert QuarterDuration(4)._get_beatwise_sections(
            offset=0.15, beats=[Beat(0.5), Beat(1.5), Beat(1)]
        ) == [[0.35, 1.5, 1], 1.15]

    def test_copy_quarter_duration(self):
        qd = QuarterDuration(3, 4)
        copied = qd.__copy__()
        assert id(qd.value) != id(copied.value)
        assert qd.value == copied.value

    def test_check_quarter_duration(self):
        assert _check_quarter_duration_value(1)
        assert _check_quarter_duration_value(1.2)
        assert _check_quarter_duration_value(1 / 3)
        assert _check_quarter_duration_value(Fraction(1, 3))
        assert _check_quarter_duration_value(QuarterDuration(1, 3))

    def test_get_type_and_dots(self):
        assert QuarterDuration(1)._get_type_and_dots() == ("quarter", 0)
        assert QuarterDuration(1.5)._get_type_and_dots() == ("quarter", 1)
        assert QuarterDuration(1.75)._get_type_and_dots() == ("quarter", 2)

        assert QuarterDuration(0.75)._get_type_and_dots() == ("eighth", 1)
        assert QuarterDuration(2 + 2 / 2 + 2 / 4)._get_type_and_dots() == ("half", 2)

        assert QuarterDuration(1 / 3)._get_type_and_dots() == ("eighth", 0)
        assert QuarterDuration(2 / 3)._get_type_and_dots() == ("quarter", 0)

    def test_get_type(self):
        assert QuarterDuration(1).get_type() == "quarter"
        assert QuarterDuration(1.5).get_type() == "quarter"
        assert QuarterDuration(1.75).get_type() == "quarter"

        assert QuarterDuration(0.75).get_type() == "eighth"
        assert QuarterDuration(2 + 2 / 2 + 2 / 4).get_type() == "half"

        assert QuarterDuration(1 / 3).get_type() == "eighth"
        assert QuarterDuration(2 / 3).get_type() == "quarter"

    def test_get_dots(self):
        assert QuarterDuration(1).get_number_of_dots() == 0
        assert QuarterDuration(1.5).get_number_of_dots() == 1
        assert QuarterDuration(1.75).get_number_of_dots() == 2

        assert QuarterDuration(0.75).get_number_of_dots() == 1
        assert QuarterDuration(2 + 2 / 2 + 2 / 4).get_number_of_dots() == 2

    def test_is_not_writable(self):
        for value in [0.23, 5 / 2, 9 / 2, 5 / 4, 9 / 5]:
            with self.assertRaises(QuarterDurationIsNotWritable):
                QuarterDuration(value)._get_type_and_dots()
            with self.assertRaises(QuarterDurationIsNotWritable):
                QuarterDuration(value).get_type()
            with self.assertRaises(QuarterDurationIsNotWritable):
                QuarterDuration(value).get_number_of_dots()

    def test_set_value(self):
        qt = QuarterDuration(2)
        qt.value = 3
        self.assertEqual(qt.value, 3)


class TestMagics(TestCase):
    cl = QuarterDuration

    def setUp(self):
        self.main = self.cl(70)
        self.equal = self.cl(70)
        self.equal_float = 70.0
        self.larger = self.cl(80)
        self.larger_float = 80.0
        self.smaller = self.cl(60)
        self.smaller_float = 60.0

    def test_abs(self):
        assert abs(self.cl(-70)) == 70

    def test_ceil(self):
        assert ceil(self.cl(70.2)) == 71

    def test_floor(self):
        assert floor(self.cl(70.2)) == 70

    def test_floor_division(self):
        a = self.cl(10)
        b = self.cl(4)
        c = self.cl(2)
        assert a // b == c
        assert a // 4 == c
        assert a // b == 2
        assert a // 4 == 2

    def test_gt(self):
        assert self.main > self.smaller
        assert self.main > self.smaller_float
        assert not self.main > self.equal
        assert not self.main > self.equal_float
        assert not self.main > self.larger
        assert not self.main > self.larger_float

    def test_ge(self):
        assert self.main >= self.smaller
        assert self.main >= self.smaller_float
        assert self.main >= self.equal
        assert self.main >= self.equal_float
        assert not self.main >= self.larger
        assert not self.main >= self.larger_float

    def test_le(self):
        assert not self.main <= self.smaller
        assert not self.main <= self.smaller_float
        assert self.main <= self.equal
        assert self.main <= self.equal_float
        assert self.main <= self.larger
        assert self.main <= self.larger_float

    def test_lt(self):
        assert not self.main < self.smaller
        assert not self.main < self.smaller_float
        assert not self.main < self.equal
        assert not self.main < self.equal_float
        assert self.main < self.larger
        assert self.main < self.larger_float

    def test_mod(self):
        a = self.cl(10)
        b = self.cl(3)
        c = self.cl(1)
        assert a % 3 == c
        assert a % 3 == 1
        assert a % b == c
        assert a % b == 1

    def test_mul(self):
        a = self.cl(10)
        b = self.cl(3)
        c = self.cl(30)
        assert a * b == 30
        assert a * b == c
        assert a * 3 == 30
        assert a * 3 == c

    def test_neg(self):
        a = self.cl(10)
        b = self.cl(-10)
        assert -a == b
        assert -a == -10
        assert -b == a
        assert -b == 10

    def test_pos(self):
        a = self.cl(10)
        assert +a == a

    def test_power(self):
        a = self.cl(10)
        b = self.cl(100)
        assert 10.0**2 == 100
        assert a**2 == 100
        assert a**2 == b

    def test_radd(self):
        a = self.cl(10)
        b = self.cl(100)
        assert a.__radd__(b) == b + a

    def test_rmod(self):
        a = self.cl(3)
        b = self.cl(10)
        assert a.__rmod__(b) == b % a

    def test_rmul(self):
        a = self.cl(3)
        b = self.cl(10)
        assert a.__rmul__(b) == b * a

    def test_eq(self):
        a = self.cl(10)
        b = self.cl(10)
        c = self.cl(11)
        assert a == b
        assert a == 10
        assert 10 == a
        assert a == 10.0
        assert a != 11
        assert a != c
        assert not a == c
        assert not a == 11
        assert not 11 == a
        d = self.cl(Fraction(10, 3))
        assert Fraction(10, 3) == Fraction(10, 3)
        assert Fraction(10, 3).__eq__(Fraction(10, 3))
        assert d.__eq__(Fraction(10, 3))
        assert d == Fraction(10, 3)
        assert a is not None
        assert a != None  # noqa

    def test_round(self):
        assert self.cl(70.7) == self.cl(70.7)
        assert round(self.cl(70.67), 1) == 70.7
        assert round(self.cl(70.67), 1) == self.cl(70.7)
        assert round(self.cl(70.67), 1) != self.cl(70.6)
        assert round(self.cl(70.67), 1) != 70.6

    def test_rtruediv(self):
        a = self.cl(3)
        b = self.cl(10)
        assert a.__rtruediv__(b) == Fraction(10, 3)

    def test_truediv(self):
        a = self.cl(10)
        b = self.cl(3)
        assert a / b == Fraction(10, 3)

    def test_trunc(self):
        a = self.cl(10.233)
        assert a.__trunc__() == 10

    def test_rfloordiv(self):
        a = self.cl(3)
        b = self.cl(10)
        assert a.__rfloordiv__(b) == b // a
