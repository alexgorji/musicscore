from pathlib import Path

from musictree.chord import Chord
from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import IdTestCase, create_articulation
from musictree.util import XML_ARTICULATION_CLASSES


class TestHelloWorldArticulations(IdTestCase):
    def test_export_hello_world(self):
        """
        Tester creates a timewise score
        """
        s = Score()
        """
        He adds a list of chords with articulations to a part
        """
        p = s.add_child(Part('P1'))
        for index in range(len(XML_ARTICULATION_CLASSES)):
            articulation_class = XML_ARTICULATION_CLASSES[index]
            next_articulation_class = XML_ARTICULATION_CLASSES[index + 1] if index != len(XML_ARTICULATION_CLASSES) - 1 else None
            ch = Chord(60, 1)
            ch.add_xml_articulation(create_articulation(articulation_class))
            p.add_chord(ch)
            if next_articulation_class:
                ch = Chord(60, 1)
                ch.add_xml_articulation(create_articulation(articulation_class))
                ch.add_xml_articulation(create_articulation(next_articulation_class))
                p.add_chord(ch)

        """
        ... and exports the xm
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
