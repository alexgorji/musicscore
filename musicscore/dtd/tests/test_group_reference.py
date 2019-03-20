from unittest import TestCase

from musicscore.dtd.dtd import Sequence, GroupReference, Choice, Element
from musicscore.musicxml.elements.fullnote import FullNote, Rest, Chord
from musicscore.musicxml.elements.note import Duration, Grace, Tie, Cue, DurationGroup, Instrument, EditorialVoice, \
    Type, Dot, Accidental, TimeModification, Stem, Notehead, NoteheadText, Staff, Beam, Notations, Lyric, Play
from musicscore.musicxml.elements.xml_element import XMLElement

TestGroup = Sequence(
    Element(Grace),
    Element(Chord)
)

class Foo(XMLElement):
    _DTD = Sequence(
        Choice(
            Sequence(
                GroupReference(TestGroup),
                Element(Duration)),
            Sequence(
                GroupReference(TestGroup),
            )
        )

    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='foo', *args, **kwargs)


class TestGroupReference(TestCase):
    def setUp(self):
        self.foo = Foo()

    def test_expand(self):
        self.foo.add_child(Chord())
        self.foo.add_child(Grace())

        #
        # print(self.foo.dtd.get_children()[0].get_children()[0].get_children())
        #
        # print([type(child).__name__ for child in self.foo.get_children()])

        self.foo.sort_children()
        # print([type(child).__name__ for child in self.foo.get_children()])
        self.assertEqual([type(child).__name__ for child in self.foo.get_children()], ['Grace', 'Chord'])
