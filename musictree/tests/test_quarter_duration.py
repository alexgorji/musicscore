from fractions import Fraction
from unittest import TestCase

from musictree.beat import Beat
from musictree.quarterduration import get_beatwise_sections, QuarterDuration


class TestQuarterDuration(TestCase):
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

    def test_add_etc(self):
        assert QuarterDuration(3, 4) + 0.25 == 1
        assert QuarterDuration(1, 6) + 1 / 6 == 1 / 3
        assert QuarterDuration(1, 6) + QuarterDuration(1, 6) == QuarterDuration(1, 3)
        assert QuarterDuration(1, 3) == 1 / 3
        assert QuarterDuration(1, 6) + QuarterDuration(1, 6) == 1/3
        assert QuarterDuration(1, 6) * 2 == 1 / 3
        assert 2 * QuarterDuration(1, 6) == 1 / 3

    def test_split_quarter_duration(self):
        """
        Test if get_beatwise_sections can split quarter duration to writable sections.
        """
        assert get_beatwise_sections(4, beats=[Beat(1), Beat(1), Beat(1), Beat(1)]) == [None, [4], None]
        assert get_beatwise_sections(3.5, beats=[Beat(1), Beat(1), Beat(1), Beat(1)]) == [None, [3, 0.5], None]
        assert get_beatwise_sections(3.5, offset=0.5, beats=[Beat(1), Beat(1), Beat(1), Beat(1)]) == [0.5, [3], None]
        assert get_beatwise_sections(4, offset=0.5, beats=[Beat(1), Beat(1), Beat(1), Beat(1)]) == [0.5, [3], 0.5]
        # or?
        # assert QuarterDuration(4).get_beatwise_sections(offset=0.5, beat_quarter_durations=[Beat(1), Beat(1), Beat(1), Beat(1)]) == [1.5, [2], 0.5]
        assert get_beatwise_sections(4, offset=0.25, beats=[Beat(1), Beat(1), Beat(1)]) == [0.75, [2], 1.25]
        assert get_beatwise_sections(4, offset=0.15, beats=[Beat(0.5), Beat(1.5), Beat(1)]) == [0.35, [1.5, 1], 1.15]
        assert get_beatwise_sections(4, offset=0.5, beats=[Beat(1), Beat(1.5), Beat(1.5), Beat(0.5)]) == [0.5, [3, 0.5], None]
        assert get_beatwise_sections(3, offset=0.5, beats=[Beat(1), Beat(1), Beat(0.5), Beat(0.5)]) == [0.5, [2], 0.5]
