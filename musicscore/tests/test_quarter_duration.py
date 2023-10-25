from quicktions import Fraction
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
        assert [QuarterDuration(7, 20), [QuarterDuration(3, 2), QuarterDuration(1)], QuarterDuration(23, 20)] == [0.35,
                                                                                                                  [1.5,
                                                                                                                   1],
                                                                                                                  1.15]
        assert [QuarterDuration(0.35), [QuarterDuration(1.5), QuarterDuration(1)], QuarterDuration(1.15)] == [0.35,
                                                                                                              [1.5, 1],
                                                                                                              1.15]

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
        assert QuarterDuration(4)._get_beatwise_sections(beats=[Beat(1), Beat(1), Beat(1), Beat(1)]) == [[4], None]
        assert QuarterDuration(3.5)._get_beatwise_sections(beats=[Beat(1), Beat(1), Beat(1), Beat(1)]) == [[3, 0.5],
                                                                                                           None]
        assert QuarterDuration(3.5)._get_beatwise_sections(offset=0.5, beats=[Beat(1), Beat(1), Beat(1), Beat(1)]) == [
            [0.5, 3], None]
        assert QuarterDuration(4)._get_beatwise_sections(offset=0.5, beats=[Beat(1), Beat(1), Beat(1), Beat(1)]) == [
            [0.5, 3], 0.5]
        assert QuarterDuration(4)._get_beatwise_sections(offset=0.25, beats=[Beat(1), Beat(1), Beat(1)]) == [[0.75, 2],
                                                                                                             1.25]
        assert QuarterDuration(4)._get_beatwise_sections(offset=0.5,
                                                         beats=[Beat(1), Beat(1.5), Beat(1.5), Beat(0.5)]) == [
                   [0.5, 3, 0.5],
                   None]
        assert QuarterDuration(3)._get_beatwise_sections(offset=0.5, beats=[Beat(1), Beat(1), Beat(0.5), Beat(0.5)]) == [
            [0.5, 2], 0.5]
        assert QuarterDuration(4)._get_beatwise_sections(offset=0.15, beats=[Beat(0.5), Beat(1.5), Beat(1)]) == [
            [0.35, 1.5, 1], 1.15]

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
        assert QuarterDuration(1)._get_type_and_dots() == ('quarter', 0)
        assert QuarterDuration(1.5)._get_type_and_dots() == ('quarter', 1)
        assert QuarterDuration(1.75)._get_type_and_dots() == ('quarter', 2)

        assert QuarterDuration(0.75)._get_type_and_dots() == ('eighth', 1)
        assert QuarterDuration(2 + 2 / 2 + 2 / 4)._get_type_and_dots() == ('half', 2)

        assert QuarterDuration(1 / 3)._get_type_and_dots() == ('eighth', 0)
        assert QuarterDuration(2 / 3)._get_type_and_dots() == ('quarter', 0)

    def test_get_type(self):
        assert QuarterDuration(1).get_type() == 'quarter'
        assert QuarterDuration(1.5).get_type() == 'quarter'
        assert QuarterDuration(1.75).get_type() == 'quarter'

        assert QuarterDuration(0.75).get_type() == 'eighth'
        assert QuarterDuration(2 + 2 / 2 + 2 / 4).get_type() == 'half'

        assert QuarterDuration(1 / 3).get_type() == 'eighth'
        assert QuarterDuration(2 / 3).get_type() == 'quarter'

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
