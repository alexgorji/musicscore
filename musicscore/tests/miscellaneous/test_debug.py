from fractions import Fraction
from pathlib import Path
from musicscore.chord import Chord
from musicscore.score import Score
from musicscore.tests.util import XMLTestCase

path = Path(__file__)


class DebugginTests(XMLTestCase):
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
