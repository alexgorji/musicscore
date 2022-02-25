from pathlib import Path
from unittest import TestCase

from musictree.midi import MidiNote, C
from musicxml.xmlelement.xmlelement import XMLClef, XMLSign, XMLLine

from musictree.score import Score
from musictree.tests.util import diff_xml, _create_expected_path
from musictree.util import isinstance_as_string, lcm


class TestUtils(TestCase):
    def test_isinstance_as_string(self):
        assert isinstance_as_string(Score(), 'Score')
        assert isinstance_as_string(Score(), 'MusicTree')
        assert not isinstance_as_string(Score(), 'str')

        class Measure:
            pass

        assert not isinstance_as_string(Measure(), 'MusicTree')

        assert isinstance_as_string(C(4), 'MidiNote')
        assert isinstance_as_string(C(4), 'Midi')
        assert isinstance_as_string(C(4), 'C')
        assert not isinstance_as_string(C(4), 'str')

    def test_create_expected_path(self):
        path = Path(__file__).parent / 'test_util_diff_xml.xml'
        expected_path = _create_expected_path(path)
        assert expected_path == Path(__file__).parent / 'test_util_diff_xml_expected.xml'

    def test_diff_xml_no_diff(self):
        path = Path(__file__).parent / 'test_util_diff_xml.xml'
        assert diff_xml(path) == []

    def test_diff_xml_with_diff(self):
        path = Path(__file__).parent / 'test_util_diff_xml.xml'
        path2 = Path(__file__).parent / 'test_util_diff_xml_with_diff.xml'
        assert diff_xml(path, path2) == ['- <key>', '- <fifths>0</fifths>', '- </key>']

    def test_lcm(self):
        assert lcm([3, 4, 5, 7]) == 420
        assert lcm([2, 4, 6]) == 12

    # def test_update_xml_object(self):
    #     old = XMLClef(number=3)
    #     s1 = old.add_child(XMLSign('F'))
    #     l1 = old.add_child(XMLLine(4))
    #
    #     new = XMLClef(number=2)
    #     s2 = new.add_child(XMLSign('F'))
    #     l2 = new.add_child(XMLLine(2))
    #
    #     update_xml_object(old, new)
    #
    #     assert old != new
    #     assert old.xml_sign == s1 != s2
    #     assert s1.value == 'F'
    #     assert old.xml_line == l2 != l1
    #     assert l1.value == l2.value == 2
    #     assert old.number == new.number == 2
