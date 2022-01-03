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
        assert XSDComplexTypeScorePartwise.get_xsd_indicator().elements == [('XMLWork', '0', '1'), ('XMLMovementNumber', '0', '1'),
                                                                            ('XMLMovementTitle', '0', '1'), ('XMLIdentification', '0', '1'),
                                                                            ('XMLDefaults', '0', '1'), ('XMLCredit', '0', 'unbounded'),
                                                                            ('XMLPartList', '1', '1'), ('XMLPart', '1', 'unbounded')]

    def test_score_partwise_indicator(self):
        score = XMLScorePartwise()
        assert isinstance(score.type_.get_xsd_indicator(), XSDSequence)

    def test_hello_world(self):
        score = XMLScorePartwise()
        score.add_child(XMLPartList())
        score.add_child(XMLPart())

        score.write(parent_folder / 'test_helloworld_actual.xml')
        diff = main.diff_files('test_helloworld_actual.xml', 'test_helloworld_expected.xml')
        assert diff == []
