from unittest import TestCase
from musicscore.dtd.dtd import Sequence, Choice, Element, Group, DTDLeaf
from musicscore.dtd.note import Grace, FullNote, Cue, Duration, Instrument, EditorialVoice, Type, Dot, Accidental, \
    TimeModification, Stem, Notehead, NotheadText, Staff, Beam, Notations, Play, Lyric, Tie, DurationGroup, Note, \
    Rest
from musicscore.musicxml.elements.xml_note import XMLDuration


class TestDTDTree(TestCase):
    def setUp(self):
        self.note = Note()
        # self.dtd = (
        #     Sequence(
        #         Choice(
        #             Sequence(
        #                 Element(Grace),
        #                 Choice(
        #                     Sequence(
        #                         Group(FullNote)
        #                     ),
        #                     Sequence(
        #                         Group(FullNote),
        #                         Element(Tie, 0, 2)
        #                     ),
        #                     Sequence(
        #                         Element(Cue),
        #                         Group(FullNote)
        #                     )
        #                 )
        #             ),
        #             Sequence(
        #                 Element(Cue),
        #                 Group(FullNote),
        #                 Group(DurationGroup)
        #             ),
        #             Sequence(
        #                 Group(FullNote),
        #                 Group(DurationGroup),
        #                 Element(Tie, 0, 2)
        #             )
        #         ),
        #         Element(Instrument, 0),
        #         Group(EditorialVoice),
        #         Element(Type, 0),
        #         Element(Dot, 0, None),
        #         Element(Accidental, 0),
        #         Element(TimeModification, 0, None),
        #         Element(Stem, 0),
        #         Element(Notehead, 0),
        #         Element(NotheadText, 0),
        #         Group(Staff, 0),
        #         Element(Beam, 0, 8),
        #         Element(Notations, 0, None),
        #         Element(Lyric, 0, None),
        #         Element(Play, 0)
        #     )
        # )

    def test_expand(self):
        result = [['Grace', 'Chord', 'Pitch', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification', 'Stem',
                   'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Chord', 'Unpitched', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification', 'Stem',
                   'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Chord', 'Rest', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification', 'Stem',
                   'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Chord', 'Pitch', 'Tie', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Chord', 'Unpitched', 'Tie', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Chord', 'Rest', 'Tie', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Cue', 'Chord', 'Pitch', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Cue', 'Chord', 'Unpitched', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Cue', 'Chord', 'Rest', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Cue', 'Chord', 'Pitch', 'Duration', 'Instrument', 'Type', 'Dot', 'Accidental',
                   'TimeModification', 'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Cue', 'Chord', 'Unpitched', 'Duration', 'Instrument', 'Type', 'Dot', 'Accidental',
                   'TimeModification', 'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Cue', 'Chord', 'Rest', 'Duration', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Chord', 'Pitch', 'Duration', 'Tie', 'Instrument', 'Type', 'Dot', 'Accidental',
                   'TimeModification', 'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Chord', 'Unpitched', 'Duration', 'Tie', 'Instrument', 'Type', 'Dot', 'Accidental',
                   'TimeModification', 'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Chord', 'Rest', 'Duration', 'Tie', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play']]

        self.assertEqual([[node._type.__name__ for node in possibility] for possibility in self.note.dtd.expand()], result)
        with self.assertRaises(StopIteration):
            for i in range(16):
                if i == 0:
                    possibility = self.note.dtd.get_current_combination()
                else:
                    possibility = self.note.dtd.next()

    def test_check_type(self):
        self.note.reset_children()
        self.note.add_child(Rest())
        result = ['Grace', 'Chord', 'Rest', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification', 'Stem', 'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play']

        self.assertEqual([node._type.__name__ for node in self.note.dtd.get_current_combination()], result)

        self.note.add_child(Duration(1))
