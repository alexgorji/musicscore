import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf_1 = SimpleFormat(quarter_durations=[2, 2], midis=[0, 71])
        sf_1.chords[1].add_articulation('accent')
        sf_1.to_stream_voice().add_to_score(self.score, staff_number=1)
        sf_2 = SimpleFormat(quarter_durations=[2, 2], midis=[71, 0])
        sf_2.chords[0].add_articulation('staccato')
        sf_2.to_stream_voice().add_to_score(self.score, staff_number=2)

        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        sf_1 = SimpleFormat(quarter_durations=[2, 2], midis=[0, 71])
        sf_1.chords[1].add_articulation('accent')
        sf_1.to_stream_voice(1).add_to_score(self.score, staff_number=1)
        sf_2 = SimpleFormat(quarter_durations=[2, 2], midis=[71, 0])
        sf_2.chords[0].add_articulation('staccato')
        sf_2.to_stream_voice(2).add_to_score(self.score, staff_number=1)

        sf_1 = SimpleFormat(quarter_durations=[2, 2], midis=[0, 71])
        sf_1.chords[1].add_articulation('accent')
        sf_1.to_stream_voice(1).add_to_score(self.score, staff_number=2)
        sf_2 = SimpleFormat(quarter_durations=[2, 2], midis=[71, 0])
        sf_2.chords[0].add_articulation('staccato')
        sf_2.to_stream_voice(2).add_to_score(self.score, staff_number=2)

        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
