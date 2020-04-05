import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treeclef import TreeClef, BASS_CLEF
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):

    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        clef = TreeClef(number=2)
        sf = SimpleFormat(quarter_durations=[1, 1])
        sf.chords[0].add_clef(clef)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[1, 1])
        sf.chords[0].add_clef(BASS_CLEF)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
