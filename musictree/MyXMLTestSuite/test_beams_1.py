from pathlib import Path

from quicktions import Fraction

from musictree.chord import Chord
from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import IdTestCase, generate_all_16ths, generate_all_32nds


class TestBeams1(IdTestCase):
    def test_beams_1(self):
        """
        Write all possible combinations of 16ths and 32nds in a beat
        """
        s = Score()
        p = s.add_child(Part('P1', name='Music'))

        p.add_measure(time=(1, 4))

        groups = [(Fraction(1, 2), Fraction(1, 2))] + generate_all_16ths() + generate_all_32nds()
        for group in groups:
            for qd in group:
                p.add_chord(Chord(60, qd))
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
