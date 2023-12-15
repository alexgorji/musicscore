from unittest import TestCase, skip
from unittest.mock import Mock

from musicscore import Chord, Beat, QuarterDuration, Part
from musicscore.tests.util_subdivisions import generate_all_subdivision_patterns


class TestBeams32th(TestCase):
    def test_break_16th_and_32nd_in_the_middle(self):
        p = Part('p1')
        p.add_measure([1, 4])
        subdivision = 8
        rhythmic_patterns = generate_all_subdivision_patterns(8, True)
        for pattern in rhythmic_patterns:
            [p.add_chord(Chord(60, QuarterDuration(x, subdivision))) for x in pattern]
        p.finalize()
        for beat in p.get_beats():
            beat_chords = beat.get_chords()
            qds = [ch.quarter_duration for ch in beat_chords]
            if qds == [1 / 4, 1 / 4, 1 / 4, 1 / 8, 1 / 8]:
                continue
            for i in range(1, len(beat_chords)):
                current_chord = beat_chords[i]
                previous_chord = beat_chords[i - 1]
                if current_chord.offset == 1 / 2:
                    for key, value in current_chord.beams.items():
                        if key == 1:
                            assert value in ['end', 'continue']
                        else:
                            assert value != 'continue'
                    for key, value in previous_chord.beams.items():
                        if key == 1:
                            assert value in ['begin', 'continue']
                        else:
                            assert value != 'continue'
                    continue
