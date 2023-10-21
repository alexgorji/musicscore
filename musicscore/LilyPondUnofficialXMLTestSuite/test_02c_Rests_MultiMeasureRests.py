"""
Four multi-measure rests: 3 measures, 15 measures, 1 measure, and 12 measures.
"""
from pathlib import Path

from musicscore import Score
from musicscore.tests.util import IdTestCase


class TestLily61a(IdTestCase):
    def test_lily_61a_Lyrics(self):
        score = Score()
        score.add_part('p1')
        score.set_multi_measure_rest(1, 3)
        score.set_multi_measure_rest(4, 19)
        score.set_multi_measure_rest(21, 32)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
