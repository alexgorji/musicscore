from pathlib import Path

from musicxml.xmlelement.xmlelement import *

from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase, create_technical, create_articulation, create_ornament
from musicscore.util import XML_TECHNICAL_CLASSES, XML_ARTICULATION_CLASSES, XML_OTHER_NOTATIONS, XML_DYNAMIC_CLASSES, XML_ORNAMENT_CLASSES


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
        for index, cls in enumerate(XML_ARTICULATION_CLASSES):
            next_cls = XML_ARTICULATION_CLASSES[index + 1] if index != len(XML_ARTICULATION_CLASSES) - 1 else None
            ch = Chord(60, 1)
            ch.add_x(create_articulation(cls))
            p.add_chord(ch)
            if next_cls:
                ch = Chord(60, 1)
                ch.add_x(create_articulation(cls))
                ch.add_x(create_articulation(next_cls))
                p.add_chord(ch)

        for index, cls in enumerate(XML_TECHNICAL_CLASSES):
            if cls == XMLHammerOn:
                ch = Chord(60, 1)
                ch.add_x(XMLHammerOn('2', type='start'))
                p.add_chord(ch)
                ch = Chord(60, 1)
                ch.add_x(XMLHammerOn('2', type='stop'))
            elif cls == XMLPullOff:
                ch = Chord(60, 1)
                ch.add_x(XMLPullOff('2', type='start'))
                p.add_chord(ch)
                ch = Chord(60, 1)
                ch.add_x(XMLPullOff('2', type='stop'))
            else:
                next_cls = XML_TECHNICAL_CLASSES[index + 1] if index != len(XML_TECHNICAL_CLASSES) - 1 else None
                ch = Chord(60, 1)
                ch.add_x(create_technical(cls))
                p.add_chord(ch)
                if next_cls and next_cls not in [XMLHammerOn, XMLPullOff]:
                    ch = Chord(60, 1)
                    ch.add_x(create_technical(cls))
                    ch.add_x(create_technical(next_cls))
                    ch.add_x(XMLAccent(placement='above'))
                    p.add_chord(ch)

        for cls in XML_ORNAMENT_CLASSES[1:]:
            ch = Chord(60, 1)
            ch.add_x(create_ornament(cls))
            p.add_chord(ch)
        ch = Chord(60, 4)
        p.add_chord(ch)
        ch.add_x(XMLTrillMark())
        ch.add_x(XMLAccidentalMark('sharp'))
        ch.add_x(XMLWavyLine(type='start'))
        ch.add_x(XMLWavyLine(type='stop'))

        for cls in XML_DYNAMIC_CLASSES:
            ch = Chord(60, 1)
            ch.add_x(cls(), placement='below')
            p.add_chord(ch)

        for cls in XML_OTHER_NOTATIONS:
            if cls in [XMLGlissando, XMLSlide, XMLSlur]:
                ch = Chord(60, 1)
                ch.add_x(cls(type='start'))
                p.add_chord(ch)
                ch = Chord(60, 1)
                ch.add_x(cls(type='stop'))
                p.add_chord(ch)
            elif cls == XMLNonArpeggiate:
                ch = Chord(60, 1)
                ch.add_x(cls(type='top'))
                p.add_chord(ch)
            elif cls == XMLOtherNotation:
                ch = Chord(60, 1)
                ch.add_x(cls(type='single'))
                p.add_chord(ch)
            else:
                ch = Chord(60, 1)
                ch.add_x(cls())
                p.add_chord(ch)
        """
        ... and exports the xml
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
