import os

from quicktions import Fraction

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treeclef import BASS_CLEF
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        measure = self.score.add_measure()
        self.score.add_part()
        chord = TreeChord(quarter_duration=4, midis=[60])
        measure.get_part(1).add_chord(chord)
        measure.get_part(1).staves = 2
        chord.staff_number = 1
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        measure = self.score.add_measure()
        self.score.add_part()
        chord = TreeChord(quarter_duration=4, midis=[60])
        measure.get_part(1).add_chord(chord)
        chord.staff_number = 2
        measure.get_part(1).staves = 2
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        sf = SimpleFormat(quarter_durations=[0.25, 2.25, 0.5, 1, 2, Fraction(1, 3), Fraction(4, 3), Fraction(1, 3), 1])
        for index, chord in enumerate(sf.chords):
            if index in [1, 6]:
                chord.staff_number = 2
        sf.to_stream_voice(1).add_to_score(self.score, part_number=1)
        all_parts = [part for m in self.score.get_children_by_type(TreeMeasure) for part in
                     m.get_children_by_type(TreePart)]
        for part in all_parts:
            part.staves = 2

        xml_path = path + '_test_3.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        sf = SimpleFormat(4)
        sf.to_stream_voice(1).add_to_score(self.score, part_number=1)
        score_part = self.score.get_score_parts()[0]
        score_part.number_of_staves = 2
        xml_path = path + '_test_4.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):
        sf = SimpleFormat(4)
        sf.to_stream_voice(1).add_to_score(self.score, part_number=1)
        score_part = self.score.get_score_parts()[0]
        score_part.number_of_staves = 2
        clef = BASS_CLEF.__deepcopy__()
        clef.number = 2
        self.score.get_measure(1).get_part(1).add_clef(clef)
        xml_path = path + '_test_5.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_6(self):
        r_sf = SimpleFormat(quarter_durations=[4])
        l_sf = SimpleFormat(quarter_durations=[4], midis=[60])
        r_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=1)
        l_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=2)
        xml_path = path + '_test_6.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_7(self):
        r_sf = SimpleFormat(
            quarter_durations=[0.25, 2.25, 0.5, 1, 2, Fraction(1, 3), Fraction(4, 3), Fraction(1, 3), 1])
        l_sf = SimpleFormat(quarter_durations=[4, 5], midis=[72, 75])
        r_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=1)
        l_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=2)
        xml_path = path + '_test_7.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_8(self):
        r_sf = SimpleFormat(
            quarter_durations=[0.25, 2.25, 0.5, 1, 2, Fraction(1, 3), Fraction(4, 3), Fraction(1, 3), 1])
        l_sf = SimpleFormat(quarter_durations=[4, 5], midis=[50, 55])
        r_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=1)
        l_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=2)
        clef = BASS_CLEF.__deepcopy__()
        clef.number = 2
        self.score.get_measure(1).get_part(1).add_clef(clef)
        xml_path = path + '_test_8.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_9(self):
        r_sf = SimpleFormat(
            quarter_durations=[0.25, 2.25, 0.5, 1, 2, Fraction(1, 3), Fraction(4, 3), Fraction(1, 3), 1],
            midis=[60, 61, 62, 63])
        l_sf = SimpleFormat(quarter_durations=[4, 5], midis=[50, 55])
        r_sf.chords[1].manual_staff_number = 2
        r_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=1)
        l_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=2)
        clef = BASS_CLEF.__deepcopy__()
        clef.number = 2
        self.score.get_measure(1).get_part(1).add_clef(clef)
        xml_path = path + '_test_9.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_10(self):
        # chord clef
        r_sf = SimpleFormat(
            quarter_durations=[4, 4],
            midis=[60, 61])
        l_sf = SimpleFormat(quarter_durations=[4, 4], midis=[50, 55])
        l_sf.chords[0].add_clef(BASS_CLEF)
        r_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=1)
        l_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=2)
        xml_path = path + '_test_10.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_11(self):
        r_sf = SimpleFormat(
            quarter_durations=[0.25, 2.25, 0.5, 1, 2, Fraction(1, 3), Fraction(4, 3), Fraction(1, 3), 1],
            midis=[60, 61, 54, 63])
        l_sf = SimpleFormat(quarter_durations=[4, 5], midis=[72, 53])
        r_sf.chords[1].manual_staff_number = 2
        r_sf.auto_clef()
        l_sf.auto_clef()
        r_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=1)
        l_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=2)

        xml_path = path + '_test_11.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_12(self):
        r_sf_2 = SimpleFormat(
            quarter_durations=[0.25, 2.25, 0.5, 1, 2, Fraction(1, 3), Fraction(4, 3), Fraction(1, 3), 1],
            midis=[60, 61, 54, 63])
        r_sf_1 = SimpleFormat(
            quarter_durations=[0.25, 2.25, 0.5, 1, 2, Fraction(1, 3), Fraction(4, 3), Fraction(1, 3), 1],
            midis=[70, 71, 64, 73])
        l_sf_1 = SimpleFormat(quarter_durations=[4, 5], midis=[50, 35])
        l_sf_2 = SimpleFormat(quarter_durations=[5, 4], midis=[44, 60])
        r_sf_2.auto_clef()
        r_sf_1.auto_clef()
        l_sf_1.auto_clef()
        l_sf_2.auto_clef()
        r_sf_1.to_stream_voice(2).add_to_score(self.score, part_number=1, staff_number=1)
        r_sf_2.to_stream_voice(1).add_to_score(self.score, part_number=1, staff_number=1)
        l_sf_1.to_stream_voice(2).add_to_score(self.score, part_number=1, staff_number=2)
        l_sf_2.to_stream_voice(1).add_to_score(self.score, part_number=1, staff_number=2)

        xml_path = path + '_test_12.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_13(self):
        # accidental
        r_sf = SimpleFormat(quarter_durations=[4, 4, 4, 4], midis=[61, 63, 64, 67])
        l_sf = SimpleFormat(quarter_durations=[4, 4, 4, 4], midis=[60, 64, 63, 64])
        r_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=1)
        l_sf.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=2)

        xml_path = path + '_test_13.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)