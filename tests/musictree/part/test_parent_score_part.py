import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        simple_format = SimpleFormat(quarter_durations=4)
        simple_format.to_stream_voice().add_to_score(self.score)
        part = self.score.get_measure(1).get_part(1)
        expected = part.id
        actual = part.parent_score_part.id
        self.assertEqual(expected, actual)
