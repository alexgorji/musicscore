"""
Nested repeats, each with alternative endings.
"""

from pathlib import Path

from musicscore import Score, Chord
from musicscore.tests.util import IdTestCase


class TestLily45d(IdTestCase):
    def test_lily_45d_Repeats_Nested_Alternatives(self):
        score = Score()
        p = score.add_part('p1')
        [p.add_chord(Chord(0, 4)) for _ in range(11)]

        score.set_multi_measure_rest(3, 5)
        score.set_multi_measure_rest(6, 8)

        p.get_measure(2).set_repeat_barline()
        p.get_measure(2).set_repeat_ending(number=1, type='start')
        p.get_measure(2).set_repeat_ending(number=1, type='stop')

        p.get_measure(3).set_repeat_ending(number=2, type='start')
        p.get_measure(5).set_repeat_ending(number=2, type='discontinue')

        p.get_measure(9).set_repeat_barline()
        p.get_measure(9).set_repeat_ending(number=1, type='start')
        p.get_measure(9).set_repeat_ending(number=1, type='stop')

        p.get_measure(10).set_repeat_ending(number=2, type='start')
        p.get_measure(10).set_repeat_ending(number=5, type='discontinue')

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
