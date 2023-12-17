from unittest import TestCase, skip

from musicscore import Chord, QuarterDuration, Part
from musicscore.tests.util import IdTestCase
from musicscore.tests.util_subdivisions import generate_all_subdivision_patterns


class TestBeamsAndPrintedDurations(IdTestCase):
    def test_quarter_32th(self):
        p = Part('p1')
        p.add_measure([1, 4])
        subdivision = 8
        rhythmic_patterns = generate_all_subdivision_patterns(subdivision, True)
        for pattern in rhythmic_patterns:
            [p.add_chord(Chord(60, QuarterDuration(x, subdivision))) for x in pattern]
        p.finalize()
        for beat in p.get_beats():
            beat_chords = beat.get_chords()
            for i in range(1, len(beat_chords)):
                current_chord = beat_chords[i]
                previous_chord = beat_chords[i - 1]
                current_chord.check_printed_duration()
                current_chord.check_number_of_beams()
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

    def test_quarter_nonuplets(self):
        p = Part('p1')
        p.add_measure([1, 4])
        subdivision = 9
        rhythmic_patterns = generate_all_subdivision_patterns(subdivision, True)
        for pattern in rhythmic_patterns:
            [p.add_chord(Chord(60, QuarterDuration(x, subdivision))) for x in pattern]
        p.finalize()
        for beat in p.get_beats():
            beat_chords = beat.get_chords()
            for chord in beat_chords:
                chord.check_printed_duration()
                chord.check_number_of_beams()
