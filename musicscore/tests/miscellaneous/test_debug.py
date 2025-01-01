from fractions import Fraction
from pathlib import Path
from musicscore.chord import Chord
from musicscore.score import Score
from musicscore.tests.util import XMLTestCase

path = Path(__file__)


class DebuggingTests(XMLTestCase):
    def setUp(self):
        self.score = Score()
        return super().setUp()

    def test_septuplets_with_gracenote(self):
        durations = [
            Fraction(0, 1),
            Fraction(3, 7),
            Fraction(1, 7),
            Fraction(2, 7),
            Fraction(1, 7),
        ]
        part = self.score.add_part("part-1")
        part.add_measure(time=(1, 4))
        for duration in durations:
            part.add_chord(Chord(60, duration))

        with self.file_path(path, "septuplets_with_gracenote") as xml_path:
            self.score.export_xml(xml_path)

    def test_grouping_problems(self):
        durations = [
            Fraction(19, 675),
            Fraction(49, 646),
            Fraction(30, 791),
            Fraction(15, 791),
            Fraction(45, 791),
            Fraction(16, 375),
            Fraction(13, 914),
            Fraction(45, 791),
            Fraction(16, 225),
            Fraction(19, 668),
            Fraction(32, 675),
            Fraction(16, 135),
            Fraction(16, 675),
            Fraction(16, 225),
            Fraction(64, 675),
            Fraction(9, 949),
            Fraction(15, 791),
            Fraction(19, 668),
            Fraction(30, 791),
            Fraction(32, 675),
            Fraction(15, 791),
            Fraction(13, 914),
            Fraction(16, 675),
            Fraction(9, 949),
            Fraction(1, 211),
        ]
        # print(sum(durations).limit_denominator(1000))
        self.score.get_quantized = True
        part = self.score.add_part("part-1")
        for duration in durations:
            part.add_chord(Chord(60, duration))
        # print([ch.quarter_duration for ch in part.get_chords()])
        with self.file_path(path, "grouping_problems") as xml_path:
            self.score.export_xml(xml_path)

    def test_update_accidentals_with_rest(self):
        score = Score()
        part = score.add_part("p1")
        qds = [
            1 / 5,
            4 / 15,
            1 / 3,
            8 / 21,
            32 / 105,
            16 / 105,
            8 / 35,
            4 / 3,
            16 / 15,
            64 / 147,
            256 / 735,
            128 / 735,
            64 / 245,
            8 / 35,
            32 / 105,
            8 / 21,
            32 / 21,
            64 / 105,
            4 / 9,
            4 / 15,
            16 / 45,
            16 / 45,
            64 / 315,
            32 / 105,
            128 / 315,
            32 / 63,
            16 / 9,
            32 / 45,
            32 / 27,
            128 / 945,
            64 / 189,
            64 / 315,
            256 / 945,
        ]
        for qd in qds:
            chord = Chord(61, quarter_duration=qd)
            if qd in [16 / 105, 128 / 735, 64 / 105, 64 / 315, 32 / 45, 128 / 945]:
                chord.midis = 0
            part.add_chord(chord)
        part.get_quantized = True
        part.finalize()

    def test_tied_unwritables(self):
        score = Score()
        part = score.add_part("p1")
        part.add_measure(time=(2, 4))
        qd_patterns = [[2 / 7, 12 / 7], [1 / 8, 15 / 8], [1 / 6, 11 / 6]]
        for pattern in qd_patterns:
            for qd in pattern:
                part.add_chord(Chord(61, quarter_duration=qd))

        with self.file_path(path, "tied_unwritables") as xml_path:
            score.export_xml(xml_path)
