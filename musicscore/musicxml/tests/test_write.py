from unittest import TestCase
from musicscore.musicxml.elements.xml_partwise import XMLScorePartwise, XMLPartPartwise, XMLMeasurePartwise
from musicscore.musicxml.elements.xml_score_header import XMLScorePart
from musicscore.musicxml.elements.xml_note import XMLNote, XMLPitch
from musicscore.musicxml.elements.xml_attributes import XMLTime, XMLClef, XMLDivisions, XMLAttributes

import os
path = os.path.abspath(__file__).split('.')[0]


class TestXMLScorePartwise(TestCase):
    def setUp(self):
        self.score = XMLScorePartwise()
        part_id = 'P1'
        self.score.add_score_part(XMLScorePart(id=part_id))
        part = self.score.add_child(XMLPartPartwise(id=part_id))
        measure = self.make_measure()
        part.add_child(measure)

    def make_measure(self):
        measure = XMLMeasurePartwise(number=1)
        xml_attributes = measure.add_child(XMLAttributes())
        xml_attributes.add_child(XMLTime(4, 4))
        xml_attributes.add_child(XMLClef('G', 2))
        xml_attributes.add_child(XMLDivisions(1))
        measure.add_child(XMLNote(event=XMLPitch(), duration=4))
        return measure

    def test_xml_score(self):
        self.score.write(path=path)



