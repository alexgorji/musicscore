from unittest import TestCase

from musicscore.musicxml.elements.score_header import PartList, ScorePart, PartName
from musicscore.musicxml.elements.timewise import ScoreTimewise, Measure, Part

import os

path = os.path.abspath(__file__).split('.')[0]


class TestTimewise(TestCase):
    def setUp(self):
        self.score = ScoreTimewise()
        self.score.version = '3.0'
        part_list = self.score.add_child(PartList())
        score_part = part_list.add_child(ScorePart(id='p1'))
        score_part.add_child(PartName(name="oboe"))
        measure = self.score.add_child(Measure(number='1'))
        measure.add_child(Part(id='p1'))

    def test_score_head(self):
        print(self.score.to_string())
        self.score.write(path=path)
