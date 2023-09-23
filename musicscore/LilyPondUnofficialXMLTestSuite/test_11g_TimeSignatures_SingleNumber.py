from pathlib import Path

from musicscore import Score, Time, Chord, B
from musicscore.tests.util import IdTestCase

"""
Time signature displayed as a single number.
"""


class TestLily11g(IdTestCase):
    def test_lily_11g_TimeSignatures_SingleNumber(self):
        score = Score()
        part = score.add_part('part')
        part.add_measure(time=Time(3, 8, symbol='single-number'))
        [part.add_chord(Chord(B(4), x / 2)) for x in [1, 1, 1]]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
