"""
A simple piano staff
"""
from pathlib import Path

from musicscore import Score, F, Chord, B
from musicscore.tests.util import IdTestCase


class TestLily43a(IdTestCase):
    def test_lily_43a_PianoStaff(self):
        score = Score()
        part = score.add_part('p1')
        part.add_chord(Chord(F(4), 4), staff_number=1)
        part.add_chord(Chord(B(2), 4), staff_number=2)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
