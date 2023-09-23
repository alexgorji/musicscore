"""
Compound time signatures with same denominator: (3+2)/8 and (5+3+1)/4.
"""
from pathlib import Path

from musicscore import Score, Time, Chord, B
from musicscore.tests.util import IdTestCase


class TestLily11c(IdTestCase):
    def test_lily_11c_TimeSignatures_CompoundSimple(self):
        score = Score()
        part = score.add_part('part')
        part.add_measure(time=Time('3+2', 8))
        part.add_measure(time=Time('5+3+1', 4))
        [part.add_chord(Chord(B(4), x / 2)) for x in [1, 1, 1, 1, 1]]
        [part.add_chord(Chord(B(4), x)) for x in [4, 1, 3, 1]]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
