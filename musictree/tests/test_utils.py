from pathlib import Path
from unittest import TestCase

from musictree.midi import C

from musictree.score import Score
from musictree.tests.util import diff_xml, _create_expected_path, find_key
from musictree.util import lcm, isinstance_as_string


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


class TestFindKey(TestCase):
    def setUp(self):
        self.dict = {'part': {'@id': 'part-1',
                              'measure': [{'@number': '1',
                                           'attributes': {'clef': [{'@number': '1',
                                                                    'clef-octave-change': '2',
                                                                    'line': '2',
                                                                    'sign': 'G'},
                                                                   {'@number': '2',
                                                                    'line': '2',
                                                                    'sign': 'G'},
                                                                   {'@number': '3',
                                                                    'line': '4',
                                                                    'sign': 'F'}],
                                                          'divisions': '1',
                                                          'key': {'fifths': '0'},
                                                          'staves': '3',
                                                          'time': {'beat-type': '4', 'beats': '4'}},
                                           'backup': [{'duration': '4'}, {'duration': '4'}],
                                           'note': [{'duration': '1',
                                                     'pitch': {'octave': '4', 'step': 'C'},
                                                     'staff': '1',
                                                     'type': 'quarter',
                                                     'voice': '1'},
                                                    {'accidental': 'sharp',
                                                     'duration': '2',
                                                     'pitch': {'alter': '1',
                                                               'octave': '4',
                                                               'step': 'C'},
                                                     'staff': '1',
                                                     'type': 'half',
                                                     'voice': '1'},
                                                    {'duration': '1',
                                                     'notations': {'tied': {'@type': 'start'}},
                                                     'pitch': {'octave': '4', 'step': 'D'},
                                                     'staff': '1',
                                                     'tie': {'@type': 'start'},
                                                     'type': 'quarter',
                                                     'voice': '1'},
                                                    {'accidental': 'flat',
                                                     'dot': None,
                                                     'duration': '3',
                                                     'pitch': {'alter': '-1',
                                                               'octave': '4',
                                                               'step': 'E'},
                                                     'staff': '2',
                                                     'type': 'half',
                                                     'voice': '1'},
                                                    {'accidental': 'natural',
                                                     'duration': '1',
                                                     'notations': {'tied': {'@type': 'start'}},
                                                     'pitch': {'octave': '4', 'step': 'E'},
                                                     'staff': '2',
                                                     'tie': {'@type': 'start'},
                                                     'type': 'quarter',
                                                     'voice': '1'},
                                                    {'duration': '1',
                                                     'pitch': {'octave': '4', 'step': 'C'},
                                                     'staff': '3',
                                                     'type': 'quarter',
                                                     'voice': '1'},
                                                    {'accidental': 'flat',
                                                     'chord': None,
                                                     'duration': '1',
                                                     'pitch': {'alter': '-1',
                                                               'octave': '4',
                                                               'step': 'E'},
                                                     'staff': '3',
                                                     'type': 'quarter',
                                                     'voice': '1'},
                                                    {'accidental': 'sharp',
                                                     'duration': '2',
                                                     'pitch': {'alter': '1',
                                                               'octave': '4',
                                                               'step': 'C'},
                                                     'staff': '3',
                                                     'type': 'half',
                                                     'voice': '1'},
                                                    {'duration': '1',
                                                     'notations': {'tied': {'@type': 'start'}},
                                                     'pitch': {'octave': '4', 'step': 'D'},
                                                     'staff': '3',
                                                     'tie': {'@type': 'start'},
                                                     'type': 'quarter',
                                                     'voice': '1'},
                                                    {'accidental': 'natural',
                                                     'chord': None,
                                                     'duration': '1',
                                                     'notations': {'tied': {'@type': 'start'}},
                                                     'pitch': {'octave': '4', 'step': 'E'},
                                                     'staff': '3',
                                                     'tie': {'@type': 'start'},
                                                     'type': 'quarter',
                                                     'voice': '1'}]},
                                          {'@number': '2',
                                           'attributes': {'divisions': '1', 'staves': '3'},
                                           'backup': [{'duration': '4'}, {'duration': '4'}],
                                           'note': [{'duration': '2',
                                                     'notations': {'tied': {'@type': 'stop'}},
                                                     'pitch': {'octave': '4', 'step': 'D'},
                                                     'staff': '1',
                                                     'tie': {'@type': 'stop'},
                                                     'type': 'half',
                                                     'voice': '1'},
                                                    {'duration': '1',
                                                     'notations': {'tied': {'@type': 'stop'}},
                                                     'pitch': {'octave': '4', 'step': 'E'},
                                                     'staff': '2',
                                                     'tie': {'@type': 'stop'},
                                                     'type': 'quarter',
                                                     'voice': '1'},
                                                    {'duration': '1',
                                                     'pitch': {'octave': '4', 'step': 'F'},
                                                     'staff': '2',
                                                     'type': 'quarter',
                                                     'voice': '1'},
                                                    {'duration': '1',
                                                     'notations': {'tied': {'@type': 'stop'}},
                                                     'pitch': {'octave': '4', 'step': 'D'},
                                                     'staff': '3',
                                                     'tie': {'@type': 'stop'},
                                                     'type': 'quarter',
                                                     'voice': '1'},
                                                    {'chord': None,
                                                     'duration': '1',
                                                     'notations': {'tied': {'@type': 'stop'}},
                                                     'pitch': {'octave': '4', 'step': 'E'},
                                                     'staff': '3',
                                                     'tie': {'@type': 'stop'},
                                                     'type': 'quarter',
                                                     'voice': '1'},
                                                    {'duration': '1',
                                                     'pitch': {'octave': '4', 'step': 'F'},
                                                     'staff': '3',
                                                     'type': 'quarter',
                                                     'voice': '1'}]}]}}
