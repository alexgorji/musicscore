"""
Different Arpeggio directions (normal, up, down, non-arpeggiate)
"""

from pathlib import Path

from musicscore import Score, Chord, C, E, G
from unittest import TestCase


class TestLily32d(TestCase):
    def test_lily_32d_Arpeggio(self):
        score = Score()
        part = score.add_part("p1")

        types = ["normal", "up", "normal", "down", "normal", "none", "normal"]
        chords = [Chord([C(4), E(5), G(5)], 1) for _ in types]

        for t, ch in zip(types, chords):
            ch.arpeggio = t

        [part.add_chord(ch) for ch in chords]

        xml_path = Path(__file__).with_suffix(".xml")
        score.export_xml(xml_path)
