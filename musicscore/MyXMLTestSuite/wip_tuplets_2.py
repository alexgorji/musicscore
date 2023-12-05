from pathlib import Path

from musicscore import Time
from musicscore.chord import Chord
from musicscore.score import Score
from musicscore.tests.util import IdTestCase
from musicscore.tests.util_subdivisions import generate_all_quintuplets_manually, generate_all_sextuplets_manually, \
    generate_all_septuplets_manually, generate_all_triplets_manually


class TestTuplets2(IdTestCase):
    def test_quarter_tuplets(self):
        score = Score()
        part = score.add_part('p1')
        t = Time(4, 4)
        t.actual_signatures = [1, 2, 1, 2]
        part.add_measure(t)
        tuplets = generate_all_triplets_manually() + generate_all_quintuplets_manually()


        tuplets = [x * 2 for t in tuplets for x in t]

        for t in tuplets:
            part.add_chord(Chord(60, t))

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
