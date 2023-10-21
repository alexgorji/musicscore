"""
Some more nested repeats with alternatives.
"""

from pathlib import Path

from musicscore import Score, Chord
from musicscore.tests.util import IdTestCase


class TestLily45e(IdTestCase):
    def test_lily_45e_Repeats_Nested_Alternatives(self):
        score = Score()
        p = score.add_part('p1')
        [p.add_chord(Chord(0, 4)) for _ in range(10)]

        score.set_multi_measure_rest(8, 9)

        p.get_measure(2).set_repeat_barline()
        p.get_measure(2).set_repeat_ending(number=1, type='start')
        p.get_measure(2).set_repeat_ending(number=1, type='stop')

        p.get_measure(3).set_repeat_ending(number=2, type='start')
        p.get_measure(3).set_repeat_ending(number=2, type='discontinue')

        p.get_measure(5).set_repeat_barline(location='left')
        p.get_measure(5).set_repeat_barline()

        p.get_measure(6).new_system = True

        p.get_measure(7).set_repeat_barline()
        p.get_measure(7).set_repeat_ending(number="1, 2", type='start')
        p.get_measure(7).set_repeat_ending(number="1, 2", type='stop')

        p.get_measure(8).set_repeat_barline(location='left')
        p.get_measure(9).set_repeat_barline()

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
