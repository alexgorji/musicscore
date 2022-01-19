from pathlib import Path
from unittest import TestCase

from musictree.musictree import Score, Part, Measure, Chord


class TestAcceptance(TestCase):
    def test_export_hello_world(self):
        """
        Hello World as musicxml means having a C4 pitch as a whole in a 4/4 measure with treble clef.
        """
        """
        Tester creates a timewise score
        """
        score = Score()
        """
        He adds a measure with one part to it (default Measure has a 4/4 time signature)
        """
        p = score.add_child(Part())
        m = p.add_child(Measure())
        """
        He adds a Chord with midi 60 to the part ...
        """
        m.add_child(Chord(quarter_duration=4))
        """
        ... and exports the xml (3.1 is default)
        """
        xml_path = Path(__file__).with_suffix('.muscixml')
        score.export_xml(xml_path)
