from musicscore.musicxml.elements.note import Note, Grace, Duration, Beam, Tie, Type, Lyric
from musicscore.musicxml.elements.fullnote import Chord, Pitch, DisplayStep, DisplayOctave, Rest
from musicscore.dtd.dtd import ChildOccurrenceDTDConflict, ChildTypeDTDConflict, ChildIsNotOptional
from unittest import TestCase


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

    def test_close(self):
        self.note.add_child(Rest())
        self.note.add_child(Grace())
        self.note.close()
        result = ['Grace', 'Chord', 'Pitch', 'Instrument', 'Type', 'Dot', 'Accidental', 'TimeModification', 'Stem',
                  'Notehead', 'NotheadText', 'Beam', 'Notations', 'Lyric', 'Play']
        self.assertEqual([node.type_.__name__ for node in self.note._DTD.get_current_combination()], result)

        self.note.reset_children()
        self.note.add_child(Rest())
        with self.assertRaises(ChildIsNotOptional):
            self.note.close()

    def test_sort_children(self):
        self.note.add_child(Pitch())
        self.note.add_child(Beam())
        self.note.add_child(Tie())
        self.note.add_child(Beam())
        self.note.add_child(Duration(1))
        self.note.add_child(Tie())
        self.note.close()
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
  <grace slash="yes" make-time="101" steal-time-following="90"/>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
</note>
'''
        self.assertEqual(self.note.to_string(), result)

    def test_to_string(self):
        self.note.add_child(Pitch())
        self.note.add_child(Beam())
        self.note.add_child(Tie())
        self.note.add_child(Beam())
        self.note.add_child(Duration(1))
        self.note.add_child(Tie())
        self.note.add_child(Chord())
        self.note.close()
        result = '''<note>
  <chord/>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <tie/>
  <tie/>
  <beam/>
  <beam/>
</note>
'''
        self.assertEqual(self.note.to_string(), result)

    def test_rest(self):
        rest = self.note.add_child(Rest())
        self.note.add_child(Duration(1))
        rest.add_child(DisplayOctave(4))
        rest.add_child(DisplayStep('B'))
        result = '''<note>
  <rest>
    <display-octave>4</display-octave>
    <display-step>B</display-step>
  </rest>
  <duration>1</duration>
</note>
'''
        self.assertEqual(self.note.to_string(), result)

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
        self.note.add_child(Lyric('lyric 1'))
        self.note.add_child(Lyric('lyric 2'))
        result = '''<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <lyric>lyric 1</lyric>
  <lyric>lyric 2</lyric>
</note>
'''
