import os

from quicktions import Fraction

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treechordflags3 import TreeChordFlag3
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):
    def setUp(self):
        self.score = TreeScoreTimewise()
        self.score.add_measure()
        self.score.add_part()

    def test_1(self):
        midis = [61, 61, 62, 60, 63, 64, 65, 61]
        for midi in midis:
            self.score.add_chord(1, 1, TreeChord(midi, quarter_duration=0.5))

        self.score.get_measure(1).get_part(1)
        self.score.finish()

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        midis = [60.0, 60.5, 61.0, 62.5, 64.0, 66.0, 68.0, 69.5, 71.0, 71.5, 72.0, 71.5, 71.0, 69.5, 68.0, 66.0, 64.0,
                 62.5, 61.0, 60.5]
        measure_number = 1
        for midi in midis:
            chord = TreeChord(midi, quarter_duration=0.5)
            chord.add_lyric(midi)
            self.score.add_chord(measure_number, 1, chord)
            remaining_duration = self.score.get_measure(measure_number).get_part(1).get_staff(1).get_voice(
                1).remaining_duration
            if remaining_duration == 0:
                self.score.add_measure()
                measure_number += 1
        self.score.accidental_mode = 'modern'
        result_path = path + '_test_2'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_3(self):
        midis = [(61.0, 63), 61.0, 0, 62.0, 61, 61, 61, (62, 61)]
        measure_number = 1
        for midi in midis:
            chord = TreeChord(midi, quarter_duration=0.5)
            chord.add_lyric([m.value for m in chord.midis])
            self.score.add_chord(measure_number, 1, chord)
            remaining_duration = self.score.get_measure(measure_number).get_part(1).get_staff(1).get_voice(
                1).remaining_duration
            if remaining_duration == 0:
                self.score.add_measure()
                measure_number += 1
        self.score.accidental_mode = 'modern'
        result_path = path + '_test_3'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_4(self):
        simpleformat = SimpleFormat(midis=list(range(60, 68)))
        voice = simpleformat.to_stream_voice(2)
        voice.add_to_score(self.score)
        xml_path = path + '_test_4.xml'
        self.score.accidental_mode = 'modern'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):
        simpleformat = SimpleFormat(midis=[71.5, 71.5, 72, 72, 71.5, 71.5], quarter_durations=6 * [0.5])
        voice = simpleformat.to_stream_voice(1)
        voice.add_to_score(self.score)
        result_path = path + '_test_5'
        self.score.accidental_mode = 'normal'
        self.score.write(result_path)
        TestScore().assert_template(result_path=result_path)

    def test_6(self):
        midis = [51.5, 51.5, 50.5, 48.5, 49.5, 48.5, 50.0, 50.0, 49.5, 49.0]
        durations = [Fraction(255, 56), Fraction(6525, 3136), Fraction(6075, 3136), Fraction(2475, 3136),
                     Fraction(2145, 3136), Fraction(2805, 3136), Fraction(1815, 3136), Fraction(65, 56),
                     Fraction(2015, 1568), Fraction(1625, 1568)]
        simpleformat = SimpleFormat(midis=midis, quarter_durations=durations)
        simpleformat.auto_clef()
        voice = simpleformat.to_stream_voice(1)
        voice.add_to_score(self.score)
        result_path = path + '_test_6'
        self.score.max_division = 7
        self.score.accidental_mode = 'modern'
        self.score.write(result_path)
        TestScore().assert_template(result_path=result_path)

    def test_7(self):
        # todo update_accidental does not work ...
        class TestFlag3(TreeChordFlag3):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def implement(self, chord):
                split = chord.split(2, 2)
                split[0].to_rest()
                for ch in split:
                    ch.update_type()
                    ch.update_dot()
                return split

        xml_path = path + '_test_7.xml'
        sf = SimpleFormat(midis=[61], quarter_durations=[4])
        sf.to_stream_voice().add_to_score(self.score, part_number=1)
        chord = sf.chords[0]
        chord.add_flag(TestFlag3())
        sf.to_stream_voice().add_to_score(self.score, part_number=2)
        self.score.write(xml_path)

    def test_8(self):
        midis = [60 + factor * 0.5 for factor in range(0, 25)]
        simple_format = SimpleFormat(midis=midis + midis[-1::-1][1:])
        for index, chord in enumerate(simple_format.chords):
            if index <= len(midis) - 1:
                chord.midis[0].accidental.mode = 'sharp'
            else:
                chord.midis[0].accidental.mode = 'flat'
        simple_format.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_8.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_9(self):
        midis = [60, 61, 62, 63, 64, 61, 62, 61]
        simple_format = SimpleFormat(midis=midis)
        simple_format.to_stream_voice().add_to_score(self.score, part_number=1)
        for chord in simple_format.chords:
            chord.midis[0].accidental.force_show = True
        simple_format.to_stream_voice().add_to_score(self.score, part_number=2)
        for chord in simple_format.chords:
            chord.midis[0].accidental.force_hide = True
        simple_format.to_stream_voice().add_to_score(self.score, part_number=3)
        xml_path = path + '_test_9.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    # def test_10(self):
    #     v1 = SimpleFormat(quarter_durations=[2, 2], midis=[72, 73])
    #     v2 = SimpleFormat(quarter_durations=[2, 2], midis=[60, 61])
    #     v1.to_stream_voice(1).add_to_score(self.score)
    #     v2.to_stream_voice(2).add_to_score(self.score)
    #
    #     xml_path = path + '_test_10.xml'
    #     self.score.write(xml_path)
    #     self.assertCompareFiles(xml_path)
