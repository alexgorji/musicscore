import os

from quicktions import Fraction

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[1, 0.25, 2.25, 0.5, 1, 2])
        sf.to_stream_voice(1).add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        xml_notes = []
        for measure in self.score.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                for staff in part.tree_part_staves.values():
                    xml_notes.extend(staff.xml_notes)
        expected = [0, Fraction(1, 1), Fraction(5, 4), Fraction(2, 1), Fraction(7, 2), 0, Fraction(1, 1),
                    Fraction(3, 1)]
        actual = [xml_note.offset for xml_note in xml_notes]
        self.assertEqual(expected, actual)

    def test_2(self):
        sf_1 = SimpleFormat(quarter_durations=[1, 0.25, 2.25])
        sf_2 = SimpleFormat(quarter_durations=[0.25, 2.25, 1])
        sf_3 = SimpleFormat(quarter_durations=[2.25, 1, 0.25])
        sf_1.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=1)
        sf_2.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=2)
        sf_3.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=3)
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
        xml_note_offsets = {}
        for measure in self.score.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                for key in part.tree_part_staves.keys():
                    staff = part.tree_part_staves[key]
                    xml_note_offsets[key] = [xml_note.offset for xml_note in staff.xml_notes]
        # print(xml_note_offsets)
        expected = {1: [Fraction(0, 1), Fraction(1, 1), Fraction(5, 4), Fraction(2, 1), Fraction(7, 2)],
                    2: [Fraction(0, 1), Fraction(1, 1), Fraction(5, 4), Fraction(2, 1), Fraction(7, 2)],
                    3: [Fraction(0, 1), Fraction(1, 1), Fraction(5, 4), Fraction(2, 1), Fraction(7, 2)]}
        actual = xml_note_offsets
        self.assertEqual(actual, expected)

    def test_3(self):
        sf_1 = SimpleFormat(quarter_durations=[1, 0.25, 2.25])
        sf_2 = SimpleFormat(quarter_durations=[0.25, 2.25, 1], midis=[60, 60, 60])
        sf_1.to_stream_voice(1).add_to_score(self.score, part_number=1, staff_number=1)
        sf_2.to_stream_voice(2).add_to_score(self.score, part_number=1, staff_number=1)
        xml_path = path + '_test_3.xml'
        self.score.write(xml_path)
        xml_note_offsets = {}
        for measure in self.score.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(TreePart):
                for staff in part.tree_part_staves.values():
                    for key in staff.tree_part_voices.keys():
                        voice = staff.tree_part_voices[key]
                        xml_note_offsets[key] = [xml_note.offset for xml_note in voice.xml_notes]
        print(xml_note_offsets)
        expected = {1: [0, Fraction(1, 1), Fraction(5, 4), Fraction(2, 1), Fraction(7, 2)],
                    2: [Fraction(0, 1), Fraction(1, 4), Fraction(1, 1), Fraction(5, 2), Fraction(7, 2)]}

        actual = xml_note_offsets
        self.assertEqual(actual, expected)
    # def test_3(self):
    #     r_sf_2 = SimpleFormat(
    #         quarter_durations=[1, 0.25, 2.25, 0.5, 1, 2, Fraction(1, 3), Fraction(4, 3), Fraction(1, 3), 1],
    #         midis=[60, 61, 54, 63, 65, 65, 64, 60])
    #     r_sf_1 = SimpleFormat(
    #         quarter_durations=[0.25, 2.25, 0.5, 1, 2, Fraction(1, 3), Fraction(4, 3), Fraction(1, 3), 2],
    #         midis=[70, 71, 64, 73, 72, 71, 65])
    #     l_sf_1 = SimpleFormat(quarter_durations=[4, 5], midis=[50, 35])
    #     l_sf_2 = SimpleFormat(quarter_durations=[5, 4], midis=[44, 60])
    #     r_sf_2.auto_clef()
    #     r_sf_1.auto_clef()
    #     l_sf_1.auto_clef()
    #     l_sf_2.auto_clef()
    #     r_sf_1.to_stream_voice(2).add_to_score(self.score, part_number=1, staff_number=1)
    #     r_sf_2.to_stream_voice(1).add_to_score(self.score, part_number=1, staff_number=1)
    #     l_sf_1.to_stream_voice(2).add_to_score(self.score, part_number=1, staff_number=2)
    #     l_sf_2.to_stream_voice(1).add_to_score(self.score, part_number=1, staff_number=2)
    #
    #     xml_path = path + '_test_3.xml'
    #     self.score.write(xml_path)
    #     self.assertCompareFiles(xml_path)
