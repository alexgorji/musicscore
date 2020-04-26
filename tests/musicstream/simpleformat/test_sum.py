import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        sf_1 = SimpleFormat(quarter_durations=[1, 2, 3, 2, 1], midis=[60, (60, 62), (64, 66, 71), 72, 73])
        sf_1.to_stream_voice().add_to_score(self.score)
        sf_2 = SimpleFormat(quarter_durations=[0.5, 1, 1.5, 2, 3], midis=[0, 69, (72, 73), (58, 60, 65, 71), 80])
        sf_2.to_stream_voice().add_to_score(self.score, staff_number=2)
        sf_3 = SimpleFormat.sum(sf_1, sf_2)
        sf_3.to_stream_voice().add_to_score(self.score, staff_number=3)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        xml_path = path + '_test_2.xml'
        sf_1 = SimpleFormat(quarter_durations=[1, 2, 3, 2, 1], midis=[60, (60, 62), (64, 66, 71), 72, 73])
        sf_1.to_stream_voice().add_to_score(self.score)
        sf_2 = SimpleFormat(quarter_durations=[0.5, 1, 1.5, 2, 3], midis=[0, 69, (72, 73), (58, 60, 65, 71), 80])
        sf_2.to_stream_voice().add_to_score(self.score, staff_number=2)
        sf_3 = SimpleFormat.sum(sf_1, sf_2, no_doubles=True)
        sf_3.to_stream_voice().add_to_score(self.score, staff_number=3)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        xml_path = path + '_test_3.xml'
        sf_1 = SimpleFormat(quarter_durations=[1, 2, 3, 2, 1], midis=[60, (60, 62), (64, 66, 71), 72, 73])
        sf_2 = SimpleFormat(quarter_durations=[0.5, 1, 1.5, 2, 3], midis=[0, 69, (72, 73), (58, 60, 65, 71), 80])
        sf_3 = SimpleFormat(quarter_durations=[1.5, 1.5, 1.5], midis=[(55, 58), 0, 57])

        sfs = [sf_1, sf_2, sf_3]

        for index, sf in enumerate(sfs):
            sf.to_stream_voice().add_to_score(self.score, staff_number=index + 1)

        sum_sf = SimpleFormat.sum(*sfs, no_doubles=True)
        sum_sf.to_stream_voice().add_to_score(self.score, staff_number=len(sfs) + 1)

        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
