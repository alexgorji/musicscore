import os
from unittest import TestCase

from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        measure = self.score.add_measure()
        self.score.add_part()
        chord = TreeChord(quarter_duration=4, midis=[60])
        measure.get_part(1).add_chord(chord)
        print(chord.staff_number)
        chord.staff_number = 1
        print(chord)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
