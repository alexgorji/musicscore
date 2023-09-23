from pathlib import Path

from musicscore import Score, Chord
from musicscore.tests.util import IdTestCase


class TestParts(IdTestCase):
    def test_multiple_parts(self):
        """
        Create multiple parts with names
        """
        score = Score()
        for i in range(5):
            p = score.add_part(f'part-{i}')
            p.add_chord(Chord(0, 4))

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
