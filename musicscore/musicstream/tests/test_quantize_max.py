from unittest import TestCase
import os

from quicktions import Fraction

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
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

        sf = sf.__deepcopy__()
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 2)

        self.score.fill_with_rest()
        self.score.add_beats()

        for measure in self.score.get_children_by_type(TreeMeasure):
            part = measure.get_part(2)
            for beat in part.get_beats():
                beat.max_division = 7

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        # TestScore()

    def test_2(self):
        self.score.add_measure(TreeMeasure(time=(3, 4)))
        sf = SimpleFormat(durations=[0.5, 0.6, 0.7, 0.8])
        for index, chord in enumerate(sf.chords):
            chord.add_lyric(index + 1)
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 1)

        sf = sf.__deepcopy__()
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 2)

        self.score.fill_with_rest()
        self.score.add_beats()

        for measure in self.score.get_children_by_type(TreeMeasure):
            part = measure.get_part(2)
            for beat in part.get_beats():
                beat.max_division = 7

        self.score.quantize()

        result_path = path + '_test_2'
        self.score.write(path=result_path)
