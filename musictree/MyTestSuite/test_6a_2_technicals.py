from pathlib import Path

from musicxml.xmlelement.xmlelement import XMLAccent

from musictree.chord import Chord
from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import IdTestCase, create_technical
from musictree.util import XML_TECHNICAL_CLASSES


class TestHelloWorldTechnicals(IdTestCase):
    def test_export_hello_world(self):
        """
        Tester creates a timewise score
        """
        s = Score()
        """
        He adds a list of chords with technicals to a part
        """
        p = s.add_child(Part('P1'))
        for index in range(len(XML_TECHNICAL_CLASSES)):
            technical_class = XML_TECHNICAL_CLASSES[index]
            next_technical_class = XML_TECHNICAL_CLASSES[index + 1] if index != len(XML_TECHNICAL_CLASSES) - 1 else None
            ch = Chord(60, 1)
            ch.add_xml_technical(create_technical(technical_class))
            p.add_chord(ch)
            if next_technical_class:
                ch = Chord(60, 1)
                ch.add_xml_technical(create_technical(technical_class))
                ch.add_xml_technical(create_technical(next_technical_class))
                ch.add_xml_articulation(XMLAccent(placement='above'))
                p.add_chord(ch)

        """
        ... and exports the xm
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
