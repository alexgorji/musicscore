import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = os.path.abspath(__file__).split('.')[0]


class TestAddBracket(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_arrow(self):
        xml_path = path + '_test_arrow.xml'

        sf = SimpleFormat(quarter_durations=5 * [2.25])
        sf.chords[0].add_bracket(type='start', line_end='none', relative_x=50)
        sf.chords[1].add_bracket(type='continue', line_end='none')
        sf.chords[2].add_bracket(type='stop', line_end='arrow', relative_x=-30, relative_y=20)

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    # def test_dashed_arrow(self):
    #     xml_path = path + '_test_dashed_arrow.xml'
    #
    #     sf = SimpleFormat(quarter_durations=5 * [2.25])
    #     sf.chords[0].add_bracket(type='start', line_end='none', line_type='dashed', relative_x=50)
    #     sf.chords[1].add_bracket(type='continue', line_type='dashed', line_end='none')
    #     sf.chords[2].add_bracket(type='stop', line_end='arrow', line_type='dashed', relative_x=-30, relative_y=20)
    #
    #     sf.to_stream_voice().add_to_score(self.score)
    #     self.score.write(xml_path)
    #     self.assertCompareFiles(xml_path)
