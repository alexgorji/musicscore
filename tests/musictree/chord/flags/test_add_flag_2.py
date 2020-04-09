import os

from musicscore.musicstream.streamvoice import SimpleFormat, TreeChord
from musicscore.musictree.treechordflags2 import FingerTremoloFlag2, NoiseFlag2
from musicscore.musictree.treeinstruments import Piano
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        # finger tremolo
        xml_path = path + '_test_1.xml'
        durations = [2, 2, 2]
        midis = [60, 62, 63]
        sf = SimpleFormat(quarter_durations=durations, midis=midis)
        for chord in sf.chords:
            chord.add_flag(FingerTremoloFlag2(tremolo_chord=TreeChord(midis=[67])))

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        # finger tremolo
        xml_path = path + '_test_2.xml'
        durations = [1.5, 1.5, 1.5]
        midis = [60, 62, 63]
        sf = SimpleFormat(quarter_durations=durations, midis=midis)
        for chord in sf.chords:
            chord.add_flag(FingerTremoloFlag2(tremolo_chord=TreeChord(midis=[67])))

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        # finger tremolo
        xml_path = path + '_test_3.xml'
        durations = [0.25]
        midis = [60]
        sf = SimpleFormat(quarter_durations=durations, midis=midis)
        for chord in sf.chords:
            chord.add_flag(FingerTremoloFlag2(tremolo_chord=TreeChord(midis=[67])))

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        # finger tremolo
        xml_path = path + '_test_4.xml'
        durations = [0.2, 0.8, 1]
        midis = [60, 62, 63]
        sf = SimpleFormat(quarter_durations=durations, midis=midis)
        for chord in sf.chords:
            chord.add_flag(FingerTremoloFlag2(tremolo_chord=TreeChord(midis=[67])))

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):
        # finger tremolo
        self.score.add_instrument(Piano())
        xml_path = path + '_test_5.xml'
        durations = [5, 3]
        midis = [63, 0]
        sf = SimpleFormat(quarter_durations=durations, midis=midis)
        tremolo_chord = TreeChord(midis=[47])
        tremolo_chord.manual_staff_number = 2
        sf.chords[0].add_flag(FingerTremoloFlag2(tremolo_chord=tremolo_chord))
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_6(self):
        # noise flag
        xml_path = path + '_test_6.xml'
        durations = [0.25, 0.75, 0.5, 0.5, 1, 1.25, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
        sf = SimpleFormat(quarter_durations=durations)
        for chord in sf.chords:
            chord.add_flag(NoiseFlag2())

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
