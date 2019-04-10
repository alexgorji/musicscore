from unittest import TestCase

from quicktions import Fraction

from musicscore.musictree.midi import Midi
from musicscore.musictree.treebeat import TreeBeat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treenote import TreeNote
from musicscore.musictree.treepart import TreePart
from musicscore.musicxml.elements.note import Lyric, Tie
from musicscore.musicxml.types.complextypes.lyric import Text


class Test(TestCase):

    def setUp(self):
        m = TreeMeasure(time=(4, 4))
        self.part = TreePart(id='one')
        m.add_child(self.part)
        self.part.set_beats()
        self.part.add_child(TreeNote(quarter_duration=1, event=Midi(60).get_pitch_rest()))
        self.part.add_child(TreeNote(quarter_duration=1.75, event=Midi(60).get_pitch_rest()))
        self.part.add_child(TreeNote(quarter_duration=1.25, event=Midi(60).get_pitch_rest()))

    def test_previous_note(self):
        p = self.part
        self.assertEqual(p.notes[0].previous, None)
        self.assertEqual(id(p.notes[1].previous), id(p.notes[0]))
        self.assertEqual(id(p.notes[2].previous), id(p.notes[1]))

    def test_offset(self):
        p = self.part
        result = [0, 1, 2.75]
        self.assertEqual([note.offset for note in p.notes], result)

    def test_split_beats(self):
        p = self.part
        p.add_notes_to_beats()
        p.split_notes_beatwise()

        result = [0, Fraction(1, 1), Fraction(2, 1), Fraction(11, 4), Fraction(3, 1)]
        self.assertEqual([note.offset for note in p.notes], result)
        result = [[], ['Tie'], [], ['Tie'], []]
        self.assertEqual([[type(t).__name__ for t in note.get_children_by_type(Tie)] for note in p.notes], result)

    def test_split_beats_2(self):
        m = TreeMeasure(time=(3, 4))
        p = TreePart(id='one')
        m.add_child(p)
        p.set_beats()
        p.add_child(TreeNote(quarter_duration=1.4, event=Midi(60).get_pitch_rest()))
        p.add_child(TreeNote(quarter_duration=1.6, event=Midi(60).get_pitch_rest()))
        p.add_notes_to_beats()
        p.split_notes_beatwise()
        result = [Fraction(1, 1), Fraction(2, 5), Fraction(3, 5), Fraction(1, 1)]
        self.assertEqual([note.quarter_duration for note in p.notes], result)

    def test_quantize(self):
        m = TreeMeasure(time=(4, 4))
        p = TreePart(id='one')
        m.add_child(p)
        p.set_beats()
        p.add_child(TreeNote(quarter_duration=1, event=Midi(60).get_pitch_rest()))
        p.add_child(TreeNote(quarter_duration=1.2, event=Midi(60).get_pitch_rest()))
        p.add_child(TreeNote(quarter_duration=0.3, event=Midi(60).get_pitch_rest()))
        p.add_child(TreeNote(quarter_duration=0.2, event=Midi(60).get_pitch_rest()))
        p.add_child(TreeNote(quarter_duration=1.3, event=Midi(60).get_pitch_rest()))
        p.quantize_2()
        result = [Fraction(1, 1), Fraction(1, 1), Fraction(1, 6), Fraction(1, 3), Fraction(1, 6), Fraction(1, 3), Fraction(1, 1)]
        self.assertEqual([note.quarter_duration for note in p.notes], result)
        result = [[], ['Tie'], [], [], [], ['Tie'], []]
        self.assertEqual([[type(t).__name__ for t in note.get_children_by_type(Tie)] for note in p.notes], result)


    def test_beats(self):
        m = TreeMeasure(time=(3, 8, 2, 4))
        p = TreePart(id='one')
        m.add_child(p)
        p.set_beats()
        result = [0.5, 0.5, 0.5, 1.0, 1.0]
        self.assertEqual([beat.duration for beat in p.beats], result)
        result = [0, 0.5, 1.0, 1.5, 2.5]
        self.assertEqual([beat.offset for beat in p.beats], result)
        result = [4, 4, 4, 8, 8]
        self.assertEqual([beat.max_division for beat in p.beats], result)
        p.beats[3].max_division = 5
        result = [4, 4, 4, 5, 8]
        self.assertEqual([beat.max_division for beat in p.beats], result)
        with self.assertRaises(ValueError):
            p.set_beats([TreeBeat(duration=0.5), TreeBeat(duration=0.5), TreeBeat(duration=0.5)])
        p.set_beats([TreeBeat(duration=1), TreeBeat(duration=0.5), TreeBeat(duration=2)])
        result = [0, 1, 1.5]
        self.assertEqual([beat.offset for beat in p.beats], result)

    def test_split_notes(self):
        m = TreeMeasure(time=(3, 4))
        p = TreePart(id='one')
        m.add_child(p)
        p.set_beats()

        p.add_child(TreeNote(quarter_duration=1))
        p.add_child(TreeNote(quarter_duration=1.2))

        note1 = p.get_children_by_type(TreeNote)[0]
        l1 = Lyric()
        l1.add_child(Text('bla'))
        note1.add_child(l1)
        note1.event = Midi(71).get_pitch_rest()
        p.split_note(note1, (3, 1, 2))
        result = '''<part id="one">
  <attributes>
    <divisions>1</divisions>
  </attributes>
  <note>
    <pitch>
      <step>B</step>
      <alter>0</alter>
      <octave>4</octave>
    </pitch>
    <tie/>
    <lyric number="1">
      <text>bla</text>
    </lyric>
  </note>
  <note>
    <pitch>
      <step>B</step>
      <alter>0</alter>
      <octave>4</octave>
    </pitch>
    <tie/>
  </note>
  <note>
    <pitch>
      <step>B</step>
      <alter>0</alter>
      <octave>4</octave>
    </pitch>
  </note>
  <note>
    <rest/>
  </note>
</part>
'''
        self.assertEqual(p.to_string(), result)


