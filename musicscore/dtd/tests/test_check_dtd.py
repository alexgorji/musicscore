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

# seq4 = GroupReference(FullNote)

# seq4 = Sequence(
#     Element(Chord, min_occurrence=0),
#     Choice(
#         Element(Pitch),
#         Element(Unpitched),
#         Element(Rest)
#     )
# )

seq4 = Sequence(
    GroupReference(FullNote)
)

seq5 = Choice(
    Sequence(
        GroupReference(FullNote),
        Element(Tie, 0, 2)
    )
)

seq6 = Sequence(
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
    def test_dtd_check_el(self):
        print(seq1.check_dtd(Elision('bla')))
        print(seq1.check_dtd(Lyric()))

