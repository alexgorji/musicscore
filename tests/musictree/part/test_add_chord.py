import os

from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        self.score.add_measure()
        self.score.add_part()
        self.score.get_measure(1).get_part(1).add_chord(TreeChord(quarter_duration=4, midis=60))
        xml_path = path + '_test_1.xml'
        self.score.write(path=xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        self.score.add_measure()
        self.score.add_part()
        self.score.get_measure(1).get_part(1).add_chord(TreeChord(quarter_duration=4, midis=60), voice_number=2)
        xml_path = path + '_test_2.xml'
        self.score.write(path=xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        self.score.add_measure()
        self.score.add_part()
        self.score.get_measure(1).get_part(1).add_chord(TreeChord(quarter_duration=4, midis=70), voice_number=2)
        self.score.get_measure(1).get_part(1).add_chord(TreeChord(quarter_duration=4, midis=60), voice_number=4)
        xml_path = path + '_test_3.xml'
        self.score.write(path=xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        self.score.add_measure()
        self.score.add_part()
        self.score.get_measure(1).get_part(1).add_chord(TreeChord(quarter_duration=4, midis=70), staff_number=2)
        xml_path = path + '_test_4.xml'
        self.score.write(path=xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):
        self.score.add_measure()
        self.score.add_part()
        self.score.get_measure(1).get_part(1).add_chord(TreeChord(quarter_duration=4, midis=60), staff_number=1)
        self.score.get_measure(1).get_part(1).add_chord(TreeChord(quarter_duration=4, midis=70), staff_number=2)
        xml_path = path + '_test_5.xml'
        self.score.write(path=xml_path)
        self.assertCompareFiles(xml_path)