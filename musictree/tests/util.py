import itertools
from difflib import Differ
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

from musicxml.xmlelement.xmlelement import XMLBendAlter, XMLHoleClosed, XMLArrowDirection, XMLHarmonClosed
from quicktions import Fraction

from musictree.part import Id


def check_notes(notes, midi_values, quarter_durations):
    if len(notes) != len(midi_values) or len(notes) != len(quarter_durations):
        raise ValueError
    for n, m, qd in zip(notes, midi_values, quarter_durations):
        assert n.midi.value == m
        assert n.quarter_duration == qd



class IdTestCase(TestCase):
    def setUp(self):
        Id.__refs__.clear()


class ChordTestCase(TestCase):
    def setUp(self) -> None:
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


def generate_all_16ths():
    output = [tuple(4 * [Fraction(1, 4)])]
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 4), Fraction(3, 4)]))))
    return output


def generate_all_32nds():
    output = [tuple(8 * [Fraction(1, 8)])]
    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(2, 8)] + 6 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(2 * [Fraction(2, 8)] + 4 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(3 * [Fraction(2, 8)] + 2 * [Fraction(1, 8)]))))

    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(3, 8)] + 5 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(3, 8)] + 1 * [Fraction(2, 8)] + 3 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(3, 8)] + 2 * [Fraction(2, 8)] + 1 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(2 * [Fraction(3, 8)] + 2 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(2 * [Fraction(3, 8)] + 1 * [Fraction(2, 8)]))))

    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(4, 8)] + 4 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(4, 8)] + 1 * [Fraction(2, 8)] + 2 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(4, 8)] + 1 * [Fraction(3, 8)] + 1 * [Fraction(1, 8)]))))

    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(5, 8)] + 3 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(5, 8)] + 1 * [Fraction(2, 8)] + 1 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(5, 8)] + 1 * [Fraction(3, 8)]))))

    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(6, 8)] + 2 * [Fraction(1, 8)]))))

    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(7, 8)] + 1 * [Fraction(1, 8)]))))
    return output


def generate_all_quintuplets():
    output = [tuple(5 * [Fraction(1, 5)])]
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 5), Fraction(1, 5), Fraction(1, 5), Fraction(2, 5)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 5), Fraction(2, 5), Fraction(2, 5)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(2, 5), Fraction(3, 5)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 5), Fraction(4, 5)]))))
    return output


def generate_all_sextuplets():
    output = [tuple(6 * [Fraction(1, 6)])]
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(1, 6),
                                                             Fraction(2, 6)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 6), Fraction(1, 6), Fraction(2, 6),
                                                             Fraction(2, 6)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(3, 6)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 6), Fraction(2, 6), Fraction(3, 6)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 6), Fraction(1, 6), Fraction(4, 6)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 6), Fraction(5, 6)]))))
    return output


def generate_all_septuplets():
    output = [tuple(7 * [Fraction(1, 7)])]
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(1, 7),
                                                             Fraction(2, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(2, 7), Fraction(2, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(2, 7), Fraction(2, 7), Fraction(2, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(3, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(2, 7), Fraction(3, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(3, 7), Fraction(3, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(4, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(3, 7), Fraction(4, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(5, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(2, 7), Fraction(5, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(6, 7)]))))
    return output


def generate_all_triplets():
    output = [tuple(3 * [Fraction(1, 3)])]
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 3), Fraction(2, 3)]))))
    return output


def create_technical(class_):
    if class_.__name__ == 'XMLFingering':
        technical = class_('2')
    elif class_.__name__ == 'XMLPluck':
        technical = class_('something')
    elif class_.__name__ == 'XMLFret':
        technical = class_(2)
    elif class_.__name__ == 'XMLString':
        technical = class_(2)
    elif class_.__name__ == 'XMLHammerOn':
        technical = class_('2', type='start')
    elif class_.__name__ == 'XMLPullOff':
        technical = class_('2', type='start')
    elif class_.__name__ == 'XMLTap':
        technical = class_('2')
    elif class_.__name__ == 'XMLHandbell':
        technical = class_('damp')
    elif class_.__name__ == 'XMLHarmonClosed':
        technical = class_('yes')
    elif class_.__name__ == 'XMLOtherTechnical':
        technical = class_('bla')
    else:
        technical = class_()
    if class_.__name__ == 'XMLBend':
        technical.add_child(XMLBendAlter(2))
    elif class_.__name__ == 'XMLHole':
        technical.add_child(XMLHoleClosed('yes'))
    elif class_.__name__ == 'XMLArrow':
        technical.add_child(XMLArrowDirection('up'))
    elif class_.__name__ == 'XMLHarmonMute':
        technical.add_child(XMLHarmonClosed('yes'))

    return technical


def create_articulation(class_):
    if class_.__name__ == 'XMLBreathMark':
        articulation = class_('comma')
    elif class_.__name__ == 'XMLCaesura':
        articulation = class_('normal')
    else:
        articulation = class_()
    return articulation
