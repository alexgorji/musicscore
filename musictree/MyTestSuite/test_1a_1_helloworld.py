from pathlib import Path

from musictree.chord import Chord
from musictree.measure import Measure
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
        m = p.add_child(Measure(number=1))
        """
        He adds a Chord with midi 60 to the measure
        """
        m.add_chord(Chord(60, 4))
        m.update_chord_accidentals()

        """
        ... and exports the xml (3.1 is default)
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)