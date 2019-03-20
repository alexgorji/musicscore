from unittest import TestCase

from musicscore.dtd.dtd import Element, Sequence, GroupReference, Choice
from musicscore.musicxml.elements.attributes import TimeSignature, Beats, BeatType
from musicscore.musicxml.elements.barline import Barline
from musicscore.musicxml.elements.fullnote import Chord, FullNote, Rest
from musicscore.musicxml.elements.note import Duration, Type, Grace, Tie, Cue, DurationGroup, Note
from musicscore.musicxml.elements.xml_element import XMLElement


class TestSortChoice1(TestCase):
    def setUp(self):
        class Foo1(XMLElement):
            _DTD = Choice(
                Element(Duration),
                Element(Barline)
            )

            def __init__(self, *args, **kwargs):
                super().__init__(tag='foo1', *args, **kwargs)

        self.foo1 = Foo1()

    def test_sort_choice1(self):
        self.foo1.add_child(Barline())
        self.foo1.sort_children()
        result = ['Barline']
        self.assertEqual([type(child).__name__ for child in self.foo1.get_children()], result)


class TestSortChoice2(TestCase):
    def setUp(self):
        class Foo2(XMLElement):
            _DTD = Choice(
                Element(Duration),
                Element(Barline),
                min_occurrence=0,
                max_occurrence=None
            )

            def __init__(self, *args, **kwargs):
                super().__init__(tag='foo2', *args, **kwargs)

        self.foo2 = Foo2()

    def test_sort_choice2(self):
        self.foo2.add_child(Barline())
        self.foo2.add_child(Duration(2))
        self.foo2.add_child(Duration(3))
        self.foo2.add_child(Barline())
        self.foo2.sort_children()
        result = ['Barline', 'Duration', 'Duration', 'Barline']
        self.assertEqual([type(child).__name__ for child in self.foo2.get_children()], result)


class TestSortChoice3(TestCase):
    def setUp(self):
        class Foo3(XMLElement):
            _DTD = Choice(
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
            )

            def __init__(self, *args, **kwargs):
                super().__init__(tag='foo3', *args, **kwargs)

        self.foo3 = Foo3()

    def test_sort_choice3(self):
        self.foo3.add_child(Duration(2))
        self.foo3.add_child(Rest())

        self.foo3.sort_children()
        result = ['Rest', 'Duration']
        self.assertEqual([type(child).__name__ for child in self.foo3.get_children()], result)
