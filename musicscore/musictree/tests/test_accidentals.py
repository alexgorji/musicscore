import os
from unittest import TestCase

from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescore_timewise import TreeScoreTimewise
from musicscore.musicxml.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self):
        self.score = TreeScoreTimewise()
        self.score.add_measure()
        self.score.add_part('one')

    def test_1(self):
        midis = [61, 61, 62, 60, 63, 64, 65, 61]
        for midi in midis:
            self.score.add_chord(1, 1, TreeChord(midi, quarter_duration=0.5))

        self.score.get_measure(1).get_part(1)
        self.score.finish()

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        midis = [60.0, 60.5, 61.0, 62.5, 64.0, 66.0, 68.0, 69.5, 71.0, 71.5, 72.0, 71.5, 71.0, 69.5, 68.0, 66.0, 64.0,
                 62.5, 61.0, 60.5]
        measure_number = 1
        for midi in midis:
            chord = TreeChord(midi, quarter_duration=0.5)
            chord.add_lyric(midi)
            self.score.add_chord(measure_number, 1, chord)
            remaining_duration = self.score.get_measure(measure_number).get_part(1).get_voice(1).remaining_duration
            if remaining_duration == 0:
                self.score.add_measure()
                measure_number += 1
        self.score.accidental_mode = 'modern'
        result_path = path + '_test_2'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_3(self):
        midis = [(61.0, 63), 61.0, 0, 62.0, 61, 61, 61, (62, 61)]
        measure_number = 1
        for midi in midis:
            chord = TreeChord(midi, quarter_duration=0.5)
            chord.add_lyric(midi)
            self.score.add_chord(measure_number, 1, chord)
            remaining_duration = self.score.get_measure(measure_number).get_part(1).get_voice(1).remaining_duration
            if remaining_duration == 0:
                self.score.add_measure()
                measure_number += 1
        self.score.accidental_mode = 'modern'
        result_path = path + '_test_3'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
