from pathlib import Path

from quicktions import Fraction

from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase, generate_all_16ths, generate_all_32nds


class TestHelloTBeams1(IdTestCase):
    def test_export_hello_world_tuplets_1(self):
        """
        Write all possible combinations of 16ths and 32nds in a beat
        """
        """
        Tester creates a timewise score
        """
        s = Score()
        """
        He adds a measure with one part to it
        """
        p = s.add_child(Part('P1', name='Music'))
        """
        He adds a 1/4 measure
        """
        p.add_measure(time=(1, 4))
        """
        All possible combinations are:
        """
        groups = [(Fraction(1, 2), Fraction(1, 2))] + generate_all_16ths() + generate_all_32nds()
        for group in groups:
            for qd in group:
                p.add_chord(Chord(60, qd))
        """
        ... and exports the xml
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
