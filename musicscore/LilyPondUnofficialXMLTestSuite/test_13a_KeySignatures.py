from pathlib import Path

from musicscore import Score, Time, Chord, Key
from unittest import TestCase

"""
Various key signature: from 11 flats to 11 sharps
"""


class TestLily131(TestCase):
    def test_lily_13a_KeySignatures(self):
        score = Score()
        part = score.add_part("p1")
        part.add_measure(Time(2, 4))
        for x in range(-11, 12):
            part.add_chord(Chord(60, 2))
            part.get_current_measure().key = Key(fifths=x)

        xml_path = Path(__file__).with_suffix(".xml")
        score.export_xml(xml_path)
