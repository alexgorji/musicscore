from unittest import TestCase

from musicscore import Chord


class TestTypes(TestCase):
    def test_types(self):
        ch = Chord(60, 1)
        assert ch.quarter_duration.get_type() == 'quarter'
        assert ch.quarter_duration.get_number_of_dots() == 0
        assert ch.quarter_duration.get_tuplet_ratio() is None

        ch = Chord(60, 1/2)
        assert ch.quarter_duration.get_type() == 'eighth'
        assert ch.quarter_duration.get_number_of_dots() == 0
        assert ch.quarter_duration.get_tuplet_ratio() is None

        ch = Chord(60, 1 / 3)
        assert ch.quarter_duration.get_type() == 'eighth'
        assert ch.quarter_duration.get_number_of_dots() == 0
        assert ch.quarter_duration.get_tuplet_ratio() == (3, 2)


