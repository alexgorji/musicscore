from unittest import TestCase

from quicktions import Fraction

from musictree.quarterduration import QuarterDuration


class TestQuarterDuration(TestCase):
    def test_qd_init(self):
        qd = QuarterDuration()
        assert qd == 0
        qd = QuarterDuration(1.5)
        assert qd == 3 / 2
        qd = QuarterDuration(Fraction(4, 3))
        assert qd == 4 / 3
        with self.assertRaises(TypeError):
            QuarterDuration(3, 2, 1)
        qd = QuarterDuration(0)
        qd.value = 1
        assert qd == 1
