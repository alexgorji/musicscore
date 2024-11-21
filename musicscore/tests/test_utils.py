from pathlib import Path
from unittest import TestCase, skip

from musicscore import Chord
from musicscore.exceptions import WrongNumberOfChordsError
from musicscore.midi import C

from musicscore.score import Score
from musicscore.tests.util import diff_xml, _create_expected_path, create_test_objects
from musicscore.util import lcm, isinstance_as_string, XML_DYNAMIC_CLASSES, XML_ARTICULATION_CLASSES, \
    XML_ORNAMENT_CLASSES, XML_ORNAMENT_AND_OTHER_NOTATIONS, XML_TECHNICAL_CLASSES, XML_OTHER_NOTATIONS, \
    XML_DIRECTION_TYPE_CLASSES, XML_OTHER_NOTATIONS, XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS, slur_chords, split_list, wedge_chords, \
    trill_chords, bracket_chords, octave_chords
from musicxml import XMLTrillMark, XMLWavyLine, XMLOctaveShift


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

    def test_slur_chords(self):
        chords = [Chord(60, 1)]
        with self.assertRaises(WrongNumberOfChordsError):
            slur_chords(chords)
        chords.extend([Chord(61, 1), Chord(62, 1)])
        slur_chords(chords)
        assert chords[0].get_slurs()[0].type == 'start'
        assert chords[1].get_slurs()[0].type == 'continue'
        assert chords[2].get_slurs()[0].type == 'stop'

    def test_wedge_chords(self):
        chords = [Chord(60, 1)]
        with self.assertRaises(WrongNumberOfChordsError):
            wedge_chords(chords, 'crescendo')
        chords.extend([Chord(61, 1), Chord(62, 1)])
        wedge_chords(chords, 'crescendo')
        assert chords[0].get_wedges()[0].type == 'crescendo'
        assert chords[1].get_wedges()[0].type == 'continue'
        assert chords[2].get_wedges()[0].type == 'stop'

    def test_trill_chords(self):
        chords = [Chord(60, 1)]
        with self.assertRaises(WrongNumberOfChordsError):
            trill_chords(chords)
        chords.extend([Chord(61, 1), Chord(62, 1)])
        trill_chords(chords)
        assert len(chords[0].get_x(XMLTrillMark)) == 1
        assert len(chords[1].get_x(XMLTrillMark)) == 0
        assert len(chords[2].get_x(XMLTrillMark)) == 0
        assert chords[0].get_x(XMLWavyLine)[0].type == 'start'
        assert chords[1].get_x(XMLWavyLine)[0].type == 'continue'
        assert chords[2].get_x(XMLWavyLine)[0].type == 'stop'

    def test_bracket_chords(self):
        chords = [Chord(60, 1)]
        with self.assertRaises(WrongNumberOfChordsError):
            bracket_chords(chords)
        chords.extend([Chord(61, 1), Chord(62, 1)])
        bracket_chords(chords)
        assert chords[0].get_brackets()[0].type == 'start'
        assert chords[1].get_brackets()[0].type == 'continue'
        assert chords[2].get_brackets()[0].type == 'stop'

        for i, ch in enumerate(chords):
            bracket = ch.get_brackets()[0]
            assert bracket.line_type == 'solid'
            # assert bracket.placement == 'above'
            assert bracket.number == 1
            if i == 0:
                assert bracket.line_end == 'down'
            elif i == 1:
                assert bracket.line_end == 'none'
            else:
                assert bracket.line_end == 'down'

        chords = [Chord(60, 1) for _ in range(3)]
        bracket_chords(chords, 'dashed', 'none', 'up', placement='below', number=2)
        for i, ch in enumerate(chords):
            bracket = ch.get_brackets()[0]
            # assert bracket.placement == 'below'
            assert bracket.number == 2
            assert bracket.line_type == 'dashed'
            if i == 0:
                assert bracket.line_end == 'none'
            elif i == 1:
                assert bracket.line_end == 'none'
            else:
                assert bracket.line_end == 'up'

    def test_octave_chords(self):
        chords = [Chord(60, 1) for _ in range(3)]
        octave_chords(chords)
        assert chords[0].get_x(XMLOctaveShift)[0].type == 'down'
        assert chords[1].get_x(XMLOctaveShift)[0].type == 'continue'
        assert chords[2].get_x(XMLOctaveShift)[0].type == 'stop'

        chords = [Chord(60, 1) for _ in range(3)]
        octave_chords(chords, type='down', size=15, number=2)
        assert chords[0].get_x(XMLOctaveShift)[0].type == 'down'
        assert chords[1].get_x(XMLOctaveShift)[0].type == 'continue'
        assert chords[2].get_x(XMLOctaveShift)[0].type == 'stop'
        for ch in chords:
            assert ch.get_x(XMLOctaveShift)[0].size == 15
            assert ch.get_x(XMLOctaveShift)[0].number == 2

    def test_split_list(self):
        original_list = [1, 2, 3, 4, 5, 6]
        split_indices = [2, 5]
        self.assertListEqual(split_list(original_list, split_indices), [[1, 2], [3, 4, 5], [6]])

class TestTestObjects(TestCase):

    def test_direction_type_test_objects(self):
        test_object = create_test_objects(type='direction_type')
        assert len(XML_DIRECTION_TYPE_CLASSES + XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS) == len(test_object)
        for obj in test_object:
            assert obj.__class__ in XML_DIRECTION_TYPE_CLASSES or obj.__class__ in XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS

    def test_ornament_test_objects(self):
        test_object = create_test_objects(type='ornament')
        assert len(XML_ORNAMENT_CLASSES + XML_ORNAMENT_AND_OTHER_NOTATIONS) == len(test_object)
        for obj in test_object:
            assert obj.__class__ in XML_ORNAMENT_CLASSES + XML_ORNAMENT_AND_OTHER_NOTATIONS

    def test_technical_test_objects(self):
        test_object = create_test_objects(type='technical')
        assert len(XML_TECHNICAL_CLASSES) == len(test_object)
        for obj in test_object:
            assert obj.__class__ in XML_TECHNICAL_CLASSES

    def test_articulation_test_objects(self):
        test_object = create_test_objects(type='articulation')
        assert len(XML_ARTICULATION_CLASSES) == len(test_object)
        for obj in test_object:
            assert obj.__class__ in XML_ARTICULATION_CLASSES

    def test_other_notation_test_objects(self):
        test_object = create_test_objects(type='notation')
        assert len(XML_OTHER_NOTATIONS + XML_ORNAMENT_AND_OTHER_NOTATIONS) == len(test_object)
        for obj in test_object:
            assert obj.__class__ in XML_OTHER_NOTATIONS + XML_ORNAMENT_AND_OTHER_NOTATIONS

    def test_dynamics_test_objects(self):
        test_object = create_test_objects(type='dynamics')
        assert len(XML_DYNAMIC_CLASSES) == len(test_object)
        for obj in test_object:
            assert obj.__class__ in XML_DYNAMIC_CLASSES

