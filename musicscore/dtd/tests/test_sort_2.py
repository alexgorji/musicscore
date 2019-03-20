from musicscore.musicxml.elements.fullnote import FullNote, Rest
from musicscore.musicxml.elements.note import Duration, Grace, Tie, Cue, DurationGroup, Instrument, EditorialVoice, \
    Type, Dot, Accidental, TimeModification, Stem, Notehead, NoteheadText, Staff, Beam, Notations, Lyric, Play
from musicscore.dtd.dtd import Sequence, Element, GroupReference, Choice
from unittest import TestCase

from musicscore.musicxml.elements.xml_element import XMLElement

_DTD = Sequence(
    Choice(
        Sequence(
            Element(Grace),
            Choice(
                Sequence(
                    GroupReference(FullNote)
                ),
                Sequence(
                    GroupReference(FullNote),
                    Element(Tie, 0, 2)
                ),
                Sequence(
                    Element(Cue),
                    GroupReference(FullNote)
                )
            )
        ),
        Sequence(
            Element(Cue),
            GroupReference(FullNote),
            GroupReference(DurationGroup)
        ),
        Sequence(
            GroupReference(FullNote),
            GroupReference(DurationGroup),
            Element(Tie, 0, 2)
        )
    ),
    Element(Instrument, 0),
    GroupReference(EditorialVoice, 0),
    Element(Type, 0),
    Element(Dot, 0, None),
    Element(Accidental, 0),
    Element(TimeModification, 0, None),
    Element(Stem, 0),
    Element(Notehead, 0),
    Element(NoteheadText, 0),
    GroupReference(Staff, 0),
    Element(Beam, 0, 8),
    Element(Notations, 0, None),
    Element(Lyric, 0, None),
    Element(Play, 0)
)


class Foo(XMLElement):
    _DTD = Sequence(
        Choice(
            Sequence(
                Element(Grace),
                Choice(
                    Sequence(
                        Element(Rest),
                        GroupReference(FullNote),
                        GroupReference(FullNote),
                        Element(Rest)
                    )
                )
            ),
            Sequence(
                Element(Cue),
                GroupReference(FullNote),
                GroupReference(DurationGroup)
            )
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='foo', *args, **kwargs)


class TestGroupReference(TestCase):
    def setUp(self):
        self.foo = Foo()

    def test_sort(self):
        # choice1 = self.foo.dtd.get_children()[0]
        # print('choice1', choice1)
        # seq1 = choice1.get_children()[0]
        # print('seq1', seq1)
        # el1 = seq1.get_children()[0]
        # print('el1', el1)
        # choice2 = seq1.get_children()[1]
        # print('choice2', choice2)
        # seq2 = choice2.get_children()[0]
        # print('seq2', seq2)
        # group1 = seq2.get_children()[1]
        # print('group1', group1)
        # group_sequence = group1.get_children()[0]
        # print('group_sequence', group_sequence)
        # group_sequence_children = group_sequence.get_children()
        # print('group_sequence_children', group_sequence_children)
        # group_sequence_choice = group_sequence.get_children()[1]
        # print('group_sequence_choice', group_sequence_choice)
        # group_sequence_choice_children = group_sequence_choice.get_children()
        # print('group_sequence_choice_children', group_sequence_choice_children)
        # print()
        # print(self.foo.dtd.get_leaves())
        # print(self.foo.dtd.expand()[2])

        self.foo.add_child(Rest())
        self.foo.add_child(Grace())
        # print(self.foo.get_children())
        self.foo.sort_children()
        result = ['Grace', 'Rest']
        self.assertEqual([type(child).__name__ for child in self.foo.get_children()], result)

        # print('current_combination', self.foo.dtd.get_current_combination())

