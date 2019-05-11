from musicscore.dtd.dtd import Element, Sequence, Choice, GroupReference, ChildTypeDTDConflict, \
    ChildOccurrenceDTDConflict, ChildIsNotOptional
from musicscore.musicxml.groups.common import Editorial
from musicscore.musicxml.elements.fullnote import FullNote, Pitch, Unpitched, Rest, Alter
from musicscore.musicxml.groups.musicdata import Backup, Forward, Direction, Attributes, Sound, Barline, Link, \
    Bookmark
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.attributes import TimeSignature, Interchangeable, SenzaMisura, Beats, BeatType, Time
from musicscore.musicxml.types.complextypes.lyric import Elision, EndLine, EndParagraph, Syllabic, Humming, Laughing, \
    Extend, Text
from unittest import TestCase

from musicscore.musicxml.elements.note import Grace, Play, Lyric, Notations, Beam, Staff, NoteheadText, Notehead, Stem, \
    TimeModification, Accidental, Dot, Type, EditorialVoice, Instrument, Tie, DurationGroup, Cue, Duration, Note

el = Element(Elision)

seq1 = Sequence(
    Element(Syllabic),
    Element(Elision)
)

seq2 = Sequence(
    Element(Syllabic),
    Element(Elision),
    Sequence(
        Element(EndLine),
        Element(EndParagraph)
    )
)

ch1 = Choice(
    Element(Syllabic),
    Element(Elision),
    Element(EndLine)
)

ch2 = Sequence(
    Choice(
        Element(Syllabic),
        Element(Elision)
    ),
    Element(EndLine)
)

ch3 = Choice(
    Sequence(
        Choice(
            Sequence(
                Element(Syllabic),
                Element(Elision)
            ),
            Element(EndParagraph)
        ),
        Element(EndLine)
    ),
    Element(EndLine)
)

lyric_dtd = Sequence(
    Choice(
        Sequence(
            Element(Syllabic, min_occurrence=0),
            Element(Text),
            Sequence(
                Sequence(
                    Element(Elision),
                    Element(Syllabic, min_occurrence=0),
                    min_occurrence=0
                ),
                Element(Text)
                ,
                min_occurrence=0,
                max_occurrence=None
            ),
            Element(Extend, min_occurrence=0)
        ),
        Element(Extend),
        Element(Laughing),
        Element(Humming)
    ),
    Element(EndLine, min_occurrence=0),
    Element(EndParagraph, min_occurrence=0),
    GroupReference(Editorial)
)

note_dtd = Sequence(
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

MusicData = Sequence(
    Choice(
        Element(Note),
        Element(Backup),
        Element(Forward),
        Element(Direction),
        Element(Attributes),
        Element(Sound),
        Element(Barline),
        Element(Link),
        Element(Bookmark),
        min_occurrence=0,
        max_occurrence=None
    )
)


class TestXML(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='test-xml', *args, **kwargs)


class Test(TestCase):

    def test_dtd_check_type(self):
        # dtd = seq2.__deepcopy__()
        TestXML._DTD = seq2
        test = TestXML()

        test.add_xml_child(Elision('bla'))
        test.add_xml_child(Syllabic('single'))
        with self.assertRaises(ChildTypeDTDConflict):
            test.add_xml_child(Lyric())

        TestXML._DTD = ch2
        test = TestXML()

        # dtd = ch2.__deepcopy__()
        test.add_xml_child(EndLine())
        test.add_xml_child(Syllabic('single'))
        with self.assertRaises(ChildTypeDTDConflict):
            test.add_xml_child(Elision('bla'))

    # def test_dtd_check_max_occurrence(self):
    #     dtd = seq2.__deepcopy__()
    #     dtd.add_xml_child(Elision('bla'))
    #     # print(dtd.get_current_xml_children())
    #     with self.assertRaises(ChildOccurrenceDTDConflict):
    #         dtd.add_xml_child(Elision('bla'))
    #
    #     dtd = ch2.__deepcopy__()
    #     dtd.add_xml_child(EndLine())
    #     dtd.add_xml_child(Syllabic('single'))
    #     with self.assertRaises(ChildOccurrenceDTDConflict):
    #         dtd.add_xml_child(Syllabic('single'))


class TestNoteDtd(TestCase):
    def setUp(self):
        self.note = Note()
        # self.dtd = note_dtd.__deepcopy__()
        self.note.add_xml_child(Instrument())
        self.note.add_xml_child(Rest())
        self.note.add_xml_child(Duration())
        self.note.add_xml_child(Type('quarter'))

    def test_dtd_note_1(self):
        with self.assertRaises(ChildTypeDTDConflict):
            self.note.add_xml_child(Unpitched())

    def test_dtd_note_2(self):
        with self.assertRaises(ChildOccurrenceDTDConflict):
            self.note.add_xml_child(Instrument())

    def test_dtd_note_3(self):
        self.note.add_xml_child(Tie())
        self.note.add_xml_child(Tie())

        result = ['Rest', 'Duration', 'Tie', 'Tie', 'Instrument', 'Type']
        self.assertEqual([type(xml_child).__name__ for xml_child in self.note.current_children], result)

        with self.assertRaises(ChildOccurrenceDTDConflict):
            self.note.add_xml_child(Tie())

    def test_dtd_pitch(self):
        p = Pitch()
        result = ['Step', 'Octave']
        self.assertEqual([type(child).__name__ for child in p.get_children()], result)
        p.add_child(Alter(2))
        result = ['Step', 'Alter', 'Octave']
        self.assertEqual([type(child).__name__ for child in p.get_children()], result)
        # p.close()
        # print(p.to_string())


class TestMusicData(TestCase):
    def setUp(self):
        TestXML._DTD = MusicData
        self.md = TestXML()

    def test_music_data_dtd(self):
        self.md.add_xml_child(Forward())
        self.md.add_xml_child(Bookmark())
        self.md.add_xml_child(Forward())
        self.md.add_xml_child(Direction())
        result = ['Forward', 'Bookmark', 'Forward', 'Direction']
        self.assertEqual([type(xml_child).__name__ for xml_child in self.md.current_children], result)


time_dtd = Choice(
    Sequence(
        GroupReference(TimeSignature, max_occurrence=None),
        Element(Interchangeable, min_occurrence=0)
    ),
    Element(SenzaMisura)
)


class TestTimeDtd(TestCase):
    def setUp(self):
        self.time = Time()

    def test_time(self):
        self.time.add_child(BeatType(4))
        self.time.add_child(Beats(4))
        self.time.add_child(BeatType(2))
        self.time.add_child(BeatType(16))
        self.time.add_child(Beats(5))
        result = [('Beats', 4), ('BeatType', 4), ('Beats', 5), ('BeatType', 2), ('BeatType', 16)]
        self.assertEqual([(type(child).__name__, child.value) for child in self.time.current_children], result)
        with self.assertRaises(ChildIsNotOptional):
            self.time.close_dtd()
