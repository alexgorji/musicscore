from pathlib import Path
from unittest import TestCase

from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase


class TestHelloWorld(IdTestCase):
    def test_export_hello_world(self):
        """
        Hello World Variation II: C4 with 1/3, 1/5, 1/6 and 1/10 based durations in one measure.
        """
        """
        Tester creates a timewise score
        """
        s = Score()
        """
        He adds a measure with one part to it (default Measure has a 4/4 time signature)
        """
        p = s.add_child(Part('P1', name='Music'))
        """
        He adds a 4/4 measure
        """
        p.add_measure((4, 4))
        """
        He adds a fractional Chord with midi 60 to Part
        """
        p.add_chord(Chord(60, 1 / 3))
        p.add_chord(Chord(60, 2 / 3))
        p.add_chord(Chord(60, 1 / 5))
        p.add_chord(Chord(60, 4 / 5))
        p.add_chord(Chord(60, 2 / 5))
        p.add_chord(Chord(60, 3 / 5))
        p.add_chord(Chord(60, 1 / 6))
        p.add_chord(Chord(60, 1 / 6))
        p.add_chord(Chord(60, 1 / 6))
        p.add_chord(Chord(60, 1 / 10))
        p.add_chord(Chord(60, 3 / 10))
        p.add_chord(Chord(60, 1 / 10))
        """
        ... and exports the xml
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
