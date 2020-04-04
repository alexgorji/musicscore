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
        copy = clef.__deepcopy__()
        sf = SimpleFormat(quarter_durations=[1, 1])
        sf.chords[0].add_clef(copy)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        copy = BASS_CLEF.__deepcopy__()
        sf = SimpleFormat(quarter_durations=[1, 1])
        sf.chords[0].add_clef(copy)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
