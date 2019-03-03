from unittest import TestCase
from musicscore.dtd.dtd import Sequence, Choice, Element, Group, DTDLeaf
from musicscore.dtd.note import Grace, FullNote, Cue, Duration, Instrument, EditorialVoice, Type, Dot, Accidental, \
    TimeModification, Stem, Notehead, NotheadText, Staff, Beam, Notations, Play, Lyric, Tie


class TestDTDTree(TestCase):
    def setUp(self):
        self.dtd = (
            Sequence(
                Choice(
                    Sequence(
                        Element(Grace),
                        Choice(
                            Sequence(
                                Group(FullNote)
                            ),
                            Sequence(
                                Group(FullNote),
                                Element(Tie, 0, 2)
                            ),
                            Sequence(
                                Element(Cue),
                                Group(FullNote)
                            )
                        )
                    ),
                    Sequence(
                        Element(Cue),
                        Group(FullNote),
                        Group(Duration)
                    ),
                    Sequence(
                        Group(FullNote),
                        Group(Duration),
                        Element(Tie, 0, 2)
                    )
                ),
                Element(Instrument, 0),
                Group(EditorialVoice),
                Element(Type, 0),
                Element(Dot, 0, None),
                Element(Accidental, 0),
                Element(TimeModification, 0, None),
                Element(Stem, 0),
                Element(Notehead, 0),
                Element(NotheadText, 0),
                Group(Staff, 0),
                Element(Beam, 0, 8),
                Element(Notations, 0, None),
                Element(Lyric, 0, None),
                Element(Play, 0)
            )
        )

    def test_expand(self):

        result = [['Grace', 'FullNote', 'Instrument', 'EditorialVoice', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NotheadText', 'Staff', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'FullNote', 'Tie', 'Instrument', 'EditorialVoice', 'Type', 'Dot', 'Accidental',
                   'TimeModification', 'Stem', 'Notehead', 'NotheadText', 'Staff', 'Beam', 'Notations', 'Lyric',
                   'Play'], ['Grace', 'Cue', 'FullNote', 'Instrument', 'EditorialVoice', 'Type', 'Dot', 'Accidental',
                             'TimeModification', 'Stem', 'Notehead', 'NotheadText', 'Staff', 'Beam', 'Notations',
                             'Lyric', 'Play'],
                  ['Cue', 'FullNote', 'Duration', 'Instrument', 'EditorialVoice', 'Type', 'Dot', 'Accidental',
                   'TimeModification', 'Stem', 'Notehead', 'NotheadText', 'Staff', 'Beam', 'Notations', 'Lyric',
                   'Play'], ['FullNote', 'Duration', 'Tie', 'Instrument', 'EditorialVoice', 'Type', 'Dot', 'Accidental',
                             'TimeModification', 'Stem', 'Notehead', 'NotheadText', 'Staff', 'Beam', 'Notations',
                             'Lyric', 'Play']]

        self.assertEqual([[node._type.__name__ for node in possibility] for possibility in self.dtd.expand()], result)
