"""
Various time signatures: 2/2 (alla breve), 4/4 (C), 2/2, 3/2, 2/4, 3/4, 4/4, 5/4, 3/8, 6/8, 12/8
"""
from pathlib import Path

from musicscore import Score, generate_measures, Chord, C
from musicscore.tests.util import IdTestCase


class TestLily11a(IdTestCase):
    def test_lily_11a_TimeSignatures(self):
        score = Score('Time signatures')
        p = score.add_part('ts')

        for measure in generate_measures(
                [(2, 2), (4, 4), (2, 2), (3, 2), (2, 4), (3, 4), (4, 4), (5, 4), (3, 8), (6, 8), (12, 8)]):
            p.add_child(measure)
            p.add_chord(Chord(C(5), measure.quarter_duration))

        p.get_measure(1).time.symbol = 'cut'
        p.get_measure(2).time.symbol = 'common'

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
