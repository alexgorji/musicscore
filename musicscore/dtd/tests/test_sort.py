from unittest import TestCase

from musicscore.dtd.dtd import Sequence, Element, GroupReference
from musicscore.musicxml.elements.fullnote import Rest, Chord
from musicscore.musicxml.elements.musicdata import MusicData, Barline, Backup, Direction, Attributes
from musicscore.musicxml.elements.note import Duration, Note
from musicscore.musicxml.elements.xml_element import XMLElement


class DTD1(XMLElement):
    _DTD = Sequence(
        Element(Duration),
        GroupReference(MusicData),
        Element(Chord)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='test_1', *args, **kwargs)


class Sub1(DTD1):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TestSort(TestCase):
    def setUp(self):
        self.dtd_1 = Sub1()

    def add_note(self, duration):
        note_1 = Note()
        note_1.add_child(Rest())
        note_1.add_child(Duration(duration))
        self.dtd_1.add_child(note_1)

    def test_sort(self):

        self.dtd_1.add_child(Barline())
        self.dtd_1.add_child(Chord())
        self.add_note(2)
        self.dtd_1.add_child(Duration())
        self.dtd_1.add_child(Direction())
        self.dtd_1.add_child(Backup())
        self.add_note(1)
        self.dtd_1.add_child(Barline())

        self.dtd_1.sort_children()
        result = ['Duration', 'Barline', 'Note', 'Direction', 'Backup', 'Note', 'Barline', 'Chord']
        self.assertEqual([type(child).__name__ for child in self.dtd_1.get_children()], result)
