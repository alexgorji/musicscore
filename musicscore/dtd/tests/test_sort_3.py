from musicscore.musicxml.elements.fullnote import FullNote, Rest
from musicscore.musicxml.elements.note import Duration, Grace, Tie, Cue, DurationGroup, Instrument, EditorialVoice, \
    Type, Dot, Accidental, TimeModification, Stem, Notehead, NoteheadText, Staff, Beam, Notations, Lyric, Play
from musicscore.dtd.dtd import Sequence, Element, GroupReference, Choice
from unittest import TestCase

from musicscore.musicxml.elements.score_header import PartGroupGroup, ScorePartGroup, PartGroup, ScorePart
from musicscore.musicxml.elements.xml_element import XMLElement


class Foo(XMLElement):
    _DTD = Sequence(
        GroupReference(PartGroupGroup, min_occurrence=0, max_occurrence=None),
        GroupReference(ScorePartGroup),
        Choice(
            GroupReference(PartGroupGroup),
            GroupReference(ScorePartGroup),
            min_occurrence=0, max_occurrence=None
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='foo', *args, **kwargs)


# class TestGroupReference(TestCase):
#     def setUp(self):
#         self.foo = Foo()
#
#     def test_sort(self):
#         self.foo.add_child(PartGroup('start'))
#         self.foo.add_child(ScorePart(id='p1'))

