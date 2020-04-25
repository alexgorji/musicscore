import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = os.path.abspath(__file__).split('.')[0]


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[7])

        sf.chords[0].add_tremolo()

        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    # def test_2(self):
    #     sf = SimpleFormat(quarter_durations=[7])
    #
    #     sf.chords[0].add_tremolo(number=4)
    #
    #     sf.to_stream_voice().add_to_score(self.score)
    #     xml_path = path + '_test_2.xml'
    #     self.score.write(xml_path)
    #     self.assertCompareFiles(xml_path)

    def test_3(self):
        sf = SimpleFormat(quarter_durations=[7], midis=[(60, 64)])

        sf.chords[0].add_tremolo(3)

        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_3.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
