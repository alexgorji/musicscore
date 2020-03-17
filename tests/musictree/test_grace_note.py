import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        self.score.add_measure()
        self.score.add_part()
        self.score.add_chord(1, 1, TreeChord())
        self.score.add_chord(1, 1, TreeChord(quarter_duration=0))
        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[0.75, 0.25, 1, 0.5, 4])
        sf.chords[1].set_manual_type('16th')
        sf.chords[1].quarter_duration = 0
        sf.chords[0].set_manual_type('eighth')
        sf.chords[0].set_manual_dots(1)
        sf.chords[0].quarter_duration = 0
        sf.chords[2].set_manual_type('quarter')
        sf.chords[2].quarter_duration = 0
        sf.chords[3].set_manual_type('eighth')
        sf.chords[3].quarter_duration = 0

        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + 'test_2.xml'
        self.score.write(xml_path)
        TestScore().assert_template(result_path=xml_path)

    def test_3(self):
        sf = SimpleFormat(quarter_durations=[4])
        sf.chords[0].add_grace_chords([TreeChord(60), TreeChord(63), TreeChord(68)])
        sf.chords[0].add_grace_chords([TreeChord(61), TreeChord(66)], mode='post')

        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + 'test_3.xml'
        self.score.write(xml_path)
        TestScore().assert_template(result_path=xml_path)
