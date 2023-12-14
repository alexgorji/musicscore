from unittest import TestCase

from musicscore import Chord


class TestTypes(TestCase):
    def test_types(self):
        ch = Chord(60, 1)
        assert ch.quarter_duration.get_type() == 'quarter'
        assert ch.quarter_duration.get_number_of_dots() == 0
        assert ch.quarter_duration.get_tuplet_ratio() is None

        ch = Chord(60, 1 / 2)
        assert ch.quarter_duration.get_type() == 'eighth'
        assert ch.quarter_duration.get_number_of_dots() == 0
        assert ch.quarter_duration.get_tuplet_ratio() is None

        ch = Chord(60, 1 / 2)
        for sd in [6, 12]:
            ch.quarter_duration.beat_subdivision = sd
            assert ch.quarter_duration.get_type() == 'eighth'
            assert ch.quarter_duration.get_number_of_dots() == 1
            if sd == 6:
                assert ch.quarter_duration.get_tuplet_ratio() == (6, 4)
            else:
                assert ch.quarter_duration.get_tuplet_ratio() == (12, 8)

        ch = Chord(60, 1 / 3)
        assert ch.quarter_duration.get_type() == 'eighth'
        assert ch.quarter_duration.get_number_of_dots() == 0
        assert ch.quarter_duration.get_tuplet_ratio() == (3, 2)

        ch = Chord(60, 2 / 3)
        ch.quarter_duration.beat_subdivision = 9
        assert ch.quarter_duration.get_type() == 'eighth'
        assert ch.quarter_duration.get_number_of_dots() == 1
        assert ch.quarter_duration.get_tuplet_ratio() == (9, 8)
