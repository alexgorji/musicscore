"""
A simple repeat with two alternative endings (volta brackets).
"""

from pathlib import Path

from musicscore import Score, Chord
from musicscore.tests.util import IdTestCase


class TestLily45b(IdTestCase):
    def test_lily_45b_RepeatWithAlternatives(self):
        score = Score()
        part = score.add_part('p1')
        [part.add_chord(Chord(72, 4)) for _ in range(4)]
        part.get_measure(2).set_repeat_barline()
        part.get_measure(2).set_repeat_ending(number=1, type='start')
        part.get_measure(2).set_repeat_ending(number=1, type='stop')
        part.get_measure(3).set_repeat_ending(number=2, type='start')
        part.get_measure(3).set_repeat_ending(number=2, type='discontinue')
        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
