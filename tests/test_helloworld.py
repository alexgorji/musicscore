from pathlib import Path
from unittest import TestCase

from musictree.treechord import TreeChord
from musictree.treescore import TreeScore


class TestAcceptance(TestCase):
    def test_export_hello_world(self):
        """
        Hello World as musicxml means having a C4 pitch as a whole in a 4/4 measure with treble clef.
        """
        """
        Tester creates a timewise score
        """
        score = TreeScore()
        """
        He adds a measure with one part to it (default TreeMeasure has a 4/4 time signature)
        """
        score.add_part()
        score.parts[-1].add_measure()
        """
        He adds a TreeChord with midi 60 to the part ...
        """
        score.parts[-1].measures[-1].add_chord(TreeChord(midis=[60]))
        """
        ... and exports the xml (3.1 is default)
        """
        xml_path = Path(__file__).with_suffix('.muscixml')
        score.export_xml(xml_path)
