from pathlib import Path
from unittest import TestCase
from musicxml.xmlelement.xmlelement import *
from musicxml.xsd.xsdcomplextype import XSDComplexTypeScorePartwise
from musicxml.xsd.xsdindicator import XSDSequence

parent_folder = Path(__file__).parent


class TestScore(TestCase):

    def test_score_partwise_doc(self):
        score = XMLScorePartwise()
        assert score.__doc__ == 'The score-partwise element is the root element for a partwise MusicXML score. It includes a score-header group followed by a series of parts with measures inside. The document-attributes attribute group includes the version attribute.'

    def test_score_partwise_type(self):
        score = XMLScorePartwise()
        assert score.TYPE == XSDComplexTypeScorePartwise

    def test_xsd_complex_type_score_partwise_sequence(self):
        assert XSDComplexTypeScorePartwise.get_xsd_indicator()[0].elements == [('XMLWork', '0', '1'), ('XMLMovementNumber', '0', '1'),
                                                                               ('XMLMovementTitle', '0', '1'),
                                                                               ('XMLIdentification', '0', '1'),
                                                                               ('XMLDefaults', '0', '1'), ('XMLCredit', '0', 'unbounded'),
                                                                               ('XMLPartList', '1', '1'), ('XMLPart', '1', 'unbounded')]

    def test_score_partwise_indicator(self):
        score = XMLScorePartwise()
        assert isinstance(score.TYPE.get_xsd_indicator()[0], XSDSequence)

    def test_minimum_score(self):
        score = XMLScorePartwise()
        pl = score.add_child(XMLPartList())
        sp = pl.add_child(XMLScorePart(id='P1'))
        sp.add_child(XMLPartName('some name', print_object="no"))
        p = score.add_child(XMLPart(id='P1'))
        p.add_child(XMLMeasure(number='1'))

        score.write(parent_folder / 'test_minimum_score.xml')

    def test_hello_world(self):
        score = XMLScorePartwise(version='3.1')
        pl = score.add_child(XMLPartList())
        sp = pl.add_child(XMLScorePart(id='P1'))
        sp.add_child(XMLPartName('Part 1', print_object='no'))
        p = score.add_child(XMLPart(id='P1'))
        m = p.add_child(XMLMeasure(number='1'))
        att = m.add_child(XMLAttributes())
        att.add_child(XMLDivisions(1))
        t = att.add_child(XMLTime())
        t.add_child(XMLBeats('4'))
        t.add_child(XMLBeatType('4'))
        c = att.add_child(XMLClef())
        c.add_child(XMLSign('G'))
        c.add_child(XMLLine(2))
        k = att.add_child(XMLKey())
        k.add_child(XMLFifths(0))
        k.add_child(XMLMode('major'))
        n = m.add_child(XMLNote())
        p = n.add_child(XMLPitch())
        p.add_child(XMLStep('C'))
        p.add_child(XMLOctave(4))
        n.add_child(XMLDuration(4))
        n.add_child(XMLVoice('1'))
        n.add_child(XMLType('whole'))
        bl = m.add_child(XMLBarline(location='right'))
        bl.add_child(XMLBarStyle('light-heavy'))
        score.write(parent_folder / 'test_hello_world_actual.xml')
