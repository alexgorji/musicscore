from pathlib import Path

from musicscore import Score, Chord
from unittest import TestCase

"""
A simple, repeated measure (repeated 5 times)
"""


class TestLily45a(TestCase):
    def test_lily_45a_SimpleRepeat(self):
        score = Score()
        part = score.add_part("p1")

        [part.add_chord(Chord(0, 4)) for _ in range(2)]
        part.get_measure(1).set_repeat_barline(times=5)

        xml_path = Path(__file__).with_suffix(".xml")
        score.export_xml(xml_path)
