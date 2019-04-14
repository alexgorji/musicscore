from musicscore.musicxml.elements.note import Note, Grace, Duration, Beam, Tie, Type, Lyric
from musicscore.musicxml.elements.fullnote import Chord, Pitch, DisplayStep, DisplayOctave, Rest
from musicscore.dtd.dtd import ChildOccurrenceDTDConflict, ChildTypeDTDConflict, ChildIsNotOptional
from unittest import TestCase

from musicscore.musicxml.types.complextypes.lyric import Text


class TestNoteDTD(TestCase):
    def setUp(self):
        self.note = Note()

    def test_add_chord(self):

        ch = self.note.add_child(Chord())
        self.note.add_child(Pitch())
        self.note.add_child(Grace())
        with self.assertRaises(Exception):
            ch.add_child(Rest())

    def test_add_child_type(self):
        self.note.add_child(Pitch())
        self.note.add_child(Grace())
        with self.assertRaises(ChildTypeDTDConflict):
            self.note.add_child(Duration(1))

    def test_add_child_max_occurrence(self):
        self.note.add_child(Pitch())

        with self.assertRaises(ChildOccurrenceDTDConflict):
            self.note.add_child(Pitch())

    def test_close_1(self):
        self.note.add_child(Rest())
        self.note.add_child(Grace())
        self.note.close_dtd()
        result = ['Grace', 'Chord', 'Rest', 'Instrument', 'FootNote', 'Level', 'Voice', 'Type', 'Dot', 'Accidental',
                  'TimeModification', 'Stem', 'Notehead', 'NoteheadText', 'StaffElement', 'Beam', 'Notations', 'Lyric',
                  'Play']
        self.assertEqual([node.type_.__name__ for node in self.note.current_dtd_choice.traverse_leaves()], result)

    def test_close_2(self):
        self.note.add_child(Rest())
        with self.assertRaises(ChildIsNotOptional):
            self.note.close_dtd()

    def test_sort_children(self):
        self.note.add_child(Pitch())
        self.note.add_child(Beam('begin'))
        self.note.add_child(Tie())
        self.note.add_child(Beam('continue'))
        self.note.add_child(Duration(1))
        self.note.add_child(Tie())
        self.note.close_dtd()

        result = ['Pitch', 'Duration', 'Tie', 'Tie', 'Beam', 'Beam']
        self.assertEqual([type(child).__name__ for child in self.note.get_children()], result)

    def test_grace(self):
        self.note.add_child(Pitch())
        grace = Grace()
        grace.slash = 'yes'
        grace.make_time = 101
        with self.assertRaises(ValueError):
            grace.steal_time_following = 120

        grace.steal_time_following = 90
        self.note.add_child(grace)
        result = '''<note>
  <grace steal-time-following="90" make-time="101" slash="yes"/>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
</note>
'''
        self.assertEqual(self.note.to_string(), result)

#     def test_to_string(self):
#         self.note.add_child(Pitch())
#         self.note.add_child(Beam('begin'))
#         self.note.add_child(Tie())
#         self.note.add_child(Beam('continue'))
#         self.note.add_child(Duration(1))
#         self.note.add_child(Tie())
#         self.note.add_child(Chord())
#         self.note.close()
#         result = '''<note>
#   <chord/>
#   <pitch>
#     <step>C</step>
#     <octave>4</octave>
#   </pitch>
#   <duration>1</duration>
#   <tie/>
#   <tie/>
#   <beam number="1">begin</beam>
#   <beam number="1">continue</beam>
# </note>
# '''
#         self.assertEqual(self.note.to_string(), result)

    def test_rest(self):
        rest = self.note.add_child(Rest())
        self.note.add_child(Duration(1))
#         rest.add_child(DisplayOctave(4))
#         rest.add_child(DisplayStep('B'))
#         result = '''<note>
#   <rest>
#     <display-step>B</display-step>
#     <display-octave>4</display-octave>
#   </rest>
#   <duration>1</duration>
# </note>
# '''
#         self.assertEqual(self.note.to_string(), result)

    def test_type(self):
        self.note.add_child(Pitch())
        self.note.add_child(Duration())
        self.note.add_child(Type(value='quarter'))
        result = '''<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <type>quarter</type>
</note>
'''
        self.assertEqual(self.note.to_string(), result)

    def test_lyrics(self):
        self.note = Note()
        self.note.add_child(Pitch())
        self.note.add_child(Duration())
        self.note.add_child(Lyric()).add_child(Text('lyric 1'))
        self.note.add_child(Lyric(number='2')).add_child(Text('lyric 2'))
        result = '''<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <lyric number="1">
    <text>lyric 1</text>
  </lyric>
  <lyric number="2">
    <text>lyric 2</text>
  </lyric>
</note>
'''
        self.assertEqual(self.note.to_string(), result)
