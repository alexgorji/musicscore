from fractions import Fraction
from pathlib import Path
from musicscore.chord import Chord
from musicscore.score import Score
from musicscore.tests.util import XMLTestCase
from musicscore.tests.util_subdivisions import generate_all_subdivision_patterns

path = Path(__file__)


def create_tied_patterns():
    rhythmic_patterns = iter(generate_all_subdivision_patterns(6, False))
    chord_patterns = []
    while True:
        pattern_chord_list = [Chord(60, 1)]
        try:
            next_pattern = next(rhythmic_patterns)
        except StopIteration:
            break
        for qd in next_pattern:
            chord = Chord(60, Fraction(qd / 6))
            chord.add_lyric(qd)
            pattern_chord_list.append(chord)

        pattern_chord_list.append(Chord(60, 1))

        pattern_chord_list[0].add_tie("start")
        pattern_chord_list[1].add_tie("stop")
        pattern_chord_list[-2].add_tie("start")
        pattern_chord_list[-1].add_tie("stop")

        chord_patterns.append(pattern_chord_list)
    return chord_patterns


class TiedSextupletsTestCase(XMLTestCase):
    def test_generate_all_subdivision_patterns(self):
        self.assertEqual(
            generate_all_subdivision_patterns(6, False),
            [
                (5, 1),
                (1, 5),
                (4, 2),
                (2, 4),
                (4, 1, 1),
                (1, 4, 1),
                (1, 1, 4),
                (3, 3),
                (3, 2, 1),
                (3, 1, 2),
                (2, 3, 1),
                (2, 1, 3),
                (1, 3, 2),
                (1, 2, 3),
                (3, 1, 1, 1),
                (1, 3, 1, 1),
                (1, 1, 3, 1),
                (1, 1, 1, 3),
                (2, 2, 2),
                (2, 2, 1, 1),
                (2, 1, 2, 1),
                (2, 1, 1, 2),
                (1, 2, 2, 1),
                (1, 2, 1, 2),
                (1, 1, 2, 2),
                (2, 1, 1, 1, 1),
                (1, 2, 1, 1, 1),
                (1, 1, 2, 1, 1),
                (1, 1, 1, 2, 1),
                (1, 1, 1, 1, 2),
                (1, 1, 1, 1, 1, 1),
            ],
        )

    def test_patterns(self):
        patterns = create_tied_patterns()
        self.assertEqual(
            [[chord.quarter_duration for chord in pattern] for pattern in patterns],
            [
                [1 / 1, 5 / 6, 1 / 6, 1 / 1],
                [1 / 1, 1 / 6, 5 / 6, 1 / 1],
                [1 / 1, 2 / 3, 1 / 3, 1 / 1],
                [1 / 1, 1 / 3, 2 / 3, 1 / 1],
                [1 / 1, 2 / 3, 1 / 6, 1 / 6, 1 / 1],
                [1 / 1, 1 / 6, 2 / 3, 1 / 6, 1 / 1],
                [1 / 1, 1 / 6, 1 / 6, 2 / 3, 1 / 1],
                [1 / 1, 1 / 2, 1 / 2, 1 / 1],
                [1 / 1, 1 / 2, 1 / 3, 1 / 6, 1 / 1],
                [1 / 1, 1 / 2, 1 / 6, 1 / 3, 1 / 1],
                [1 / 1, 1 / 3, 1 / 2, 1 / 6, 1 / 1],
                [1 / 1, 1 / 3, 1 / 6, 1 / 2, 1 / 1],
                [1 / 1, 1 / 6, 1 / 2, 1 / 3, 1 / 1],
                [1 / 1, 1 / 6, 1 / 3, 1 / 2, 1 / 1],
                [1 / 1, 1 / 2, 1 / 6, 1 / 6, 1 / 6, 1 / 1],
                [1 / 1, 1 / 6, 1 / 2, 1 / 6, 1 / 6, 1 / 1],
                [1 / 1, 1 / 6, 1 / 6, 1 / 2, 1 / 6, 1 / 1],
                [1 / 1, 1 / 6, 1 / 6, 1 / 6, 1 / 2, 1 / 1],
                [1 / 1, 1 / 3, 1 / 3, 1 / 3, 1 / 1],
                [1 / 1, 1 / 3, 1 / 3, 1 / 6, 1 / 6, 1 / 1],
                [1 / 1, 1 / 3, 1 / 6, 1 / 3, 1 / 6, 1 / 1],
                [1 / 1, 1 / 3, 1 / 6, 1 / 6, 1 / 3, 1 / 1],
                [1 / 1, 1 / 6, 1 / 3, 1 / 3, 1 / 6, 1 / 1],
                [1 / 1, 1 / 6, 1 / 3, 1 / 6, 1 / 3, 1 / 1],
                [1 / 1, 1 / 6, 1 / 6, 1 / 3, 1 / 3, 1 / 1],
                [1 / 1, 1 / 3, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 1],
                [1 / 1, 1 / 6, 1 / 3, 1 / 6, 1 / 6, 1 / 6, 1 / 1],
                [1 / 1, 1 / 6, 1 / 6, 1 / 3, 1 / 6, 1 / 6, 1 / 1],
                [1 / 1, 1 / 6, 1 / 6, 1 / 6, 1 / 3, 1 / 6, 1 / 1],
                [1 / 1, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 3, 1 / 1],
                [1 / 1, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 1],
            ],
        )
        for pattern in patterns:
            self.assertTrue(pattern[0].is_tied_to_next)
            self.assertTrue(pattern[-1].is_tied_to_previous)

    def test_all_tied_sextuplets(self):
        s = Score()
        p = s.add_part("p1")
        p.add_measure(time=(3, 4))
        for pattern in create_tied_patterns():
            for chord in pattern:
                p.add_chord(chord)
        with self.file_path(path, "all") as xml_path:
            s.export_xml(xml_path)
