from unittest import TestCase

from musicscore.musicxml.elements.attributes import Attributes, Time, Beats, BeatType, Divisions, Clef, Sign, Line
from musicscore.musicxml.elements.fullnote import Rest, Pitch
from musicscore.musicxml.elements.note import Note, Duration
from musicscore.musicxml.elements.partwise import ScorePartwise, Part, Measure
from musicscore.musicxml.elements.score_header import PartList, ScorePart, PartName, PartAbbreviation

import os

from musicscore.musicxml.tests.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class TestPartwise(TestScore):
    def setUp(self):
        self.score = ScorePartwise()
        self.score.version = '3.0'
        part_list = self.score.add_child(PartList())
        score_part = part_list.add_child(ScorePart(id='P1'))
        score_part.add_child(PartName(name="Oboe", print_object='yes'))

        part = self.score.add_child(Part(id='P1'))
        measure = part.add_child(Measure(number='1'))
        attributes = measure.add_child(Attributes())
        attributes.add_child(Divisions(1))
        time = attributes.add_child(Time())
        time.add_child(Beats(4))
        time.add_child(BeatType(4))
        clef = attributes.add_child(Clef())
        clef.add_child(Sign('G'))
        clef.add_child(Line(2))
        note = measure.add_child(Note())
        note.add_child(Pitch())
        note.add_child(Duration(4))

    def test_score_head(self):
        # print(self.score.to_string())
        self.score.write(path=path)
        self.assert_template(path)
