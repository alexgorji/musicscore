"""
Repeats can also be nested.
"""

from pathlib import Path

from musicscore import Score, Chord
from musicscore.tests.util import IdTestCase


class TestLily45c(IdTestCase):
    def test_lily_45d_RepeatsMultipleTimes(self):
        score = Score()
        p = score.add_part('p1')
        [p.add_chord(Chord(0, 4)) for _ in range(8)]

        score.set_multi_measure_rest(2, 3)
        score.set_multi_measure_rest(4, 7)

        p.get_measure(2).set_repeat_barline(location='left')
        p.get_measure(3).set_repeat_barline(location='right')

        p.get_measure(4).set_repeat_barline(location='left')
        p.get_measure(7).set_repeat_barline(location='right')

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
