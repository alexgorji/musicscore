"""
Rests can have explicit pitches, where they are displayed. The first rest uses no explicit position and should use the default position, all others are explicitly positioned somewhere else.
"""

from pathlib import Path

from musicscore import Score
from musicscore.chord import Rest
from unittest import TestCase


class TestLily02b(TestCase):
    def test_lily_02b_Rests_PitchedRests(self):
        score = Score()
        part = score.add_part("p1")

        part.add_measure(time=(5, 4))
        rest_step_octaves = [None, ("D", 4), ("F", 5), ("A", 3), ("C", 6)]
        rests = [Rest(1, so[0], so[1]) if so else Rest(1) for so in rest_step_octaves]
        [part.add_chord(r) for r in rests]
        xml_path = Path(__file__).with_suffix(".xml")
        score.export_xml(xml_path)
