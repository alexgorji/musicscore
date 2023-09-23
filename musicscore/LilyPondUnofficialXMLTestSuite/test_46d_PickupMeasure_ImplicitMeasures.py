"""
A 3/8 pickup measure, a measure that is split into one (incomplete, only 2/4) measure and an implicit measure,
and an incomplete measure (containg 3/4)
"""
from pathlib import Path

from musicscore import Score, Time, Chord, E, F, G, A, B, C, D
from musicscore.tests.util import IdTestCase


class TestLily46d(IdTestCase):
    def test_lily_46d_PicupMeasure_ImplicitMeasure(self):
        score = Score()
        part = score.add_part('p1')
        t = Time(4, 4)
        t.actual_signatures = [3, 8]
        part.add_measure(time=t)
        part.add_measure(Time(4, 4))
        for d in [2, 1]:
            part.add_chord(Chord(E(4), d*1/2))
        for m in [F(4), G(4), A(4), B(4), C(5), D(5), 0]:
            part.add_chord(Chord(m, 1))

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)

