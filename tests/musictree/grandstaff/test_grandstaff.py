import os
from unittest import TestCase

from quicktions import Fraction

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
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
        TestScore().assert_template(xml_path)

    def test_2(self):
        measure = self.score.add_measure()
        self.score.add_part()
        chord = TreeChord(quarter_duration=4, midis=[60])
        measure.get_part(1).add_chord(chord)
        chord.staff_number = 2
        measure.get_part(1).staves = 2
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

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
