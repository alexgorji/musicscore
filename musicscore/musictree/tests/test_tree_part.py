from unittest import TestCase

from musicscore.musictree.midi import Midi
from musicscore.musictree.treebeat import TreeBeat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treenote import TreeNote
from musicscore.musictree.treepart import TreePart
from musicscore.musicxml.elements.note import Lyric
from musicscore.musicxml.types.complextypes.lyric import Text


class Test(TestCase):

    def test_beats(self):
        m = TreeMeasure(time=(3, 8, 2, 4))
        p = TreePart(id='one')
        m.add_child(p)
        p.set_beats()
        result = [0.5, 0.5, 0.5, 1.0, 1.0]
        self.assertEqual([beat.duration for beat in p.get_beats()], result)
        result = [0, 0.5, 1.0, 1.5, 2.5]
        self.assertEqual([beat.offset for beat in p.get_beats()], result)
        result = [4, 4, 4, 8, 8]
        self.assertEqual([beat.max_division for beat in p.get_beats()], result)
        p.get_beats()[3].max_division = 5
        result = [4, 4, 4, 5, 8]
        self.assertEqual([beat.max_division for beat in p.get_beats()], result)
        with self.assertRaises(ValueError):
            p.set_beats([TreeBeat(duration=0.5), TreeBeat(duration=0.5), TreeBeat(duration=0.5)])
        p.set_beats([TreeBeat(duration=1), TreeBeat(duration=0.5), TreeBeat(duration=2)])
        result = [0, 1, 1.5]
        self.assertEqual([beat.offset for beat in p.get_beats()], result)

    def test_split_notes(self):
        m = TreeMeasure(time=(3, 4))
        p = TreePart(id='one')
        m.add_child(p)
        p.set_beats()

        p.add_child(TreeNote(quarter_duration=1))
        p.add_child(TreeNote(quarter_duration=1.2))
        # p.add_child(TreeNote(quarter_duration=0.8))

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


