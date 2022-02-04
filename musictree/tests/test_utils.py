from pathlib import Path
from unittest import TestCase

from musictree.score import Score
from musictree.tests.util import diff_xml, _create_expected_path
from musictree.util import isinstance_as_string


class TestUtils(TestCase):
    def test_isinstance_as_string(self):
        assert isinstance_as_string(Score, 'Score')
        assert isinstance_as_string(Score, 'MusicTree')
        assert not isinstance_as_string(Score, 'str')

        class Measure:
            pass

        assert not isinstance_as_string(Measure, 'MusicTree')

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
