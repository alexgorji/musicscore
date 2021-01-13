import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = os.path.abspath(__file__).split('.')[0]


class TestAddDynamics(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_one_value(self):
        xml_path = path + '_test_one_value.xml'

        sf = SimpleFormat(quarter_durations=[4])
        sf.chords[0].add_dynamics('p')

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_list_of_values(self):
        xml_path = path + '_test_list_of_values.xml'

        sf = SimpleFormat(quarter_durations=[4])
        sf.chords[0].add_dynamics(['sffz', 'mp', 'f'])

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
