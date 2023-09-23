"""
Some tuples (3:2, 3:2, 3:2, 4:2, 4:1, 7:3, 6:2) with the default tuplet bracket displaying the number of actual
notes played. The second tuplet does not have a number attribute set.
"""
from pathlib import Path

from musicscore import Score, Time, Chord, A, B, C, D, E, F, G
from musicscore.tests.util import IdTestCase


class TestLily23a(IdTestCase):
    def test_lily_23a_Tuplets(self):
        score = Score()
        part = score.add_part('p1')

        part.add_measure(Time(2, 2))
        scale = [C(4), D(4), E(4), F(4), G(4), A(4), B(4), C(5), D(5), E(5), F(5), G(5), A(5), B(5), C(6)]
        scale += list(reversed(scale))
        for m, d in zip(scale, 9 * [2 / 3] + 8 * [1] + 7 * [2 / 7] + 6 * [2 / 3]):
            part.add_chord(Chord(m, d))

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
