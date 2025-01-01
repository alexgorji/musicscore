from fractions import Fraction
from pathlib import Path
from musicscore.chord import Chord
from musicscore.score import Score
from musicscore.tests.util import XMLTestCase
from musicscore.tests.util_subdivisions import generate_all_subdivision_patterns

path = Path(__file__)


class ConfigureSixtupletsTestCase(XMLTestCase):
    def setUp(self):
        self.score = Score()
        self.part = self.score.add_part("P1")
        self.part.add_measure(time=(1, 4))

    def test_default_sixtuplets(self):
        patterns = generate_all_subdivision_patterns(6, False)
        for pattern in patterns:
            for qd in pattern:
                self.part.add_chord(Chord(60, Fraction(qd, 6)))
        with self.file_path(path, "default") as xml_path:
            self.score.export_xml(xml_path)

    def test_simplified_sixtuplets(self):
        patterns = generate_all_subdivision_patterns(6, False)
        for pattern in patterns:
            for qd in pattern:
                self.part.add_chord(Chord(60, Fraction(qd, 6)))
        for beat in self.part.get_beats():
            beat.simplified_sixtuplets = True
        with self.file_path(path, "simplified") as xml_path:
            self.score.export_xml(xml_path)
