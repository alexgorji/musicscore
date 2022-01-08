from pathlib import Path
from unittest import TestCase
from xmldiff import main
from musicxml.xmlelement.xmlelement import *
from musicxml.xsd.xsdcomplextype import XSDComplexTypeScorePartwise
from musicxml.xsd.xsdindicators import *
from musicxml.xsd.xsdindicators import XSDSequence

parent_folder = Path(__file__).parent


class TestScore(TestCase):
    def test_diff_xml_files(self):
        """
        Test if xml file can be tested properly
        """

        expected = 'test_expected.xml'
        actual = 'test_actual.xml'
        diff = main.diff_files(actual, expected)
        assert diff == []

    def test_score_partwise_doc(self):
        score = XMLScorePartwise()
        assert score.__doc__ == 'The score-partwise element is the root element for a partwise MusicXML score. It includes a score-header group followed by a series of parts with measures inside. The document-attributes attribute group includes the version attribute.'

    def test_score_partwise_type(self):
        score = XMLScorePartwise()
        assert score.type_ == XSDComplexTypeScorePartwise

    def test_xsd_complex_type_score_partwise_sequence(self):
        assert XSDComplexTypeScorePartwise.get_xsd_indicator()[0].elements == [('XMLWork', '0', '1'), ('XMLMovementNumber', '0', '1'),
                                                                               ('XMLMovementTitle', '0', '1'),
                                                                               ('XMLIdentification', '0', '1'),
                                                                               ('XMLDefaults', '0', '1'), ('XMLCredit', '0', 'unbounded'),
                                                                               ('XMLPartList', '1', '1'), ('XMLPart', '1', 'unbounded')]

    def test_score_partwise_indicator(self):
        score = XMLScorePartwise()
        assert isinstance(score.type_.get_xsd_indicator()[0], XSDSequence)

    def test_minimum_score(self):
        score = XMLScorePartwise()
        pl = score.add_child(XMLPartList())
        sp = pl.add_child(XMLScorePart(id='P1'))
        sp.add_child(XMLPartName('some name'))
        p = score.add_child(XMLPart(id='P1'))
        p.add_child(XMLMeasure(number='1'))

        score.write(parent_folder / 'test_minimum_score.xml')
        diff = main.diff_files('test_minimum_score.xml', 'test_minimum_score_expected.xml')
        assert diff == []
