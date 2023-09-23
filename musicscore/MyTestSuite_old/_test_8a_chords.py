from pathlib import Path

from musicscore import Score, Chord
from musicscore.tests.util import IdTestCase


class TestChords(IdTestCase):
    def test_chords(self):
        s = Score()
        p = s.add_part('p1')
        midis = []
        for m in range(60, 72):
            midis = midis + [m]
            p.add_chord(Chord(midis=midis, quarter_duration=2))
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
