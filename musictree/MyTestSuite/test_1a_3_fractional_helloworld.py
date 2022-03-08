from pathlib import Path
from unittest import TestCase

from musictree.chord import Chord
from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import IdTestCase


class TestHelloWorld(IdTestCase):
    def test_export_hello_world(self):
        """
        Hello World as musicxml means having a C4 pitch as a whole in a 4/4 measure with treble clef.
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
        He adds a fractional Chord with midi 61 to Part
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
        ... and exports the xml (3.1 is default)
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
