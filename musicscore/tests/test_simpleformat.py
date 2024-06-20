from pathlib import Path
from unittest import skip

from deepdiff import DeepDiff

from musicscore import Score, Midi, QuarterDuration, Chord, SimpleFormat, TrebleClef, SimpleFormatException
from musicscore.tests.util import IdTestCase, get_xml_diff_part, generate_xml_file, create_test_xml_paths
import xml.etree.ElementTree as ET

path = Path(__file__)


class TestSimpleFormat(IdTestCase):
    def setUp(self) -> None:
        self.score = Score()
        super().setUp()

    def get_diff_xml_file_elements(self, path_1, path_2, element_tag):
        if path_2 is None:
            path_2 = path_1.split('.')[0] + '_expected.xml'
        xml_element_1 = ET.parse(path_1).getroot().find(element_tag)
        xml_element_2 = ET.parse(path_2).getroot().find(element_tag)
        return DeepDiff(xml_element_1, xml_element_2)

    def _check_distinctive_quarter_durations_and_values(self, quarter_durations, sf):
        for qd in sf.get_quarter_durations():
            assert isinstance(qd, QuarterDuration)
        for output_qt, input_qt in zip(sf.get_quarter_durations(), quarter_durations):
            if isinstance(input_qt, QuarterDuration):
                assert id(output_qt) == id(input_qt)
        assert [qd.value for qd in sf.get_quarter_durations()] == quarter_durations
        assert len(set([id(qd) for qd in sf.get_quarter_durations()])) == len(quarter_durations)

    def _check_distinctive_midi_instances_and_values(self, midis, sf):
        # sf.midis are all of type Midi
        for midi_list in sf.midis:
            for midi in midi_list:
                assert isinstance(midi, Midi)

        # make sure that midis is a list of lists (like sf.midis)
        midis = [list(x) if hasattr(x, '__iter__') else [x] for x in midis]

        # each midi object is distinctive (no repetition of midi objects)
        assert len([id(midi) for midi_list in sf.midis for midi in midi_list]) == len(
            [m for midi_list in midis for m in midi_list])

        # if midi contains midi objects, these are passed on to sf.midis
        for output_midis, input_midis in zip(sf.get_midis(), midis):
            for output_midi, input_midi in zip(output_midis, input_midis):
                if isinstance(input_midi, Midi):
                    assert id(output_midi) == id(input_midi)

        # value of not midi objects in midis are the same as the value of their corresponding midi objects in sf.midis
        for m1, m2 in zip(sf.midis, midis):
            for x, z in zip(m1, m2):
                if not isinstance(z, Midi):
                    x.value = z

    def test_simple_format_init(self):
        SimpleFormat()

    def test_simple_format_init_with_numeral_parameters(self):
        quarter_durations = [1, 2, 3, 2, 1]
        midis = [60, (60, 62), (64, 66, 71), 72, 73]
        default_midi = 60

        sf = SimpleFormat(quarter_durations=quarter_durations, midis=midis, default_midi=default_midi)
        # // quarter_durations
        # distinctive QuarterDuration objects are created
        self._check_distinctive_quarter_durations_and_values(quarter_durations, sf)
        # // midis
        # distinctive Midi objects are created
        self._check_distinctive_midi_instances_and_values(midis, sf)
        # // default_midi
        assert sf.default_midi.value == default_midi

    def test_simple_format_init_with_object_parameters(self):
        quarter_durations = [QuarterDuration(1), QuarterDuration(2), QuarterDuration(3), QuarterDuration(2),
                             QuarterDuration(1)]
        midis = [Midi(60), (Midi(60), Midi(62)), (Midi(64), Midi(66), Midi(71)), Midi(72), Midi(73)]
        default_midi = Midi(60)

        sf = SimpleFormat(quarter_durations=quarter_durations, midis=midis, default_midi=default_midi)
        # // quarter_durations
        # SimpleFormat takes over the same QuarterDuration objects
        assert sf.get_quarter_durations() == quarter_durations
        # // midis
        # SimpleFormat take over the same Midi objects
        assert sf.midis == [list(midi) if hasattr(midi, '__iter__') else [midi] for midi in midis]
        # // default_midi
        # SimpleFormat take over the default_midi object
        assert sf.default_midi == default_midi

    def test_simple_format_init_with_mixed_parameters(self):
        quarter_durations = [1, 2, QuarterDuration(3), 2, QuarterDuration(1)]
        midis = [60, (Midi(60), Midi(62)), (64, 66, 71), Midi(72), 73]

        sf = SimpleFormat(quarter_durations=quarter_durations, midis=midis)
        # // quarter_durations
        # distinctive QuarterDuration objects are created or the same objects are passed on
        self._check_distinctive_quarter_durations_and_values(quarter_durations, sf)
        # // midis
        # distinctive Midi objects are created or the same objects are passed on
        self._check_distinctive_midi_instances_and_values(midis, sf)

    def test_simple_format_equalise_midi_quarter_duration_lengths(self):
        # no midis
        sf = SimpleFormat(quarter_durations=[1, 2, 3])
        assert [midi[0].value for midi in sf.midis] == [71] * 3

        # no quarter_durations
        sf = SimpleFormat(midis=[60, 61, 62])

        assert [qd.value for qd in sf.get_quarter_durations()] == [1] * 3
        # less midis
        sf = SimpleFormat(midis=[60, 61], quarter_durations=[1, 2, 3, 1])
        assert [midi[0].value for midi in sf.midis] == [60, 61, 71, 71]
        # default midis are distinctive
        assert id(sf.get_midis()[-1]) != id(sf.get_midis()[-2])
        # less quarter_durations
        sf = SimpleFormat(midis=[60, 61, 62, 60], quarter_durations=[1, 2])
        assert [qd.value for qd in sf.get_quarter_durations()] == [1, 2, 1, 1]
        # default quarter_durations are distinctive
        assert id(sf.get_quarter_durations()[-1]) != id(sf.get_quarter_durations()[-2])

    def test_simple_format_default_midi(self):
        # default value of default_midi is 71
        sf = SimpleFormat(quarter_durations=[1, 2, 3])
        assert [midi[0].value for midi in sf.midis] == [71, 71, 71]

        # default_midi can be set to a midi value
        sf = SimpleFormat(quarter_durations=[1, 2, 3], default_midi=60)
        # 3 distinctive Midi objects with correct values are created
        self._check_distinctive_midi_instances_and_values([60, 60, 60], sf)

        # default_midi can be set to a Midi object
        sf = SimpleFormat(quarter_durations=[1, 2, 3], default_midi=Midi(60))
        # three distinctive Midi objects are created
        self._check_distinctive_midi_instances_and_values([60, 60, 60], sf)

        assert sf.default_midi not in [midi[0] for midi in sf.midis]

        # // set default_midi after creation
        # default_midi can be set after creation to a midi value
        sf = SimpleFormat(quarter_durations=[1, 2, 3])
        sf.default_midi = 60
        self._check_distinctive_midi_instances_and_values([60, 60, 60], sf)
        # # default_midi can be set after creation to a Midi object
        sf = SimpleFormat(quarter_durations=[1, 2, 3])
        sf.default_midi = Midi(60)
        self._check_distinctive_midi_instances_and_values([60, 60, 60], sf)
        assert sf.default_midi not in [midi[0] for midi in sf.midis]

    def test_simple_format_chords(self):
        """
        Test midis to chords conversion
        """
        midis = [60, (60, 62), (64, 66, 71), 72, 73]
        sf = SimpleFormat(quarter_durations=[1, 1, 1, 1, 1], midis=midis)
        assert len(sf.chords) == len(midis)
        assert [[midi.value for midi in chord.midis] for chord in sf.chords] == [
            list(midi) if isinstance(midi, tuple) else [midi] for midi in midis]

    def test_add_chord(self):
        sf = SimpleFormat(quarter_durations=[1], midis=[60])
        chords = [Chord(midis, 1) for midis in [[61, 62], 63]]
        for chord in chords:
            sf.add_chord(chord)
        assert sf.chords[1:] == chords

    def test_get_quarter_positions(self):
        quarter_duration_values = [1, 2, 3, 4, 5]
        sf = SimpleFormat(quarter_duration_values)
        assert sf.get_quarter_positions() == [0, 1, 3, 6, 10, 15]

    def test_get_chord_at_position(self):
        quarter_duration_values = [1, 2, 3, 4]
        sf = SimpleFormat(quarter_duration_values)
        assert sf.get_chord_at_position(0) == sf.chords[0]
        assert sf.get_chord_at_position(0.5) == sf.chords[0]
        assert sf.get_chord_at_position(0.99) == sf.chords[0]
        assert sf.get_chord_at_position(1) == sf.chords[1]
        assert sf.get_chord_at_position(2) == sf.chords[1]
        assert sf.get_chord_at_position(2.99) == sf.chords[1]
        assert sf.get_chord_at_position(3) == sf.chords[2]
        assert sf.get_chord_at_position(5) == sf.chords[2]
        assert sf.get_chord_at_position(6) == sf.chords[3]
        assert sf.get_chord_at_position(8) == sf.chords[3]
        assert sf.get_chord_at_position(9.99) == sf.chords[3]
        assert sf.get_chord_at_position(10) is None
        assert sf.get_chord_at_position(14) is None

    @skip
    def test_auto_clef(self):
        self.fail()

    def test_change_chords(self):
        def transpose_chord(chord):
            for midi in chord.midis:
                midi.value += sf.chords.index(chord)

        sf = SimpleFormat(quarter_durations=[1, 1, 1, 1, 1], default_midi=60)
        sf.change_chords(transpose_chord)
        assert [[midi.value for midi in chord.midis] for chord in sf.chords] == [[60], [61], [62], [63], [64]]

    def test_extend(self):
        sf1 = SimpleFormat(midis=[60, 61, 62])
        sf2 = SimpleFormat(midis=[63, 64])
        sf1.extend(sf2)
        assert [[midi.value for midi in chord.midis] for chord in sf1.chords] == [[60], [61], [62], [63], [64]]

    def test_mirror(self):
        sf = SimpleFormat(midis=[60, 61, 62, 64, 67])
        sf.mirror(pivot=63)
        assert [[midi.value for midi in chord.midis] for chord in sf.chords] == [[66], [65], [64], [62], [59]]

    def test_multiply_quarter_durations(self):
        sf = SimpleFormat(quarter_durations=[1, 2, 3])
        sf.multiply_quarter_durations(2)
        assert [qd.value for qd in sf.get_quarter_durations()] == [2, 4, 6]

    def test_retrograde(self):
        sf = SimpleFormat(quarter_durations=[1, 2, 3], midis=[60, 61, 62])
        sf.retrograde()
        assert [qd.value for qd in sf.get_quarter_durations()] == [3, 2, 1]
        assert [[midi.value for midi in chord.midis] for chord in sf.chords] == [[62], [61], [60]]

    def test_sum_1(self):
        xml_path, expected_path = create_test_xml_paths(path, 'sum_1')
        sf1 = SimpleFormat(quarter_durations=[1, 2, 3], midis=[60, 61, 62])
        sf2 = SimpleFormat(quarter_durations=[3, 2, 1], midis=[63, 64, 65])
        sf = SimpleFormat.sum(sf1, sf2)
        generate_xml_file(self.score, sf1, sf2, sf, path=xml_path)
        get_xml_diff_part(expected_path, xml_path, Path(__file__))

    def test_sum_2(self):
        xml_path, expected_path = create_test_xml_paths(path, 'sum_2')
        sf1 = SimpleFormat(quarter_durations=[1, 2, 3], midis=[60, 61, 62])
        sf2 = SimpleFormat(quarter_durations=[1, 3, 2], midis=[(60, 65), 67, (50, 54)])
        sf = SimpleFormat.sum(sf1, sf2)
        generate_xml_file(self.score, sf1, sf2, sf, path=xml_path)
        get_xml_diff_part(expected_path, xml_path, Path(__file__))

    def test_sum_3(self):
        xml_path, expected_path = create_test_xml_paths(path, 'sum_3')
        sf1 = SimpleFormat(quarter_durations=[1, 2, 3, 6], midis=[60, 61, 62, 0])
        sf2 = SimpleFormat(quarter_durations=[1, 3, 2, 6], midis=[(60, 65), 67, (50, 54), 0])
        sf3 = SimpleFormat(quarter_durations=[3, 4, 5], midis=[69, 68, 67])
        sf = SimpleFormat.sum(sf1, sf2, sf3)
        part = self.score.add_part(id='part-1')
        for index, simpleformat in enumerate([sf1, sf2, sf3, sf]):
            for chord in simpleformat.chords:
                part.add_chord(chord, staff_number=index + 1)
        part.get_staff(1, 3).clef = TrebleClef()
        part.get_staff(1, 4).clef = TrebleClef()
        self.score.export_xml(xml_path)
        get_xml_diff_part(expected_path, xml_path, Path(__file__))

    def test_complex_sum(self):
        xml_path, expected_path = create_test_xml_paths(path, 'complex_sum')
        sf1 = SimpleFormat(quarter_durations=[1, 2, 3, 2, 1], midis=[60, (60, 62), (64, 66, 71), 72, 73])
        sf2 = SimpleFormat(quarter_durations=[0.5, 1, 1.5, 2, 3, 1], midis=[0, 69, (72, 73), (58, 60, 65, 71), 80, 0])
        sf = SimpleFormat.sum(sf1, sf2)
        generate_xml_file(self.score, sf1, sf2, sf, path=xml_path)
        get_xml_diff_part(expected_path, xml_path, Path(__file__))

    def test_sum_of_tied_chords(self):
        # path = Path(__file__).stem + '_sum_of_tied_chords.xml'
        # expected = Path(__file__).stem + '_sum_of_tied_chords_expected.xml'
        sf1 = SimpleFormat(quarter_durations=[1, 2, 3], midis=[[60, 63], [60, 61], 62])
        sf2 = SimpleFormat(quarter_durations=[3, 2, 1], midis=[63, 64, 65])
        # sum1 = SimpleFormat.sum(sf1, sf2)

        sf2.chords[0].add_tie('start')
        sf2.chords[1].add_tie('start')
        sf2.chords[2].add_tie('start')
        with self.assertRaises(SimpleFormatException):
            SimpleFormat.sum(sf1, sf2)
        # self.generate_xml_file(sf1, sf2, sum1, sum2, path=path)
        # get_xml_diff_part(expected, path)

    def test_sum_without_duplicates_1(self):
        xml_path, expected_path = create_test_xml_paths(path, 'sum_without_duplicates_1')
        sf1 = SimpleFormat(quarter_durations=[1, 2, 3], midis=[60, (61, 67), 62])
        sf2 = SimpleFormat(quarter_durations=[1, 3, 2], midis=[(60, 65), 67, (70, 62, 65)])
        sum1 = SimpleFormat.sum(sf1, sf2)
        sum2 = SimpleFormat.sum(sf1, sf2, no_duplicates=True)
        generate_xml_file(self.score, sf1, sf2, sum1, sum2, path=xml_path)
        get_xml_diff_part(xml_path, xml_path, Path(__file__))

    def test_sum_without_duplicates_2(self):
        xml_path, expected_path = create_test_xml_paths(path, 'sum_without_duplicates_2')
        sf1 = SimpleFormat(quarter_durations=[1, 2, 3], midis=[60, (61, 66), 62])
        sf2 = SimpleFormat(quarter_durations=[1, 3, 2], midis=[(60, 65), 66, (70, 62, 65)])
        sf1.chords[1].midis[1].accidental.mode = 'flat'
        sf2.chords[1].midis[0].accidental.mode = 'sharp'
        sum1 = SimpleFormat.sum(sf1, sf2)
        sum2 = SimpleFormat.sum(sf1, sf2, no_duplicates=True)
        generate_xml_file(self.score, sf1, sf2, sum1, sum2, path=xml_path)
        get_xml_diff_part(expected_path, xml_path, Path(__file__))

    def test_sum_different_simple_format_lengths_exception(self):
        sf1 = SimpleFormat(quarter_durations=[3, 2, 3], midis=[65, 64, 63])
        sf2 = SimpleFormat(quarter_durations=[3, 2, 1], midis=[63, 64, 65])
        with self.assertRaises(SimpleFormatException):
            SimpleFormat.sum(sf1, sf2)
