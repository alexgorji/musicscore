from pathlib import Path

from musictree import Time
from musictree.chord import Chord
from musictree.score import Score
from musictree.tests.util import IdTestCase


class TestTuplets2(IdTestCase):
    def test_quarter_tuplets(self):
        score = Score()
        part = score.add_part('p1')
        part.add_measure(Time(1, 2))
        [part.add_chord(Chord(60, 2 / 3)) for _ in range(3)]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
