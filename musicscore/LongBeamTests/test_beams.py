from fractions import Fraction
from unittest import TestCase, skip
from unittest.mock import Mock

from musicscore import Chord, Beat, QuarterDuration, Part, beam_chord_group
from musicscore.chord import _group_chords
from musicscore.config import NUMBEROFBEAMS
from musicscore.tests.util_subdivisions import generate_all_subdivision_patterns


class TestBeams32th(TestCase):

    def test_number_of_beams(self):
        p = Part('p1')
        p.add_measure([1, 4])
        subdivision = 8
        rhythmic_patterns = generate_all_subdivision_patterns(subdivision, True)
        for pattern in rhythmic_patterns:
            [p.add_chord(Chord(60, QuarterDuration(x, subdivision))) for x in pattern]
        p.finalize()
        for beat in p.get_beats():
            for chord in beat.get_chords():
                assert chord.test_number_of_beams()
    def test_break_16th_and_32nd_in_the_middle(self):
        p = Part('p1')
        p.add_measure([1, 4])
        subdivision = 8
        rhythmic_patterns = generate_all_subdivision_patterns(subdivision, True)
        for pattern in rhythmic_patterns:
            [p.add_chord(Chord(60, QuarterDuration(x, subdivision))) for x in pattern]
        p.finalize()
        for beat in p.get_beats():
            beat_chords = beat.get_chords()
            print([ch.quarter_duration for ch in beat_chords])
            for ch in beat_chords:
                print(ch.beams, ch.type)
                assert max(ch.beams.keys()) == NUMBEROFBEAMS[ch.type]
            for i in range(1, len(beat_chords)):
                current_chord = beat_chords[i]
                previous_chord = beat_chords[i - 1]
                if current_chord.offset == 1 / 2:
                    print([ch.beams for ch in beat_chords])
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

    def test_group_nontuplets(self):
        p = Part('p1')
        p.add_measure([1, 4])
        subdivision = 9
        rhythmic_patterns = generate_all_subdivision_patterns(subdivision, True)
        for pattern in rhythmic_patterns:
            chords = [Chord(60, QuarterDuration(x, subdivision)) for x in pattern]
            beat = Beat()
            beat._parent = Mock()
            [beat._add_chord(ch) for ch in chords]
            beat._split_not_writable_chords()
            beat._update_chord_types()
            beat_chords = beat.get_chords()
            print([ch.quarter_duration for ch in beat_chords])
            chord_groups = _group_chords(beat_chords, [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)])
            if not chord_groups:
                print(None)
            else:
                for group in chord_groups:
                    print([ch.quarter_duration for ch in group])
                    beam_chord_group(group)
                    print([ch.beams for ch in group])
