from pathlib import Path

from musicscore import Score, Chord, Midi, Time
from unittest import TestCase

"""
All pitch intervals in ascending jump size.
"""


class TestLily01b(TestCase):
    def test_lily_01b_Pitches_Intervals(self):
        score = Score("Various pitches and interval sizes")
        p = score.add_part("intervals")
        p.add_measure(Time(2, 4))
        for i in range(24):
            m1 = Midi(72 + i)
            m2 = Midi(72 - i)
            p.add_chord(Chord(m1, 1))
            p.add_chord(Chord(m2, 1))

        xml_path = Path(__file__).with_suffix(".xml")
        score.export_xml(xml_path)
