from unittest import TestCase

from musicscore.musicxml.elements.attributes import Attributes, Time, Beats, BeatType, Divisions, Clef, Sign, Line
from musicscore.musicxml.elements.fullnote import Rest
from musicscore.musicxml.elements.note import Note, Duration
from musicscore.musicxml.elements.score_header import PartList, ScorePart, PartName
from musicscore.musicxml.elements.timewise import ScoreTimewise, Measure, Part

import os

path = os.path.abspath(__file__).split('.')[0]


def make_attributes(part):
    attributes = part.add_child(Attributes())
    attributes.add_child(Divisions(2))
    time = attributes.add_child(Time())
    time.add_child(Beats(4))
    time.add_child(BeatType(4))
    clef = attributes.add_child(Clef())
    clef.add_child(Sign('G'))
    clef.add_child(Line(2))


class TestTimewise(TestCase):
    def setUp(self):
        self.score = ScoreTimewise()
        self.score.version = '3.0'
        part_list = self.score.add_child(PartList())
        score_part = part_list.add_child(ScorePart(id='P1'))
        score_part.add_child(PartName(name="Oboe"))
        measure = self.score.add_child(Measure(number='1'))
        part = measure.add_child(Part(id='P1'))
        make_attributes(part)
        note = part.add_child(Note())
        note.add_child(Rest(measure='yes'))
        note.add_child(Duration(8))


    def test_score_head(self):
        print(self.score.to_string())
        self.score.write(path=path)

    # <attributes>
    #   <divisions>2</divisions>
    #   <time>
    #     <beats>4</beats>
    #     <beat-type>4</beat-type>
    #   </time>
    #   <clef>
    #     <sign>G</sign>
    #     <line>2</line>
    #   </clef>
    # </attributes>
    # <note>
    #   <rest measure="yes"/>
    #   <duration>8</duration>
    # </note>
