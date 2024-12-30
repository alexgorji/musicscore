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
        # durations = [
        #     Fraction(128, 675),
        #     Fraction(64, 135),
        #     Fraction(64, 675),
        #     Fraction(64, 225),
        #     Fraction(256, 675),
        #     Fraction(256, 675),
        #     Fraction(1024, 3375),
        #     Fraction(512, 3375),
        #     Fraction(256, 3375),
        #     Fraction(256, 1125),
        #     Fraction(128, 3375),
        #     Fraction(256, 3375),
        #     Fraction(128, 1125),
        #     Fraction(512, 3375),
        #     Fraction(128, 675),
        #     Fraction(256, 3375),
        #     Fraction(64, 1125),
        #     Fraction(64, 675),
        #     Fraction(128, 3375),
        #     Fraction(64, 3375),
        #     Fraction(64, 375),
        #     Fraction(64, 1125),
        #     Fraction(256, 1125),
        #     Fraction(64, 225),
        #     Fraction(128, 1125),
        #     Fraction(16, 375),
        #     Fraction(32, 375),
        #     Fraction(16, 125),
        #     Fraction(64, 375),
        #     Fraction(16, 75),
        #     Fraction(32, 1125),
        #     Fraction(16, 225),
        #     Fraction(16, 1125),
        #     Fraction(16, 375),
        #     Fraction(64, 1125),
        #     Fraction(256, 1125),
        #     Fraction(64, 375),
        #     Fraction(64, 225),
        #     Fraction(128, 1125),
        #     Fraction(64, 1125),
        #     Fraction(16, 75),
        #     Fraction(16, 225),
        #     Fraction(64, 225),
        #     Fraction(16, 45),
        #     Fraction(32, 225),
        #     Fraction(32, 225),
        #     Fraction(128, 1125),
        #     Fraction(64, 1125),
        #     Fraction(32, 1125),
        #     Fraction(32, 375),
        #     Fraction(128, 675),
        #     Fraction(32, 225),
        #     Fraction(32, 135),
        #     Fraction(64, 675),
        #     Fraction(32, 675),
        #     Fraction(16, 135),
        #     Fraction(32, 135),
        #     Fraction(16, 45),
        #     Fraction(64, 135),
        #     Fraction(16, 27),
        #     Fraction(16, 225),
        #     Fraction(16, 675),
        #     Fraction(64, 675),
        #     Fraction(16, 135),
        #     Fraction(32, 675),
        #     Fraction(16, 45),
        #     Fraction(64, 225),
        #     Fraction(32, 225),
        #     Fraction(16, 225),
        #     Fraction(16, 75),
        #     Fraction(128, 675),
        #     Fraction(64, 135),
        #     Fraction(64, 675),
        #     Fraction(64, 225),
        #     Fraction(256, 675),
        #     Fraction(32, 1125),
        #     Fraction(32, 3375),
        #     Fraction(128, 3375),
        #     Fraction(32, 675),
        #     Fraction(64, 3375),
        #     Fraction(256, 3375),
        #     Fraction(64, 1125),
        #     Fraction(64, 675),
        #     Fraction(128, 3375),
        #     Fraction(64, 3375),
        #     Fraction(32, 225),
        #     Fraction(128, 1125),
        #     Fraction(64, 1125),
        #     Fraction(32, 1125),
        #     Fraction(32, 375),
        #     Fraction(256, 3375),
        #     Fraction(128, 675),
        #     Fraction(128, 3375),
        #     Fraction(128, 1125),
        #     Fraction(512, 3375),
        #     Fraction(32, 675),
        #     Fraction(64, 675),
        #     Fraction(32, 225),
        #     Fraction(128, 675),
        #     Fraction(32, 135),
        #     Fraction(64, 675),
        #     Fraction(256, 3375),
        #     Fraction(128, 3375),
        #     Fraction(64, 3375),
        #     Fraction(64, 1125),
        #     Fraction(16, 375),
        #     Fraction(16, 1125),
        #     Fraction(64, 1125),
        #     Fraction(16, 225),
        #     Fraction(32, 1125),
        #     Fraction(32, 675),
        #     Fraction(16, 135),
        #     Fraction(16, 675),
        #     Fraction(16, 225),
        #     Fraction(64, 675),
        #     Fraction(32, 3375),
        #     Fraction(64, 3375),
        #     Fraction(32, 1125),
        #     Fraction(128, 3375),
        #     Fraction(32, 675),
        #     Fraction(64, 3375),
        #     Fraction(16, 1125),
        #     Fraction(16, 675),
        #     Fraction(32, 3375),
        #     Fraction(16, 3375),
        # ]
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
