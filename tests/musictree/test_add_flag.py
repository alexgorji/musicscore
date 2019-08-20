from itertools import cycle
from unittest import TestCase
import os

from musicscore.musicstream import SimpleFormat, TreeChord
from musicscore.musictree.treechordflags import PercussionFlag, XFlag, BeatwiseFlag, FingerTremoloFlag
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        durations = [2, 1, 0.5, 0.25, 0.25, 4, 2, 3]
        sf = SimpleFormat(durations=durations)
        for chord in sf.chords:
            chord.add_flag(PercussionFlag())

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_2(self):
        xml_path = path + '_test_2.xml'
        durations = [2]
        sf = SimpleFormat(durations=durations)

        for chord in sf.chords:
            chord.add_flag(XFlag())

        sf.to_stream_voice().add_to_score(self.score, part_number=1)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_3(self):
        xml_path = path + '_test_3.xml'
        durations = [5]
        sf = SimpleFormat(durations=durations)

        for chord in sf.chords:
            chord.add_flag(XFlag())

        sf.to_stream_voice().add_to_score(self.score, part_number=1)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_4(self):
        xml_path = path + '_test_4.xml'
        durations = [2, 1, 0.5, 0.25, 0.25, 4, 2, 3]
        sf = SimpleFormat(durations=durations)
        sf.to_stream_voice().add_to_score(self.score, part_number=1)

        for chord in sf.chords:
            chord.add_flag(XFlag())

        sf.to_stream_voice().add_to_score(self.score, part_number=2)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_5(self):
        xml_path = path + '_test_5.xml'
        durations = [3.5]
        self.score.set_time_signatures(durations=[3.5])
        sf = SimpleFormat(durations=durations)
        sf.to_stream_voice().add_to_score(self.score, part_number=1)

        for chord in sf.chords:
            chord.add_flag(XFlag())

        sf.to_stream_voice().add_to_score(self.score, part_number=2)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_6(self):
        self.maxDiff = None
        xml_path = path + '_test_6.xml'
        durations = 5 * [3.5]
        sf = SimpleFormat(durations=durations)
        sf.to_stream_voice().add_to_score(self.score, part_number=1)

        slur_type = cycle([None, 'tie', 'dashed'])
        for chord in sf.chords:
            type = slur_type.__next__()
            chord.add_flag(XFlag(slur=type))
            chord.add_words(str(type))

        sf.to_stream_voice().add_to_score(self.score, part_number=2)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_7(self):
        xml_path = path + "_test_7.xml"
        sf = SimpleFormat(midis=[60, 63], durations=[2, 5.33, 2.666])
        sf.chords[1].add_flag(BeatwiseFlag())
        # sf.chords[1].add_flag(TreeFingerTremoloFlag(tremolo_chord=TreeChord(midis=57)))
        # sf.chords[1].add_flag(FingerTremoloFlag(tremolo_chord=TreeChord(midis=57)))
        sf.to_stream_voice().add_to_score(self.score)

        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_8(self):
        xml_path = path + "_test_8.xml"
        sf = SimpleFormat(midis=[60, 63], durations=[2, 5.33, 2.666])
        sf.chords[1].add_flag(XFlag(slur='dashed'))
        # sf.chords[1].add_flag(TreeFingerTremoloFlag(tremolo_chord=TreeChord(midis=57)))
        # sf.chords[1].add_flag(FingerTremoloFlag(tremolo_chord=TreeChord(midis=57)))
        sf.to_stream_voice().add_to_score(self.score)

        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)

    def test_9(self):
        xml_path = path + "_test_9.xml"
        sf = SimpleFormat(midis=[60, 63], durations=[2, 5.33, 2.666])
        sf.chords[1].add_flag(FingerTremoloFlag(tremolo_chord=TreeChord(midis=57)))
        # sf.chords[1].add_flag(TreeFingerTremoloFlag(tremolo_chord=TreeChord(midis=57)))
        # sf.chords[1].add_flag(FingerTremoloFlag(tremolo_chord=TreeChord(midis=57)))
        sf.to_stream_voice().add_to_score(self.score)

        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)
