from pathlib import Path

from quicktions import Fraction

from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase
from musicscore.tests.util_subdivisions import generate_all_16ths_manually, generate_all_32nds_manually


class TestBeams1(IdTestCase):
    def test_beams_1(self):
        """
        Write all possible combinations of 16ths and 32nds in a beat
        """
        s = Score()
        p = s.add_child(Part('P1', name='Music'))

        p.add_measure(time=(1, 4))

        groups = [(Fraction(1, 2), Fraction(1, 2))] + generate_all_16ths_manually() + generate_all_32nds_manually()
        for group in groups:
            for qd in group:
                p.add_chord(Chord(60, qd))
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
