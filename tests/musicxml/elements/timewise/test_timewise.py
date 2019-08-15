from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.elements.fullnote import Rest
from musicscore.musicxml.elements.note import Note, Duration
from musicscore.musicxml.elements.scoreheader import PartList
from musicscore.musicxml.groups.musicdata import Attributes
from musicscore.musicxml.types.complextypes.attributes import Clef, Divisions, Time, Beats, BeatType
from musicscore.musicxml.types.complextypes.clef import Sign, Line
from musicscore.musicxml.types.complextypes.partlist import ScorePart
from musicscore.musicxml.types.complextypes.scorepart import PartName, PartAbbreviation
from musicscore.musicxml.elements.timewise import Score, Measure, Part

import os

from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class TestTimewise(TestScore):
    def setUp(self):
        self.score = Score()
        self.score.version = '3.0'
        part_list = self.score.add_child(PartList())
        score_part = part_list.add_child(ScorePart(id='P1'))
        score_part.add_child(PartName(name="Oboe"))
        score_part.add_child(PartAbbreviation("Ob."))

        measure = self.score.add_child(Measure(number='1'))
        part = measure.add_child(Part(id='P1'))
        attributes = part.add_child(Attributes())
        attributes.add_child(Divisions(2))
        time = attributes.add_child(Time())
        time.add_child(Beats(4))
        time.add_child(BeatType(4))
        clef = attributes.add_child(Clef())
        clef.add_child(Sign('G'))
        clef.add_child(Line(2))
        note = part.add_child(Note())
        note.add_child(Rest(measure='yes'))
        note.add_child(Duration(8))

        measure = self.score.add_child(Measure(number='2'))
        part = measure.add_child(Part(id='P1'))
        attributes = part.add_child(Attributes())
        attributes.add_child(Divisions(2))
        note = part.add_child(Note())
        note.add_child(Rest(measure='yes'))
        note.add_child(Duration(8))

    def test_score_head(self):
        # print(self.score.to_string())
        self.score.write(path=path)
        self.assert_template(path)

