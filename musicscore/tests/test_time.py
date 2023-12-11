from fractions import Fraction
from unittest import TestCase

from musicscore import Part, Chord
from musicscore.tests.util import IdTestCase
from musicscore.time import Time, flatten_times, _convert_signatures_to_ints


class TestTime(TestCase):

    def test_convert_signatures_to_ints(self):
        assert _convert_signatures_to_ints([1, 2]) == [1, 2]
        assert _convert_signatures_to_ints([1, 2, 3, 4]) == [1, 2, 3, 4]
        assert _convert_signatures_to_ints(["1", "2", "3", "4"]) == [1, 2, 3, 4]
        assert _convert_signatures_to_ints(["2+3+5", 8, 3, 4]) == [2, 8, 3, 8, 5, 8, 3, 4]
        assert _convert_signatures_to_ints(["2+3", "8"]) == [2, 8, 3, 8]

    def test_time_init(self):
        t = Time()
        expected = """<time>
  <beats>4</beats>
  <beat-type>4</beat-type>
</time>
"""
        assert t.to_string() == expected
        t.xml_beats = '3'
        expected = """<time>
  <beats>3</beats>
  <beat-type>4</beat-type>
</time>
"""
        assert t.to_string() == expected
        t = Time(6, 8, 3, 4)
        expected = """<time>
  <beats>6</beats>
  <beat-type>8</beat-type>
  <beats>3</beats>
  <beat-type>4</beat-type>
</time>
"""
        assert t.to_string() == expected

    def test_change_fractions(self):
        t = Time()
        t.signatures = [7, 8, 3, 4]
        expected = """<time>
  <beats>7</beats>
  <beat-type>8</beat-type>
  <beats>3</beats>
  <beat-type>4</beat-type>
</time>
"""
        assert t.to_string() == expected
        t.signatures = None
        expected = """<time>
  <beats>4</beats>
  <beat-type>4</beat-type>
</time>
"""
        assert t.to_string() == expected
        t.signatures = [2, 4]
        expected = """<time>
  <beats>2</beats>
  <beat-type>4</beat-type>
</time>
"""
        assert t.to_string() == expected

        t.signatures = ['3+2', 8]
        expected = """<time>
  <beats>3+2</beats>
  <beat-type>8</beat-type>
</time>
"""
        assert t.to_string() == expected

    def test_time_actual_signatures(self):
        t = Time()
        assert t.actual_signatures == [1, 4, 1, 4, 1, 4, 1, 4]
        t.signatures = [3, 4]
        assert t.actual_signatures == [1, 4, 1, 4, 1, 4]
        t.actual_signatures = [3, 4]
        assert t.actual_signatures == [3, 4]

        t.signatures = [2, 8]
        assert t.signatures == [2, 8]
        assert t.actual_signatures == [2, 8]

        t.signatures = [3, 8]
        assert t.actual_signatures == [3, 8]

        t.signatures = [4, 8]
        assert t.actual_signatures == [2, 8, 2, 8]

        t.signatures = [5, 8]
        assert t.actual_signatures == [3, 8, 2, 8]

        t.signatures = [6, 8]
        assert t.actual_signatures == [3, 8, 3, 8]

        t.signatures = [7, 8]
        assert t.actual_signatures == [4, 8, 3, 8]

        t.signatures = [8, 8]
        assert t.actual_signatures == 8 * [1, 8]

        t.signatures = [9, 8]
        assert t.actual_signatures == 3 * [3, 8]

        t.signatures = [10, 8]
        assert t.actual_signatures == 10 * [1, 8]

        t.signatures = [11, 8]
        assert t.actual_signatures == 11 * [1, 8]

        t.signatures = [12, 8]
        assert t.actual_signatures == 4 * [3, 8]

        t.signatures = [15, 8]
        assert t.actual_signatures == 5 * [3, 8]

        t.signatures = [18, 8]
        assert t.actual_signatures == 6 * [3, 8]

        t.actual_signatures = ['3+2+5', '8']
        assert t.actual_signatures == [3, 8, 2, 8, 5, 8]

        t.signatures = [3, 4]
        assert t.actual_signatures == [1, 4, 1, 4, 1, 4]
        t.actual_signatures = [3, 4]
        assert t.actual_signatures == [3, 4]
        t.signatures = [3, 2]
        assert t.actual_signatures == [1, 2, 1, 2, 1, 2]

    def test_get_beats_quarter_durations(self):
        t = Time()
        assert t.get_beats_quarter_durations() == [Fraction(1)] * 4
        t.signatures = [3, 4]
        assert t.get_beats_quarter_durations() == [Fraction(1)] * 3
        t.signatures = [6, 8]
        assert t.get_beats_quarter_durations() == [Fraction(3, 2)] * 2
        t.actual_signatures = [1, 8] * 6
        assert t.get_beats_quarter_durations() == [Fraction(1, 2)] * 6
        t.signatures = [3, 4, 2, 8]
        # t._reset_actual_signatures()
        assert t.get_beats_quarter_durations() == [Fraction(1)] * 3 + [Fraction(1, 1)]

    def test_flatten_times(self):
        times = [2 * Time(3, 8), (3, 4), 3 * [(1, 8)], Time(1, 8, 3, 4), Time(3, 4)]
        flattened_times = flatten_times(times)
        assert [t.signatures for t in flattened_times] == [(3, 8), (3, 8), (3, 4), (1, 8), (1, 8), (1, 8), (1, 8, 3, 4),
                                                           (3, 4)]

    def test_copy(self):
        t = Time(3, 4, show=False)
        t.actual_signatures = (1, 8, 2, 4)
        copied = t.__copy__()
        assert copied != t
        assert copied.signatures == t.signatures
        assert copied.actual_signatures == t.actual_signatures
        assert copied.show == t.show


class TestActualTime(IdTestCase):

    # def test_actual_time_cannot_change_measure_quarter_duration(self):
    #     t = Time(3, 4)
    #     t.actual_signatures = [4, 4]
    def test_add_measure_sets_actual_time_of_previous(self):
        p = Part('p1')
        t = Time(4, 4)
        t.actual_signatures = [2, 2]
        m1 = p.add_measure(t)
        m2 = p.add_measure()
        assert m1.time.actual_signatures == m2.time.actual_signatures
        assert [b.quarter_duration for b in m1.get_beats()] == [b.quarter_duration for b in m2.get_beats()]

    def test_actual_time_and_beat_quarter_duration(self):
        t = Time(3, 2)
        assert t.get_beats_quarter_durations() == [2, 2, 2]
        t.actual_signatures = [3, 2]
        assert t.get_beats_quarter_durations() == [6]

        t = Time(2, 2)
        assert t.get_beats_quarter_durations() == [2, 2]
        t.actual_signatures = [2, 2]
        assert t.get_beats_quarter_durations() == [4]

    def test_actual_time_and_beat_get_actual_notes(self):
        part = Part('p1')
        t = Time(2, 2)
        measure = part.add_measure(t)
        quarter_durations = [4 / 3, 2 / 3, 2 / 5, 2 / 5, 2 / 5, 2 / 5, 2 / 5]
        for qd in quarter_durations:
            part.add_chord(Chord(60, qd))
        assert measure.get_beat(staff_number=1, voice_number=1, beat_number=1).quarter_duration == 2
        assert len(measure.get_beat(staff_number=1, voice_number=1, beat_number=1).get_children()) == 2
        assert len(measure.get_beat(staff_number=1, voice_number=1, beat_number=2).get_children()) == 5

        part = Part('p2')
        t = Time(2, 2)
        t.actual_signatures = [1, 2, 1, 2]
        measure = part.add_measure(t)
        quarter_durations = [4 / 3, 2 / 3, 2 / 5, 2 / 5, 2 / 5, 2 / 5, 2 / 5]
        for qd in quarter_durations:
            part.add_chord(Chord(60, qd))
        assert measure.get_beat(staff_number=1, voice_number=1, beat_number=1).quarter_duration == 2
        assert len(measure.get_beat(staff_number=1, voice_number=1, beat_number=1).get_children()) == 2
        assert len(measure.get_beat(staff_number=1, voice_number=1, beat_number=2).get_children()) == 5
