from pathlib import Path

from quicktions import Fraction

from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase
from musicscore.tests.util_subdivisions import generate_all_quintuplets_manually, generate_all_sextuplets_manually, \
    generate_all_septuplets_manually, generate_all_triplets_manually, generate_all_subdivisions, \
    generate_all_subdivision_patterns


class TestTuplets1(IdTestCase):
    def test_tuplets_1(self):
        """
        Write all possible tuplet combinations up until 32nds
        """

        s = Score()

        p = s.add_child(Part('P1', name='Music'))

        p.add_measure(time=(1, 4))

        rhythmic_patterns = []
        for subdivision in range(8, 9):
            rhythmic_patterns.extend(generate_all_subdivision_patterns(subdivision, True))

        for rhythmic_pattern in rhythmic_patterns:
            subdivision = sum(rhythmic_pattern)
            for x in rhythmic_pattern:
                ch = Chord(60, Fraction(x, subdivision))
                ch.add_lyric(x)
                p.add_chord(ch)
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
