from itertools import cycle
from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat, TreeChord
from musicscore.musictree.treechordflags1 import PercussionFlag1, XFlag1, BeatwiseFlag1, FingerTremoloFlag1, GlissFlag1
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from quicktions import Fraction
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        durations = [2, 1, 0.5, 0.25, 0.25, 4, 2, 3]
        sf = SimpleFormat(quarter_durations=durations)
        for chord in sf.chords:
            chord.add_flag(PercussionFlag1())

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_2(self):
        xml_path = path + '_test_2.xml'
        durations = [2]
        sf = SimpleFormat(quarter_durations=durations)

        for chord in sf.chords:
            chord.add_flag(XFlag1())

        sf.to_stream_voice().add_to_score(self.score, part_number=1)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_3(self):
        xml_path = path + '_test_3.xml'
        durations = [5]
        sf = SimpleFormat(quarter_durations=durations)

        for chord in sf.chords:
            chord.add_flag(XFlag1())

        sf.to_stream_voice().add_to_score(self.score, part_number=1)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_4(self):
        xml_path = path + '_test_4.xml'
        durations = [2, 1, 0.5, 0.25, 0.25, 4, 2, 3]
        sf = SimpleFormat(quarter_durations=durations)
        sf.to_stream_voice().add_to_score(self.score, part_number=1)

        for chord in sf.chords:
            chord.add_flag(XFlag1())

        sf.to_stream_voice().add_to_score(self.score, part_number=2)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_5(self):
        # todo: see template
        xml_path = path + '_test_5.xml'
        durations = [3.5]
        self.score.set_time_signatures(quarter_durations=[3.5])
        sf = SimpleFormat(quarter_durations=durations)
        sf.to_stream_voice().add_to_score(self.score, part_number=1)

        for chord in sf.chords:
            chord.add_flag(XFlag1())

        sf.to_stream_voice().add_to_score(self.score, part_number=2)

        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)

    def test_6(self):
        self.maxDiff = None
        xml_path = path + '_test_6.xml'
        durations = 5 * [3.5]
        sf = SimpleFormat(quarter_durations=durations)
        sf.to_stream_voice().add_to_score(self.score, part_number=1)

        slur_type = cycle([None, 'tie', 'dashed'])
        for chord in sf.chords:
            type = slur_type.__next__()
            chord.add_flag(XFlag1(slur=type))
            chord.add_words(str(type))

        sf.to_stream_voice().add_to_score(self.score, part_number=2)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_7(self):
        xml_path = path + "_test_7.xml"
        sf = SimpleFormat(midis=[60, 63], quarter_durations=[2, 5.33, 2.666])
        sf.chords[1].add_flag(BeatwiseFlag1())
        # sf.chords[1].add_flag(TreeFingerTremoloFlag(tremolo_chord=TreeChord(midis=57)))
        # sf.chords[1].add_flag(FingerTremoloFlag(tremolo_chord=TreeChord(midis=57)))
        sf.to_stream_voice().add_to_score(self.score)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_8(self):
        xml_path = path + "_test_8.xml"
        sf = SimpleFormat(midis=[60, 63], quarter_durations=[2, 5.33, 2.666])
        sf.chords[1].add_flag(XFlag1(slur='dashed'))
        # sf.chords[1].add_flag(TreeFingerTremoloFlag(tremolo_chord=TreeChord(midis=57)))
        # sf.chords[1].add_flag(FingerTremoloFlag(tremolo_chord=TreeChord(midis=57)))
        sf.to_stream_voice().add_to_score(self.score)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_9(self):
        xml_path = path + "_test_9.xml"
        sf = SimpleFormat(midis=[60, 63], quarter_durations=[2, 5.33, 2.666])
        sf.chords[1].add_flag(FingerTremoloFlag1(tremolo_chord=TreeChord(midis=57), mode='modern'))
        sf.to_stream_voice().add_to_score(self.score)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_10(self):
        xml_path = path + "_test_10.xml"
        sf = SimpleFormat(midis=[84, 84, 84], quarter_durations=[2, 5.33, 2.666])
        sf.to_stream_voice(1).add_to_score(self.score, first_measure=1)

        sf = SimpleFormat(midis=[60, 63], quarter_durations=[2, 5.33, 2.666])
        sf.chords[1].add_flag(FingerTremoloFlag1(tremolo_chord=TreeChord(midis=68), mode='modern'))
        sf.to_stream_voice(2).add_to_score(self.score, first_measure=1)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_11(self):
        xml_path = path + "_test_11.xml"
        sf = SimpleFormat(midis=[60, 60, 60, 60, 60, 60, 60],
                          quarter_durations=[Fraction(3, 2), Fraction(3, 2), Fraction(1, 2), Fraction(1, 2), 1, Fraction(1, 2),
                                             Fraction(3, 2)])
        for ch in sf.chords:
            ch.add_flag(FingerTremoloFlag1(TreeChord(midis=[63]), mode='modern'))
        sf.to_stream_voice(1).add_to_score(self.score, first_measure=1)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_12(self):
        xml_path = path + "_test_12.xml"
        sf = SimpleFormat(midis=[60, 60, 60, 60],
                          quarter_durations=[1, 1, 1, 1])
        for ch in sf.chords:
            ch.add_flag(FingerTremoloFlag1(TreeChord(midis=[63]), mode='modern'))
        sf.to_stream_voice(1).add_to_score(self.score, first_measure=1)
        self.score.accidental_mode = 'modern'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_13(self):
        xml_path = path + "_test_13.xml"
        sf = SimpleFormat(midis=[60, 60, 60, 60],
                          quarter_durations=[1, 1, 1, 1])
        for ch in sf.chords:
            ch.add_flag(FingerTremoloFlag1(TreeChord(midis=[63]), mode='conventional'))
        sf.to_stream_voice(1).add_to_score(self.score, first_measure=1)
        self.score.accidental_mode = 'modern'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_14(self):
        xml_path = path + "_test_14.xml"
        sf = SimpleFormat(midis=[60, 60, 60, 60],
                          quarter_durations=[2, 2, 2, 2])
        for ch in sf.chords:
            ch.add_flag(FingerTremoloFlag1(TreeChord(midis=[63]), mode='conventional'))
        sf.to_stream_voice(1).add_to_score(self.score, first_measure=1)
        self.score.accidental_mode = 'modern'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_15(self):
        xml_path = path + "_test_15.xml"
        sf = SimpleFormat(midis=[60],
                          quarter_durations=[0.5])
        for ch in sf.chords:
            ch.add_flag(FingerTremoloFlag1(TreeChord(midis=[63]), mode='conventional'))
        sf.to_stream_voice(1).add_to_score(self.score, first_measure=1)
        self.score.accidental_mode = 'modern'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_16(self):
        xml_path = path + "_test_16.xml"
        sf = SimpleFormat(midis=[60],
                          quarter_durations=[1.5])
        for ch in sf.chords:
            ch.add_flag(FingerTremoloFlag1(TreeChord(midis=[63]), mode='conventional'))
        sf.to_stream_voice(1).add_to_score(self.score, first_measure=1)
        self.score.accidental_mode = 'modern'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_17(self):
        xml_path = path + "_test_17.xml"
        sf = SimpleFormat(midis=[60, 61, 62, 63, 64],
                          quarter_durations=[1.5, 1, 2, 2.5, 1])
        for ch in sf.chords:
            ch.add_flag(FingerTremoloFlag1(TreeChord(midis=[67]), mode='conventional'))
        sf.to_stream_voice(1).add_to_score(self.score, first_measure=1)
        self.score.accidental_mode = 'modern'
        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)

    def test_18(self):
        xml_path = path + "_test_18.xml"
        sf = SimpleFormat(midis=[60, 61, 62],
                          quarter_durations=[5, 5.5, 2.5])
        for ch in sf.chords:
            ch.add_flag(GlissFlag1())
        sf.to_stream_voice(1).add_to_score(self.score, first_measure=1)
        self.score.accidental_mode = 'modern'
        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)

    def test_19(self):
        xml_path = path + "_test_19.xml"
        sf = SimpleFormat(quarter_durations=[1.5])
        self.score.set_time_signatures(quarter_durations=[1.5])
        for ch in sf.chords:
            ch.add_flag(BeatwiseFlag1(slur='tie'))
        sf.to_stream_voice().add_to_score(self.score)

        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)

    def test_20(self):
        xml_path = path + "_test_20.xml"
        sf = SimpleFormat(quarter_durations=[3])
        self.score.set_time_signatures(quarter_durations=[3])
        for ch in sf.chords:
            ch.add_flag(PercussionFlag1(minimum_duration=0.5))
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_21(self):
        xml_path = path + "_test_21.xml"
        sf = SimpleFormat(quarter_durations=[2, 2])
        sf.chords[0].add_flag(PercussionFlag1(minimum_duration=0.5))
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)


