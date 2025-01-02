from fractions import Fraction
from pathlib import Path
from musicscore.chord import Chord
from musicscore.score import Score
from musicscore.tests.util import XMLTestCase
from musicscore.tests.util_subdivisions import generate_all_subdivision_patterns

path = Path(__file__)


class ConfigureSextupletsTestCase(XMLTestCase):
    def setUp(self):
        self.patterns = generate_all_subdivision_patterns(6, False)
        self.score = Score()
        self.part = self.score.add_part("P1")
        self.part.add_measure(time=(1, 4))

    def test_default_sextuplets(self):
        for pattern in self.patterns:
            for qd in pattern:
                self.part.add_chord(Chord(60, Fraction(qd, 6)))
        with self.file_path(path, "default") as xml_path:
            self.score.export_xml(xml_path)

    def test_simplified_sextuplets(self):
        score = Score(simplified_sextuplets=True)
        part = score.add_part("P1")
        part.add_measure(time=(1, 4))
        for pattern in self.patterns:
            for qd in pattern:
                part.add_chord(Chord(60, Fraction(qd, 6)))
        with self.file_path(path, "simplified") as xml_path:
            score.export_xml(xml_path)

    def test_part_default_and_simplified_sextuplets(self):
        patterns = generate_all_subdivision_patterns(6, True)
        self.part.name = "default"
        for pattern in patterns:
            for qd in pattern:
                self.part.add_chord(Chord(60, Fraction(qd, 6)))
        part = self.score.add_part("P2")
        part.name = "simplified"
        part.add_measure(time=(1, 4))
        for pattern in patterns:
            for qd in pattern:
                part.add_chord(Chord(60, Fraction(qd, 6)))
        part.simplified_sextuplets = True
        with self.file_path(path, "part_default_and_simplified") as xml_path:
            self.score.export_xml(xml_path)
