import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class TestTreeTimewise(TestCase):
    def setUp(self):
        self.score = TreeScoreTimewise()
        self.score.add_measure()
        self.score.add_part()

    def test_score(self):
        result_path = path + '_test_score'
        self.score.write(result_path)
        TestScore().assert_template(result_path=result_path)

    def test_add_note(self):
        self.score.add_chord(1, 1, TreeChord(0, 1))
        self.score.add_chord(1, 1, TreeChord(0, quarter_duration=1))
        self.score.add_chord(1, 1, TreeChord(61, quarter_duration=2))
        self.score.finish()
        result_path = path + '_test_add_note'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_add_chord(self):
        self.score.add_chord(1, 1, TreeChord((60, 61), quarter_duration=4))
        self.score.finish()
        # print(self.score.to_string())
        # self.score.write(path=path)

    def test_4(self):
        self.score.tuplet_line_width = 2.4
        sf = SimpleFormat(quarter_durations=[0.2, 0.8])
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_4.xml'
        self.score.write(xml_path)
        TestScore().assert_template(result_path=xml_path)
