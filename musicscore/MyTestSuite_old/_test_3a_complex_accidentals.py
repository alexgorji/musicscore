import random
from pathlib import Path

from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase


class TestHelloCoplexAccidentals(IdTestCase):
    def test_export_hello_world_complex_accidentals(self):
        """
        Tester creates a timewise score
        """
        s = Score()
        """
        He adds a part
        """
        p = s.add_child(Part('P1', name='Music'))
        """
        He adds a lot of random pitches with different quarter_durations
        """
        random.seed(10)
        midis = [random.randint(60, 72) for _ in range(200)]
        quarter_durations = [random.randint(1, 24) / 4 for _ in range(200)]
        for m, qd in zip(midis, quarter_durations):
            ch = Chord(m, qd)
            ch.add_lyric(ch.midis[0].accidental.sign)
            p.add_chord(ch)

        """
        ... and exports the xml
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
