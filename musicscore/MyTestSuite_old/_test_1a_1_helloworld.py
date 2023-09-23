from pathlib import Path

from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase


class TestHelloWorld(IdTestCase):
    def test_export_hello_world(self):
        """
        Hello World as musicxml means having a C4 pitch as a whole in a 4/4 measure with treble clef.
        """
        """
        Tester creates score
        """
        s = Score()
        """
        He adds a part with id P1 (required) and name Music
        """
        p = s.add_child(Part('P1', name='Music'))
        """He adds a Chord with midi 60 to the part. A measure (default Measure has a 4/4 time signature) will be 
        created automatically"""
        p.add_chord(Chord(60, 4))
        """
        ... and exports the xml
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
