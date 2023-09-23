from pathlib import Path
from unittest import TestCase

from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase


class TestHelloWorld(IdTestCase):
    def test_export_hello_world(self):
        """
        Hello World, Variation I: C4 pitch, 20 beats long, in three 5/4 measures with treble clef.
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
        He adds a 5/4 measure
        """
        p.add_measure(time=(5, 4))
        """
        He adds a long Chord with midi 61 to Part
        """
        p.add_chord(Chord(60, 15))
        """
        ... and exports the xml
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
