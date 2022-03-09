from pathlib import Path

from quicktions import Fraction

from musictree.chord import Chord
from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import IdTestCase, generate_all_16ths, generate_all_32nds


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
        # for qd in groups[87]:
        #     p.add_chord(Chord(60, qd))
        # for qd in groups[7]:
        #     p.add_chord(Chord(60, qd))
        """
        ... and exports the xml
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
