from unittest import TestCase
from musicscore.musicxml.elements.note import Duration, Note
from musicscore.musicxml.elements.fullnote import Rest


class TestDTDTree(TestCase):
    def setUp(self):
        self.note = Note()

    def test_expand(self):
        result = [['Grace', 'Chord', 'Pitch', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification', 'Stem',
                   'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Chord', 'Unpitched', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification', 'Stem',
                   'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Chord', 'Rest', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification', 'Stem',
                   'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Chord', 'Pitch', 'Tie', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Chord', 'Unpitched', 'Tie', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Chord', 'Rest', 'Tie', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Cue', 'Chord', 'Pitch', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Cue', 'Chord', 'Unpitched', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Grace', 'Cue', 'Chord', 'Rest', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Cue', 'Chord', 'Pitch', 'Duration', 'Instrument', 'Type', 'Dot', 'Accidental',
                   'TimeModification', 'Stem', 'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Cue', 'Chord', 'Unpitched', 'Duration', 'Instrument', 'Type', 'Dot', 'Accidental',
                   'TimeModification', 'Stem', 'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Cue', 'Chord', 'Rest', 'Duration', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Chord', 'Pitch', 'Duration', 'Tie', 'Instrument', 'Type', 'Dot', 'Accidental',
                   'TimeModification', 'Stem', 'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Chord', 'Unpitched', 'Duration', 'Tie', 'Instrument', 'Type', 'Dot', 'Accidental',
                   'TimeModification', 'Stem', 'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play'],
                  ['Chord', 'Rest', 'Duration', 'Tie', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification',
                   'Stem', 'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play']]

        self.assertEqual([[node._type.__name__ for node in possibility] for possibility in self.note.dtd.expand()],
                         result)
        with self.assertRaises(StopIteration):
            for i in range(16):
                if i == 0:
                    self.note.dtd.get_current_combination()
                else:
                    self.note.dtd.next()

    def test_check_type(self):
        self.note.reset_children()
        self.note.add_child(Rest())
        result = ['Grace', 'Chord', 'Rest', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification', 'Stem',
                  'Notehead', 'NoteheadText', 'Beam', 'Notations', 'Lyric', 'Play']

        self.assertEqual([node._type.__name__ for node in self.note.dtd.get_current_combination()], result)

        self.note.add_child(Duration(1))
