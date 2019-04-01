from unittest import TestCase

from musicscore.dtd.dtd import Sequence, GroupReference, Choice, Element
from musicscore.musicxml.elements.fullnote import Chord
from musicscore.musicxml.elements.note import Duration, Grace
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
        self.assertEqual([type(child).__name__ for child in self.foo.get_children()], ['Grace', 'Chord'])
