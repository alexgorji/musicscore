"""
Four multi-measure rests: 3 measures, 15 measures, 1 measure, and 12 measures.
"""
from pathlib import Path

from musicscore import Score, Chord, A
from musicscore.lyrics import Lyrics
from musicscore.tests.util import IdTestCase
from musicxml import XMLMeasureStyle


class TestLily61a(IdTestCase):
    def test_lily_61a_Lyrics(self):
        score = Score()
        part = score.add_part('p1')
        # [part.add_chord(Chord(0, 4)) for _ in range(3 + 15 + 1 + 12)]
        score.set_multiple_measure_rest(1, 3)
        score.set_multiple_measure_rest(4, 19)
        score.set_multiple_measure_rest(21, 32)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
