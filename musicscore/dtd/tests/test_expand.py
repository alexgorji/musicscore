from musicscore.dtd.dtd import Element, Sequence, Choice, GroupReference
from musicscore.musicxml.common.common import Editorial
from musicscore.musicxml.elements.fullnote import FullNote, Chord, Pitch, Unpitched, Rest
from musicscore.musicxml.types.complextypes.lyric import Elision, EndLine, EndParagraph, Syllabic, Humming, Laughing, \
    Extend, Text
from unittest import TestCase

from musicscore.musicxml.elements.note import Grace, Play, Lyric, Notations, Beam, Staff, NoteheadText, Notehead, Stem, \
    TimeModification, Accidental, Dot, Type, EditorialVoice, Instrument, Tie, DurationGroup, Cue

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
    Element(Elision)
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
                Element(Elision)),
            Element(EndParagraph)
        ),
        Element(EndLine)
    )
)

ch4 = Choice(
    Sequence(
        Choice(
            Element(Grace)
        )
    )
)

ch5 = Sequence(
    Choice(
        Sequence(
            Choice(
                Element(Grace)
            )
        )
    )
)

seq3 = Sequence(
    Choice(
        Sequence(
            Choice(
                Element(Pitch),
                Element(Unpitched),
            )

        )
    )
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


class Test(TestCase):
    def test_expand(self):
        # print(el.expand())
        seq1.choices
        # el.choices
        # ch1.choices
        # print(seq2.get_choices())
        # print(ch1.get_choices())
        # for choice in ch2.get_choices():
        #     print(choice.dump())

        # result = [[['Syllabic', 'Text', [['Elision', 'Syllabic'], 'Text'], 'Extend'], 'EndLine', 'EndParagraph',
        #            [['FootNote', 'Level']]], ['Extend', 'EndLine', 'EndParagraph', [['FootNote', 'Level']]],
        #           ['Laughing', 'EndLine', 'EndParagraph', [['FootNote', 'Level']]],
        #           ['Humming', 'EndLine', 'EndParagraph', [['FootNote', 'Level']]]]
        #
        # choices = [choice.get_leaves(key=lambda leaf: leaf.type_.__name__) for choice in lyric_dtd.get_choices()]
        # self.assertEqual(choices, result)
        # print(ch5.get_choices()[0].get_leaves())
        # for choice in note_dtd.get_choices():
        #     print(choice.get_leaves())
        # choices = [choice.get_leaves(key=lambda leaf: leaf.type_.__name__) for choice in note_dtd.get_choices()]
        # for choice in ch3.get_choices():
        #     print(choice.dump())
