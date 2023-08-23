from pathlib import Path
from unittest import TestCase, skip

from musictree import Score, Midi, QuarterDuration, Chord, SimpleFormat


class Test(TestCase):
    def setUp(self) -> None:
        self.score = Score()

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
        chords = [Chord(midis=midis) for midis in [[61, 62], 63]]
        for chord in chords:
            sf.add_chord(chord)
        assert sf.chords[1:] == chords

    def test_get_quarter_positions(self):
        quarter_duration_values = [1, 2, 3, 4, 5]
        sf = SimpleFormat(quarter_duration_values)
        assert sf.get_quarter_positions() == [0, 1, 3, 6, 10, 15]

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

    def test_sum(self):
        sf1 = SimpleFormat(quarter_durations=[1, 2, 3], midis=[60, 61, 62])
        sf2 = SimpleFormat(quarter_durations=[1, 3, 2], midis=[(60, 65), 67, (50, 54)])
        sf3 = SimpleFormat(quarter_durations=[3, 4, 5], midis=[69, 68, 67])
        sf = SimpleFormat.sum(sf1, sf2, sf3)

    def test_retrograde(self):
        sf = SimpleFormat(quarter_durations=[1, 2, 3], midis=[60, 61, 62])
        sf.retrograde()
        assert [qd.value for qd in sf.get_quarter_durations()] == [3, 2, 1]
        assert [[midi.value for midi in chord.midis] for chord in sf.chords] == [[62], [61], [60]]

    def test_complex_sum(self):
        xml_file = Path(__file__).stem + '_add_to_score.xml'
        sf_1 = SimpleFormat(quarter_durations=[1, 2, 3, 2, 1], midis=[60, (60, 62), (64, 66, 71), 72, 73])
        part = self.score.add_part(id_='part1')
        for chord in sf_1.chords:
            part.add_chord(chord=chord, staff_number=1)
        sf_2 = SimpleFormat(quarter_durations=[0.5, 1, 1.5, 2, 3], midis=[0, 69, (72, 73), (58, 60, 65, 71), 80])
        for chord in sf_2.chords:
            part.add_chord(chord=chord, staff_number=2)
        sf_3 = SimpleFormat.sum(sf_1, sf_2)
        for chord in sf_3.chords:
            part.add_chord(chord=chord, staff_number=3)
        self.score.export_xml(xml_file)
    #
    # def test_2(self):
    #     xml_path = path + '_test_2.xml'
    #     sf_1 = SimpleFormat(quarter_durations=[1, 2, 3, 2, 1], midis=[60, (60, 62), (64, 66, 71), 72, 73])
    #     sf_1.to_stream_voice().add_to_score(self.score)
    #     sf_2 = SimpleFormat(quarter_durations=[0.5, 1, 1.5, 2, 3], midis=[0, 69, (72, 73), (58, 60, 65, 71), 80])
    #     sf_2.to_stream_voice().add_to_score(self.score, staff_number=2)
    #     sf_3 = SimpleFormat.sum(sf_1, sf_2, no_doubles=True)
    #     sf_3.to_stream_voice().add_to_score(self.score, staff_number=3)
    #     self.score.write(xml_path)
    #     self.assertCompareFiles(xml_path)
    #
    # def test_3(self):
    #     xml_path = path + '_test_3.xml'
    #     sf_1 = SimpleFormat(quarter_durations=[1, 2, 3, 2, 1], midis=[60, (60, 62), (64, 66, 71), 72, 73])
    #     sf_2 = SimpleFormat(quarter_durations=[0.5, 1, 1.5, 2, 3], midis=[0, 69, (72, 73), (58, 60, 65, 71), 80])
    #     sf_3 = SimpleFormat(quarter_durations=[1.5, 1.5, 1.5], midis=[(55, 58), 0, 57])
    #
    #     sfs = [sf_1, sf_2, sf_3]
    #
    #     for index, sf in enumerate(sfs):
    #         sf.to_stream_voice().add_to_score(self.score, staff_number=index + 1)
    #
    #     sum_sf = SimpleFormat.sum(*sfs, no_doubles=True)
    #     sum_sf.to_stream_voice().add_to_score(self.score, staff_number=len(sfs) + 1)
    #
    #     self.score.write(xml_path)
    #     self.assertCompareFiles(xml_path)
