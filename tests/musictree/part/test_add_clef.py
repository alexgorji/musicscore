import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treeclef import BASS_CLEF
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):

    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        sf = SimpleFormat(quarter_durations=4, midis=0)
        sf.to_stream_voice().add_to_score(self.score)
        self.score.get_measure(1).get_part(1).add_clef(BASS_CLEF)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
