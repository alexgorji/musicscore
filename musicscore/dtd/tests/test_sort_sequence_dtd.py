from unittest import TestCase

from musicscore.dtd.dtd import Element, Sequence, GroupReference, Choice
from musicscore.musicxml.elements.attributes import TimeSignature, Beats, BeatType
from musicscore.musicxml.elements.barline import Barline
from musicscore.musicxml.elements.music_data import Backup
from musicscore.musicxml.elements.note import Duration
from musicscore.musicxml.elements.xml_element import XMLElement


class TestSortSequence1(TestCase):
    def setUp(self):
        class Foo1(XMLElement):
            _DTD = Sequence(
                Element(Duration),
                Element(Barline)
            )

            def __init__(self, *args, **kwargs):
                super().__init__(tag='foo1', *args, **kwargs)

        self.foo1 = Foo1()

    def test_sort_sequence1(self):
        self.foo1.add_child(Barline())
        self.foo1.add_child(Duration(2))
        self.foo1.sort_children()
        result = ['Duration', 'Barline']
        self.assertEqual([type(child).__name__ for child in self.foo1.get_children()], result)


class TestSortSequence2(TestCase):
    def setUp(self):
        class Foo2(XMLElement):
            _DTD = Sequence(
                Element(Duration),
                Element(Barline),
                max_occurrence=None
            )

            def __init__(self, *args, **kwargs):
                super().__init__(tag='foo2', *args, **kwargs)

        self.foo2 = Foo2()

    def test_sort_sequence1(self):
        self.foo2.add_child(Barline())
        self.foo2.add_child(Duration(2))
        self.foo2.add_child(Duration(3))
        self.foo2.add_child(Barline())
        self.foo2.sort_children()
        result = ['Duration', 'Barline', 'Duration', 'Barline']
        self.assertEqual([type(child).__name__ for child in self.foo2.get_children()], result)


class TestSortSequence3(TestCase):
    def setUp(self):
        class Foo3(XMLElement):
            _DTD = Sequence(
                Element(Duration),
                Element(Barline),
                GroupReference(TimeSignature, max_occurrence=2)
            )

            def __init__(self, *args, **kwargs):
                super().__init__(tag='foo3', *args, **kwargs)

        self.foo3 = Foo3()

    def test_sort_sequence1(self):
        self.foo3.add_child(Beats(4))
        self.foo3.add_child(BeatType(4))
        self.foo3.add_child(Barline())
        self.foo3.add_child(BeatType(2))
        self.foo3.add_child(Duration(2))
        self.foo3.add_child(Beats(2))
        self.foo3.sort_children()
        result = ['Duration', 'Barline', 'Beats', 'BeatType', 'Beats', 'BeatType']
        self.assertEqual([type(child).__name__ for child in self.foo3.get_children()], result)


class TestSortSequence4(TestCase):
    def setUp(self):
        class Foo4(XMLElement):
            _DTD = Sequence(
                Choice(Element(Backup),
                       Element(Barline)
                       ),
                Element(Duration),
                GroupReference(TimeSignature, max_occurrence=2)
            )

            def __init__(self, *args, **kwargs):
                super().__init__(tag='foo4', *args, **kwargs)

        self.foo4 = Foo4()

    def test_sort_sequence1(self):
        # self.foo4.add_child(Duration(2))
        self.foo4.add_child(Beats(4))
        self.foo4.add_child(BeatType(4))
        self.foo4.add_child(Barline())
        self.foo4.add_child(BeatType(2))
        self.foo4.add_child(Duration(2))
        self.foo4.add_child(Beats(2))
        self.foo4.sort_children()
        result = ['Barline', 'Duration', 'Beats', 'BeatType', 'Beats', 'BeatType']
        self.assertEqual([type(child).__name__ for child in self.foo4.get_children()], result)