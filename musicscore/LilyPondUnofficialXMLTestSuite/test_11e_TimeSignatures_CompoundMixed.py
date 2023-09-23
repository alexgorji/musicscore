from pathlib import Path

from musicscore import Score, Time, Chord, B
from musicscore.tests.util import IdTestCase

"""
Compound time signatures of mixed type: (3+2)/8+3/4.
"""


class TestLily11e(IdTestCase):
    def test_lily_11e_TimeSignatures_CompoundMixed(self):
        score = Score()
        part = score.add_part('part')
        part.add_measure(time=Time('3+2', 8, 3, 4))
        [part.add_chord(Chord(B(4), x / 2)) for x in [1, 1, 1, 1, 1]]
        [part.add_chord(Chord(B(4), x)) for x in [1, 1, 1]]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
