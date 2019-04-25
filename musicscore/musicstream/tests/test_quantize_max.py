from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescore_timewise import TreeScoreTimewise
from musicscore.musicxml.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(durations=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        for index, chord in enumerate(sf.chords):
            chord.add_lyric(index + 1)
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 1)
        tree_part_voice = self.score.get_measure(1).get_part(1).get_voice(1)
        for beat in tree_part_voice.beats:
            beat.max_division = 6
        result_path = path + '_test_1'
        self.score.write(path=result_path)
        # TestScore()
