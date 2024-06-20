import math
import xml.etree.ElementTree as ET
from pathlib import Path

import xmltodict

from musicscore import Time, SimpleFormat, BassClef, TrebleClef
from musicscore.chord import Chord
from musicscore.exceptions import IdHasAlreadyParentOfSameTypeError, IdWithSameValueExistsError
from musicscore.key import Key
from musicscore.measure import Measure
from musicscore.part import Part, ScorePart, Id
from musicscore.quarterduration import QuarterDuration
from musicscore.score import Score
from musicscore.tests.test_metronome import TestCase
from musicscore.tests.util import get_xml_elements_diff, XMLsDifferException, get_xml_diff_part, \
    generate_xml_file, create_test_xml_paths

path = Path(__file__)


class TestId(TestCase):

    def test_id_refs(self):
        id1 = Id('p1')
        id2 = Id('p2')
        assert Id.__refs__ == [id1, id2]
        id3 = Id('p3')
        assert Id.__refs__ == [id1, id2, id3]
        id3.delete()
        assert Id.__refs__ == [id1, id2]
        Id('p3')

    def test_id_unique(self):
        Id('p1')
        id2 = Id('p2')
        with self.assertRaises(IdWithSameValueExistsError):
            Id('p1')
        id3 = Id('p3')
        with self.assertRaises(IdWithSameValueExistsError):
            Id('p2')
        with self.assertRaises(IdWithSameValueExistsError):
            id3.value = 'p2'
        assert id3.value == 'p3'
        id2.delete()
        id3.value = 'p2'
        assert id3.value == 'p2'

    def test_id_parents(self):
        id_ = Id('p1')
        assert id_.get_parents() == []
        p = Part(id=id_)
        assert id_.get_parents() == [p, p.score_part]
        with self.assertRaises(IdHasAlreadyParentOfSameTypeError):
            Part(id=id_)
        with self.assertRaises(IdHasAlreadyParentOfSameTypeError):
            ScorePart(part=p)
        assert p.xml_object.id == p.score_part.xml_object.id == 'p1'
        id_.value = 'p2'
        assert p.xml_object.id == p.score_part.xml_object.id == 'p2'
        p.id_ = 'p3'
        assert p.xml_object.id == p.score_part.xml_object.id == 'p3'


class TestPart(TestCase):
    def test_part_init(self):
        p = Part(id='p1')
        p.add_child(Measure(1))
        assert p.xml_object.id == 'p1'

    def test_part_name(self):
        p = Part(id='p1')
        assert p.name == ''
        p = Part(id='p2', name='Part 1')
        assert p.name == 'Part 1'
        p.name = None
        assert p.name == ''

    def test_part_abbreviation(self):
        p = Part(id='p1')
        assert p.abbreviation is None
        p = Part(id='p2', name='Part 1', abbreviation='p 1')
        assert p.abbreviation == 'p 1'
        p = Part(id='p3', name='Part 3')
        p.abbreviation = 'p 3'
        assert p.abbreviation == 'p 3'

    def test_part_and_score_part(self):
        p = Part(id='p1')
        assert isinstance(p.score_part, ScorePart)
        assert p.score_part.xml_object.id == p.xml_object.id

    def test_part_list_multiple_parts(self):
        score = Score()
        score.add_part('p1')
        score.add_part('p2')
        score.finalize()
        assert len(score.xml_object.xml_part_list.get_children()) == 2

    def test_add_measure(self):
        p = Part('p1')
        m = p.add_measure()
        assert p.get_children()[-1] == m
        assert m.number == 1
        assert m.time.signatures == (4, 4)
        m = p.add_measure(time=(4, 3, 2, 1))
        assert p.get_children()[-1] == m
        assert m.number == 2
        assert m.time.signatures == (4, 3, 2, 1)
        m = p.add_measure()
        assert p.get_children()[-1] == m
        assert m.number == 3
        assert m.time.signatures == (4, 3, 2, 1)

    def test_add_measure_show_time(self):
        p = Part('p1')
        m = p.add_measure()
        assert m.time.show is True
        m = p.add_measure()
        assert m.time.show is False
        m = p.add_measure(time=(3, 4))
        assert m.time.show is True

    def test_add_measure_show_key(self):
        p = Part('p1')
        m = p.add_measure()
        assert m.key.show is True
        m.finalize()
        assert m.xml_object.xml_attributes.xml_key is not None
        m = p.add_measure()
        m.finalize()
        assert m.key.show is False
        m.key = Key(fifths=1)
        assert m.key.show is True
        m = p.add_measure()
        m.finalize()
        assert m.key.fifths == 1
        assert m.key.show is False
        assert m.xml_object.xml_attributes.xml_key is None

    def test_add_measure_show_clefs(self):
        p = Part('p1')
        m = p.add_measure()
        m.add_staff(1)
        m.add_staff(2)
        assert m.clefs[0].show is True
        assert m.clefs[1].show is True
        m = p.add_measure()
        assert m.clefs[0].show is False
        assert m.clefs[1].show is False
        m = p.add_measure()
        m.clefs[0].show = True
        m.finalize()
        clefs = m.xml_object.xml_attributes.find_children('XMLClef')
        assert len(clefs) == 1
        assert clefs[0].xml_sign.value_ == 'G'
        assert clefs[0].xml_line.value_ == 2

    def test_part_add_measure_check_voice(self):
        """
        Test if Part.add_measure() adds a Measure with a Staff (number=None) and Voice (number=1)
        """
        p = Part('p1')
        m1 = p.add_measure()
        assert m1.get_staff(1) is not None
        assert m1.get_voice(staff_number=1, voice_number=1) is not None
        m1.add_staff(2)
        m2 = p.add_measure()
        m2.add_voice(staff_number=2, voice_number=2)

        assert m1.get_voice(staff_number=2, voice_number=2) is None
        assert m2.get_voice(staff_number=2, voice_number=2) is not None

    def test_part_set_current_measure(self):
        p = Part('p1')
        m1 = Measure(1)
        p.set_current_measure(1, 1, m1)
        assert p.get_current_measure(1, 1) == m1
        m2 = Measure(2)
        p.set_current_measure(1, 1, m2)
        assert p.get_current_measure(1, 1) == m2
        assert p.get_current_measure(1, 2) is None

        p = Part('p2')
        m1 = Measure(1)
        p.set_current_measure(None, 1, m1)
        assert p.get_current_measure(1, 1) == m1
        m2 = Measure(2)
        p.set_current_measure(1, 1, m2)
        assert p.get_current_measure(1, 1) == m2

    def test_part_get_current_measure_simple(self):
        p = Part('p1')
        m1 = p.add_measure()
        assert p.get_current_measure(staff_number=1, voice_number=1) == m1
        m2 = p.add_measure()
        m1._add_chord(Chord(midis=60, quarter_duration=2))
        assert p.get_current_measure(staff_number=1, voice_number=1) == m1
        m1._add_chord(Chord(midis=60, quarter_duration=2))
        assert p.get_current_measure(staff_number=1, voice_number=1) == m1
        assert m1.get_voice(staff_number=1, voice_number=1).is_filled
        m2._add_chord(Chord(midis=60, quarter_duration=2))
        assert p.get_current_measure(staff_number=1, voice_number=1) == m2
        m3 = p.add_measure()
        m4 = p.add_measure()
        m4._add_chord(Chord(midis=60, quarter_duration=2))
        assert p.get_current_measure(staff_number=1, voice_number=1) == m4

    def test_part_get_current_measure_complex(self):
        p = Part('p1')
        assert p.get_current_measure(staff_number=None, voice_number=1) is None
        m1 = p.add_measure()
        m1._add_chord(Chord(midis=60, quarter_duration=4), staff_number=2, voice_number=2)
        assert p.get_current_measure(staff_number=1, voice_number=1) == m1
        assert p.get_current_measure(staff_number=1, voice_number=2) is None
        assert p.get_current_measure(staff_number=2, voice_number=1) == m1
        assert p.get_current_measure(staff_number=2, voice_number=1).get_voice(staff_number=2,
                                                                               voice_number=1).is_filled is False
        assert p.get_current_measure(staff_number=2, voice_number=2) == m1
        assert p.get_current_measure(staff_number=2, voice_number=2).get_voice(staff_number=2,
                                                                               voice_number=2).is_filled is True
        m1.add_voice(staff_number=1, voice_number=1)
        assert p.get_current_measure(staff_number=1, voice_number=1) == m1
        #
        m2 = p.add_measure()
        m2._add_chord(Chord(midis=60, quarter_duration=4), staff_number=2, voice_number=2)

        assert p.get_current_measure(staff_number=1, voice_number=1) == m1
        assert p.get_current_measure(staff_number=1, voice_number=2) is None
        assert p.get_current_measure(staff_number=2, voice_number=1) == m1
        assert p.get_current_measure(staff_number=2, voice_number=2) == m2

        m1 = Measure(1)
        m1._add_chord(Chord(midis=60, quarter_duration=1))
        p = Part('p2')
        p.add_child(m1)
        assert p.get_current_measure(staff_number=1, voice_number=1) == m1


class TestScorePart(TestCase):

    def test_score_part_name(self):
        p = Part(id='p1')
        assert p.score_part.xml_part_name.value_ == p.name == ''
        p.name = 'Part 1'
        assert p.score_part.xml_part_name.value_ == p.name == 'Part 1'
        p.name = None
        assert p.score_part.xml_part_name.value_ == p.name == ''

    def test_score_part_abbreviation(self):
        p = Part(id='p1')
        assert p.score_part.xml_part_abbreviation == p.abbreviation is None
        p = Part(id='p2', name='Part 1', abbreviation='p 1')
        assert p.score_part.xml_part_abbreviation.value_ == p.abbreviation == 'p 1'
        p = Part(id='p3', name='Part 3')
        p.abbreviation = 'p 3'
        assert p.score_part.xml_part_abbreviation.value_ == p.abbreviation == 'p 3'

    def test_score_part_to_string(self):
        p = Part(id='p1')
        expected = """<score-part id="p1">
  <part-name />
</score-part>
"""
        assert p.score_part.to_string() == expected

    def test_add_measure_clef(self):
        p = Part('P1')
        m1 = p.add_measure(time=(3, 4))
        m2 = p.add_measure(time=(2, 4))
        p.finalize()
        assert m1.clefs[0].show is True
        assert m2.clefs[0].show is False

    def test_add_complex_quarter_durations(self):
        s = Score()
        p = s.add_child(Part('p1'))
        quarter_durations = [QuarterDuration(145, 42), QuarterDuration(1070, 737), QuarterDuration(1121, 352),
                             QuarterDuration(960, 589),
                             QuarterDuration(178, 85), QuarterDuration(134, 945), QuarterDuration(1733, 482),
                             QuarterDuration(446, 227),
                             QuarterDuration(458, 735), QuarterDuration(943, 890), QuarterDuration(650, 739),
                             QuarterDuration(939, 338),
                             QuarterDuration(327, 227), QuarterDuration(461, 183), QuarterDuration(1, 2),
                             QuarterDuration(1123, 457),
                             QuarterDuration(24, 59), QuarterDuration(1075, 397), QuarterDuration(604, 219),
                             QuarterDuration(18, 605),
                             QuarterDuration(2398, 999), QuarterDuration(235, 608), QuarterDuration(677, 799),
                             QuarterDuration(136, 637),
                             QuarterDuration(2717, 783), QuarterDuration(5, 643)]
        # first_qd = math.ceil(sum(quarter_durations[:4])) - sum(quarter_durations[:4])
        # qds = [first_qd] + [quarter_durations[4]]
        # last_qd = math.ceil(sum(qds)) - sum(qds)
        # qds += [last_qd]
        # qds = quarter_durations[:5]
        # last_qd = math.ceil(sum(qds)) - sum(qds)
        # qds += [last_qd]
        # qds = [QuarterDuration(145, 42), QuarterDuration(1070, 737), QuarterDuration(1121, 352), QuarterDuration(960, 589),
        #        QuarterDuration(178, 85), QuarterDuration(32, 171)]
        # qds = qds[4:]
        # first_qd = math.ceil(sum(qds)) - sum(qds)
        # print(first_qd)
        # qds = [first_qd] + qds
        # print(qds)
        qds = [QuarterDuration(23, 32), QuarterDuration(178, 85), QuarterDuration(32, 171), QuarterDuration(1)]
        for qd in qds:
            p.add_chord(Chord(midis=60, quarter_duration=qd))
        expected = [QuarterDuration(23, 32), QuarterDuration(9, 32), QuarterDuration(1, 1),
                    QuarterDuration(139, 171), QuarterDuration(32, 171), QuarterDuration(1, 1)]

        assert [ch.quarter_duration for ch in p.get_chords()] == expected

        for beat in [b for m in p.get_children() for st in m.get_children() for v in st.get_children() for b in
                     v.get_children()]:
            beat.quantize_quarter_durations()
            beat._split_not_writable_chords()
        expected = [QuarterDuration(3, 7), QuarterDuration(2, 7), QuarterDuration(2, 7), QuarterDuration(1, 1),
                    QuarterDuration(4, 5), QuarterDuration(1, 5), QuarterDuration(1, 1)]
        assert [ch.quarter_duration for ch in p.get_chords()] == expected

    def test_chord_previous(self):
        p = Part('P1')
        for qd in [1, 2.5, 0.5]:
            p.add_chord(Chord(midis=60, quarter_duration=qd))

        for i in range(1, len(p.get_children())):
            current = p.get_children()[i]
            previous = p.get_children()[i - 1]
            assert current.previous == previous

    def test_chord_offsets(self):
        p = Part('P1')
        for qd in [1, 2.5, 0.5]:
            p.add_chord(Chord(midis=60, quarter_duration=qd))

        assert [ch.quarter_duration for ch in p.get_chords()] == [1, 2, 0.5, 0.5]
        assert [ch.offset for ch in p.get_chords()] == [0, 0, 0, 0.5]


class TestAddChordToPart(TestCase):
    def setUp(self):
        self.score = Score()
        super().setUp()

    @staticmethod
    def _get_clefs_of_measure(part, measure_number=1):
        return xmltodict.parse(part.get_children()[measure_number - 1].to_string())['measure']['attributes'].get('clef',
                                                                                                                 None)

    def test_add_one_chord_quarter_duration_4(self):
        xml_file = create_test_xml_paths(path, 'add_one_chord_quarter_duration_4')[0]
        p = self.score.add_part(id='part1')
        chord = Chord(60, 4)
        p.add_chord(chord)
        self.score.export_xml(xml_file)
        output_score = ET.parse(xml_file)
        output_part_xml = output_score.find('part')
        output_part_xml_dict = xmltodict.parse(ET.tostring(output_part_xml))
        expected = {'part': {'@id': 'part1', 'measure': {'@number': '1',
                                                         'attributes': {'divisions': '1', 'key': {'fifths': '0'},
                                                                        'time': {'beats': '4', 'beat-type': '4'},
                                                                        'clef': {'sign': 'G', 'line': '2'}},
                                                         'note': {'pitch': {'step': 'C', 'octave': '4'},
                                                                  'duration': '4', 'voice': '1', 'type': 'whole'},
                                                         'barline': {'@location': 'right',
                                                                     'bar-style': 'light-heavy'}}}}
        assert output_part_xml_dict == expected

    def test_add_chord_to_staff_with_bass_clef(self):
        part = Part(id='part-1')
        part.add_chord(Chord(midis=60, quarter_duration=4), staff_number=2)
        part.add_chord(Chord(midis=60, quarter_duration=4), staff_number=2)
        assert self._get_clefs_of_measure(part, 1)[1] == {'@number': '2', 'sign': 'F', 'line': '4'}
        assert self._get_clefs_of_measure(part, 2) is None

    def test_add_chord_to_both_staves(self):
        part = Part(id='part-1')
        part.add_chord(Chord(midis=60, quarter_duration=4), staff_number=1)
        part.add_chord(Chord(midis=60, quarter_duration=4), staff_number=2)
        part.add_chord(Chord(midis=60, quarter_duration=4), staff_number=1)
        part.add_chord(Chord(midis=60, quarter_duration=4), staff_number=2)
        assert self._get_clefs_of_measure(part, 1)[1] == {'@number': '2', 'sign': 'F', 'line': '4'}
        assert self._get_clefs_of_measure(part, 2) is None

    def test_add_chord_to_both_staves_other_order(self):
        part = Part(id='part-1')
        part.add_chord(Chord(midis=60, quarter_duration=4), staff_number=1)
        part.add_chord(Chord(midis=60, quarter_duration=4), staff_number=1)

        part.add_chord(Chord(midis=60, quarter_duration=4), staff_number=2)
        part.add_chord(Chord(midis=60, quarter_duration=4), staff_number=2)

        assert self._get_clefs_of_measure(part, 1)[1] == {'@number': '2', 'sign': 'F', 'line': '4'}
        assert self._get_clefs_of_measure(part, 2) is None

    def test_add_long_chord_to_staff_with_bass_clef(self):
        part = Part(id='part-1')
        part.add_chord(Chord(midis=60, quarter_duration=11), staff_number=2)
        assert self._get_clefs_of_measure(part, 1)[1] == {'@number': '2', 'sign': 'F', 'line': '4'}
        assert self._get_clefs_of_measure(part, 2) is None
        assert self._get_clefs_of_measure(part, 3) is None

    def test_different_long_chords_to_staff_with_bass_clef(self):
        part = Part(id='part-1')
        midis = list(range(60, 65))
        quarter_durations = list(range(1, 6))
        for m, q in zip(midis, quarter_durations):
            part.add_chord(Chord(m, q), staff_number=2)
        assert self._get_clefs_of_measure(part, 1)[1] == {'@number': '2', 'sign': 'F', 'line': '4'}
        for measure_number in range(2, math.ceil(sum(quarter_durations) / 4)):
            assert self._get_clefs_of_measure(part, measure_number) is None

    def test_add_chord_to_two_staves_same_length(self):
        part = Part(id='part-1')
        midis = list(range(60, 65))
        quarter_durations = list(range(1, 6))
        for m, q in zip(midis, quarter_durations):
            part.add_chord(Chord(m, q), staff_number=1)
        for m, q in zip(reversed(midis), reversed(quarter_durations)):
            part.add_chord(Chord(m, q), staff_number=2)
        assert self._get_clefs_of_measure(part, 1)[1] == {'@number': '2', 'sign': 'F', 'line': '4'}
        for measure_number in range(2, math.ceil(sum(quarter_durations) / 4)):
            assert self._get_clefs_of_measure(part, measure_number) is None

    def test_add_chord_different_staves_and_voices(self):
        p = Part('p1')
        p.add_chord(Chord(60, 1))
        m = p.get_children()[0]
        assert m.get_voice(staff_number=1, voice_number=1) is not None
        p.add_chord(Chord(61, 2), staff_number=2, voice_number=4)
        for i in range(1, 5):
            assert m.get_voice(staff_number=2, voice_number=i) is not None
        p.add_chord(Chord(62, 3), staff_number=1, voice_number=1)
        assert [ch.quarter_duration for ch in m.get_voice(staff_number=1, voice_number=1).get_chords()] == [1, 3]
        assert [ch.midis[0].value for ch in m.get_voice(staff_number=1, voice_number=1).get_chords()] == [60, 62]
        assert [ch.quarter_duration for ch in m.get_voice(staff_number=2, voice_number=4).get_chords()] == [2]

    def test_add_chord_with_leftover(self):
        p = Part('p1')
        ch = Chord(60, 5)
        p.add_chord(ch)
        assert len(p.get_children()) == 2
        m1, m2 = p.get_children()
        assert p.get_current_measure(1, 1) == m2
        assert m1.get_voice(staff_number=1, voice_number=1).is_filled
        assert not m2.get_voice(staff_number=1, voice_number=1).is_filled

    def test_add_chord_to_full_measure(self):
        p = Part('p1')
        p.add_chord(Chord(60, 4))
        p.add_chord(Chord(60, 6))
        m1, m2, m3 = p.get_children()
        assert p.get_current_measure() == m3

    def test_add_chord_to_existing_measures(self):
        p = Part('p1')
        for _ in range(3):
            p.add_measure()
        m1, m2, m3 = p.get_children()
        assert p.get_current_measure() == m1
        p.add_chord(Chord(60, 5))
        assert p.get_current_measure() == m2

    def test_add_chord_with_staff_number(self):
        p = Part('P1')
        ch1 = Chord(60, 1)
        ch2 = Chord(48, 1)
        p.add_chord(ch1, staff_number=1)
        assert ch1.get_staff_number() is None
        p.add_chord(ch2, staff_number=2)
        assert ch1.get_staff_number() == 1
        assert ch2.get_staff_number() == 2
        p.finalize()
        assert ch1.notes[0].xml_staff.value_ == 1
        assert ch2.notes[0].xml_staff.value_ == 2

    def test_add_chord_with_clef(self):
        xml_path, expected_path = create_test_xml_paths(path, 'add_chord_with_clef')
        sf1 = SimpleFormat(midis=[60, (61, 66), 62], quarter_durations=[1, 2, 3])
        sf2 = SimpleFormat(midis=[60, (61, 66), 62], quarter_durations=[1, 2, 3])
        sf1.chords[1].clef = BassClef()

        sf2.chords[1].clef = BassClef()
        sf2.chords[2].clef = TrebleClef()
        score = Score()
        part = score.add_part(id='part-1')
        for index, simpleformat in enumerate([sf1, sf2]):
            for chord in simpleformat.chords:
                part.add_chord(chord, staff_number=index + 1)
        part.get_staff(1, 2).clef = TrebleClef()
        score.export_xml(xml_path)

        get_xml_diff_part(expected_path, xml_path, Path(__file__))

    def test_add_first_chord_with_clef(self):
        xml_path, expected_path = create_test_xml_paths(path, 'add_first_chord_with_clef')
        sf1 = SimpleFormat(midis=[60, (61, 66), 62], quarter_durations=[2, 6, 4])
        sf1.chords[0].clef = BassClef()
        sf1.chords[2].clef = TrebleClef()
        generate_xml_file(Score(), sf1, path=xml_path)
        get_xml_diff_part(expected_path, xml_path, Path(__file__))


class TestSplitQdAndTime(TestCase):
    def test_part_add_split_original_ties_1(self):
        chord = Chord(midis=60, quarter_duration=10)
        p = Part('p1')
        p.add_measure((5, 4))
        p.add_chord(chord)
        for chord in p.get_chords():
            assert chord._original_starting_ties == [set()]

    def test_part_add_split_original_ties_2(self):
        chord = Chord(midis=[60, 62], quarter_duration=10)
        chord.midis[0].add_tie('start')
        chord.midis[1].add_tie('stop')
        p = Part('p1')
        p.add_measure((5, 4))
        p.add_chord(chord)
        for chord in p.get_chords():
            assert chord._original_starting_ties == [{'start'}, {'stop'}]

    def test_part_add_split_chord_5_3_4(self):
        chord = Chord(midis=60, quarter_duration=5)
        p = Part('p1')
        p.add_measure((3, 4))
        p.add_chord(chord)
        assert len(p.get_children()) == 2
        m = p.get_children()[-1]
        assert len(m.get_chords()) == 1
        ch = m.get_chords()[0]
        assert ch.quarter_duration == 2
        assert ch.all_midis_are_tied_to_previous
        assert not ch.all_midis_are_tied_to_next

    def test_part_add_split_chord_5_4_4(self):
        chord = Chord(midis=60, quarter_duration=5)
        p = Part('p1')
        p.add_measure((4, 4))
        p.add_chord(chord)
        assert len(p.get_children()) == 2
        m = p.get_children()[-1]
        assert len(m.get_chords()) == 1
        ch = m.get_chords()[0]
        assert ch.quarter_duration == 1
        assert ch.all_midis_are_tied_to_previous
        assert not ch.all_midis_are_tied_to_next

    def test_part_add_split_chord_5_5_4(self):
        chord = Chord(midis=60, quarter_duration=5)
        p = Part('p1')
        p.add_measure((5, 4))
        p.add_chord(chord)
        assert len(p.get_children()) == 1
        m = p.get_children()[-1]
        all_chords = [ch1, ch2] = m.get_chords()
        assert [ch.quarter_duration for ch in all_chords] == [3, 2]
        assert not ch1.all_midis_are_tied_to_previous
        assert ch1.all_midis_are_tied_to_next
        assert ch2.all_midis_are_tied_to_previous
        assert not ch2.all_midis_are_tied_to_next

    def test_part_add_split_chord_6_4_4(self):
        chord = Chord(midis=60, quarter_duration=6)
        p = Part('p1')
        p.add_measure((4, 4))
        p.add_chord(chord)
        assert len(p.get_children()) == 2
        m = p.get_children()[-1]
        assert len(m.get_chords()) == 1
        ch = m.get_chords()[0]
        assert ch.quarter_duration == 2
        assert ch.all_midis_are_tied_to_previous
        assert not ch.all_midis_are_tied_to_next

    def test_part_add_split_chord_6_5_4(self):
        chord = Chord(midis=60, quarter_duration=6)
        p = Part('p1')
        p.add_measure((5, 4))
        p.add_chord(chord)
        assert len(p.get_children()) == 2
        m = p.get_children()[-1]
        assert len(m.get_chords()) == 1
        ch = m.get_chords()[0]
        assert ch.quarter_duration == 1
        assert ch.all_midis_are_tied_to_previous
        assert not ch.all_midis_are_tied_to_next

    def test_part_add_split_chord_7_7_4(self):
        chord = Chord(midis=60, quarter_duration=7)
        p = Part('p1')
        p.add_measure((7, 4))
        p.add_chord(chord)
        assert len(p.get_children()) == 1
        m = p.get_children()[-1]
        all_chords = [ch1, ch2] = m.get_chords()
        assert [ch.quarter_duration for ch in all_chords] == [4, 3]
        assert not ch1.all_midis_are_tied_to_previous
        assert ch1.all_midis_are_tied_to_next
        assert ch2.all_midis_are_tied_to_previous
        assert not ch2.all_midis_are_tied_to_next

    def test_part_add_split_chord_10_7_4(self):
        chord = Chord(midis=60, quarter_duration=10)
        p = Part('p1')
        p.add_measure((7, 4))
        p.add_chord(chord)
        assert len(p.get_children()) == 2
        m = p.get_children()[-1]
        assert len(m.get_chords()) == 1
        ch = m.get_chords()[0]
        assert ch.quarter_duration == 3
        assert ch.all_midis_are_tied_to_previous
        assert not ch.all_midis_are_tied_to_next

    def test_part_add_split_chord_12_7_4(self):
        chord = Chord(midis=60, quarter_duration=12)
        p = Part('p1')
        p.add_measure((7, 4))
        p.add_chord(chord)
        assert len(p.get_children()) == 2
        m = p.get_children()[-1]
        all_chords = [ch1, ch2] = m.get_chords()
        assert [ch.quarter_duration for ch in all_chords] == [3, 2]
        assert ch1.all_midis_are_tied_to_previous
        assert ch1.all_midis_are_tied_to_next
        assert ch2.all_midis_are_tied_to_previous
        assert not ch2.all_midis_are_tied_to_next

    def test_part_add_split_chord_10_5_4(self):
        chord = Chord(midis=60, quarter_duration=10)
        p = Part('p1')
        p.add_measure((5, 4))
        p.add_chord(chord)
        assert len(p.get_children()) == 2
        m = p.get_children()[-1]
        all_chords = [ch1, ch2] = m.get_chords()
        assert [ch.quarter_duration for ch in all_chords] == [3, 2]
        assert ch1.all_midis_are_tied_to_next
        assert ch1.all_midis_are_tied_to_previous
        assert not ch2.all_midis_are_tied_to_next
        assert ch2.all_midis_are_tied_to_previous

    def test_part_add_split_chord_10_10_4(self):
        chord = Chord(midis=60, quarter_duration=10)
        p = Part('p2')
        p.add_measure((10, 4))
        p.add_chord(chord)
        assert len(p.get_children()) == 1
        m = p.get_children()[-1]
        all_chords = [ch1, ch2, ch3] = m.get_chords()
        assert [ch.quarter_duration for ch in all_chords] == [4, 4, 2]
        assert not ch1.all_midis_are_tied_to_previous
        assert ch1.all_midis_are_tied_to_next
        assert ch2.all_midis_are_tied_to_previous
        assert ch2.all_midis_are_tied_to_next
        assert ch3.all_midis_are_tied_to_previous
        assert not ch3.all_midis_are_tied_to_next

    def test_add_chords_with_partially_tied_notes(self):
        xml_path, expected_path = create_test_xml_paths(path, 'add_chords_with_partially_tied_notes')
        midis = [[60, 63], [61, 63], [62, 64], [62, 65]]
        quarter_durations = [1, 2, 2, 1]
        chords = [Chord(ms, qd) for ms, qd in zip(midis, quarter_durations)]
        chords[0].midis[1].add_tie('start')
        chords[1].midis[1].add_tie('stop')
        chords[2].midis[0].add_tie('start')
        chords[3].midis[0].add_tie('stop')
        p = Part(id='part-1')
        for chord in chords:
            p.add_chord(chord)
        score = Score()
        score.add_child(p)
        score.export_xml(xml_path)
        get_xml_diff_part(expected_path, xml_path, Path(__file__))

    def test_add_chords_with_partially_tied_notes_simplified(self):
        xml_path, expected_path = create_test_xml_paths(path, 'add_chords_with_partially_tied_notes_simplified')
        midis = [[62, 64], [62, 65]]
        quarter_durations = [3, 1]
        chords = [Chord(ms, qd) for ms, qd in zip(midis, quarter_durations)]
        chords[0].midis[0].add_tie('start')
        chords[1].midis[0].add_tie('stop')
        p = Part('part-1')
        p.add_measure(Time(2, 4))
        for chord in chords:
            p.add_chord(chord)
        score = Score()
        score.add_child(p)
        score.export_xml(xml_path)
        el1 = ET.parse(Path(__file__).parent / xml_path).getroot().find("part[@id='part-1']")
        el2 = ET.parse(Path(__file__).parent / expected_path).getroot().find("part[@id='part-1']")
        diff = get_xml_elements_diff(el1=el1, el2=el2)
        if diff:
            raise XMLsDifferException(diff)
