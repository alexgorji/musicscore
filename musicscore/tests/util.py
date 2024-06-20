import inspect
import xml.etree.ElementTree as ET
from difflib import Differ
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

import xmltodict
from deepdiff import DeepDiff

from musicscore import generate_measures, Chord, C
from musicscore.part import Id
from musicxml.xmlelement.xmlelement import *
from musicscore.util import XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS, XML_DIRECTION_TYPE_CLASSES, XML_OTHER_NOTATIONS, \
    XML_ORNAMENT_CLASSES, XML_ARTICULATION_CLASSES, XML_TECHNICAL_CLASSES, XML_DYNAMIC_CLASSES, \
    XML_ORNAMENT_AND_OTHER_NOTATIONS


class XMLsDifferException(Exception):
    pass


notehead_values = ['slash', 'triangle', 'diamond', 'square', 'rectangle', 'cross', 'x', 'circle dot', 'circle-x',
                   'circled', 'inverted triangle', 'left triangle', 'arrow down', 'arrow up', 'slashed',
                   'back slashed', 'normal', 'cluster', 'none']
notehead_aikin_values = ['do', 're', 'mi', 'fa', 'fa up', 'so', 'la', 'ti']


def check_notes(notes, midi_values, quarter_durations):
    if len(notes) != len(midi_values) or len(notes) != len(quarter_durations):
        raise ValueError
    for n, m, qd in zip(notes, midi_values, quarter_durations):
        assert n.midi.value == m
        assert n.quarter_duration == qd


class IdTestCase(TestCase):
    def setUp(self):
        Id.__refs__.clear()


class ChordTestCase(IdTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.mock_beat = Mock()
        self.mock_voice = Mock()
        self.mock_staff = Mock()
        self.mock_measure = Mock()

        self.mock_voice.number = 1
        self.mock_beat.up = self.mock_voice
        self.mock_voice.up = self.mock_staff
        self.mock_staff.up = self.mock_measure
        self.mock_measure.get_divisions.return_value = 1
        self.mock_staff.number = None

    def tearDown(self) -> None:
        patch.stopall()


def _create_expected_path(path):
    return Path(path.parent / f"{path.stem}_expected{path.suffix}")


def diff_xml(path_1, path_2=None):
    if path_2 is None:
        path_2 = _create_expected_path(path_1)

    with open(path_1) as f1, open(path_2) as f2:
        f_1 = [i.strip() for i in f1]
        f_2 = [i.strip() for i in f2]

    diff = Differ()
    difference = list(diff.compare(f_1, f_2))
    return [d for d in difference if d.startswith('-') or d.startswith('+')]


def get_xml_elements_diff(el1, el2):
    return DeepDiff(xmltodict.parse(ET.tostring(el1)), xmltodict.parse(ET.tostring(el2)))


def get_xml_diff_part(expected, xml_path, file_path):
    el1 = ET.parse(file_path.parent / xml_path).getroot().find("part[@id='part-1']")
    el2 = ET.parse(file_path.parent / expected).getroot().find("part[@id='part-1']")
    diff = get_xml_elements_diff(el1=el1, el2=el2)
    if diff:
        raise XMLsDifferException(diff)


def generate_xml_file(score, *simpleformats, path):
    part = score.add_part(id='part-1')
    for index, simpleformat in enumerate(simpleformats):
        for chord in simpleformat.chords:
            part.add_chord(chord, staff_number=index + 1)
    score.export_xml(path)


def generate_repetitions(part):
    for m in generate_measures([(3, 8), (3, 4)] + 2 * [(6, 4)] + 3 * [(4, 4)] + [(5, 4)]):
        part.add_child(m)

    for qd in 3 * [0.5] + 3 * [1] + 4 * [1.5] + 3 * [2] + [1, 1, 1, 2, 1, 1, 2, 2, 3, 3, 3, 4, 4, 2, 2, 1.5, 1.5,
                                                           3.25, 1.75, 1]:
        part.add_chord(Chord(C(5, '#'), qd))


def generate_path(frame):
    f = str(inspect.getframeinfo(frame).function) + '.xml'
    path = Path(inspect.getframeinfo(frame).filename).parent / f
    return path


def create_test_xml_paths(path, test_name):
    return path.parent.joinpath(f'{path.stem}_{test_name}.xml'), path.parent.joinpath(
        f'{path.stem}_{test_name}_expected.xml')


def create_test_objects(type):
    output = []
    if type == 'direction_type':
        for cl in XML_DIRECTION_TYPE_CLASSES + XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS:
            if cl == XMLSymbol:
                obj = cl('0')
            elif cl == XMLWedge:
                obj = cl(type='crescendo')
            elif cl == XMLDashes:
                obj = cl(type='start')
            elif cl == XMLBracket:
                obj = cl(type='start', line_end='none')
            elif cl == XMLPedal:
                obj = cl(type='start')
            elif cl == XMLMetronome:
                obj = cl()
                obj.add_child(XMLBeatUnit('quarter'))
                obj.add_child(XMLPerMinute('120'))
            elif cl == XMLOctaveShift:
                obj = cl(type='up')
            elif cl == XMLHarpPedals:
                obj = cl()
                pt = obj.add_child(XMLPedalTuning())
                pt.add_child(XMLPedalStep('A'))
                pt.add_child(XMLPedalAlter(1))
            elif cl == XMLStringMute:
                obj = cl(type='on')
            elif cl == XMLScordatura:
                obj = cl()
                acc = obj.add_child(XMLAccord())
                acc.add_child(XMLTuningStep('A'))
                acc.add_child(XMLTuningOctave(0))
            # elif cl == XMLImage:
            #     obj = cl(source='www.example.com', type='image/gif')
            elif cl == XMLPrincipalVoice:
                obj = cl(type='start', symbol='none')
            elif cl == XMLPercussion:
                obj = cl()
                obj.add_child(XMLWood('cabasa'))
            elif cl == XMLStaffDivide:
                obj = cl(type='up')
            else:
                obj = cl()
            output.append(obj)

    elif type == 'technical':
        needed_values = {XMLFret: 1, XMLString: 1, XMLHandbell: 'belltree', XMLFingering: '2', XMLPluck: 'something',
                         XMLTap: '2', XMLHarmonClosed: 'yes', XMLOtherTechnical: 'something'}
        needed_types = {XMLHammerOn: 'start', XMLPullOff: 'start'}
        needed_children = {XMLBend: XMLBendAlter(2), XMLHole: XMLHoleClosed('yes'), XMLArrow: XMLArrowDirection('up'),
                           XMLHarmonMute: XMLHarmonClosed('yes')}
        for cl in XML_TECHNICAL_CLASSES:
            if cl in needed_children:
                obj = cl()
                obj.add_child(needed_children[cl])
            elif cl in needed_types:
                obj = cl(type=needed_types[cl])
            elif cl in needed_values:
                obj = cl(needed_values[cl])
            else:
                obj = cl()
            output.append(obj)

    elif type == 'ornament':
        for cl in XML_ORNAMENT_AND_OTHER_NOTATIONS + XML_ORNAMENT_CLASSES:
            if cl == XMLAccidentalMark:
                obj = cl('sharp')
            elif cl == XMLTremolo:
                obj = cl(3)
            else:
                obj = cl()
            output.append(obj)

    elif type == 'notation':
        for cl in XML_OTHER_NOTATIONS + XML_ORNAMENT_AND_OTHER_NOTATIONS:
            if cl == XMLAccidentalMark:
                obj = cl('sharp')
            else:
                obj = cl()
            output.append(obj)

    elif type == 'articulation':
        for cl in XML_ARTICULATION_CLASSES:
            obj = cl()
            output.append(obj)
    elif type == 'dynamics':
        for cl in XML_DYNAMIC_CLASSES:
            obj = cl()
            output.append(obj)
    else:
        raise NotImplementedError(f"type {type}")
    return output


def _generate_xml_lyric(text=None, number=1, syllabic=None, extend=None, **kwargs):
    xl = XMLLyric(number=str(number), **kwargs)
    xl.xml_text = text
    xl.xml_syllabic = syllabic
    if extend:
        xl.xml_extend = XMLExtend(type=extend)
    return xl
