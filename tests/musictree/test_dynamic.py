from unittest import TestCase

from musicscore.musictree.treechord import TreeChord
from musicscore.musicxml.elements.note import Notations, Duration
from musicscore.musicxml.types.complextypes.dynamics import FF
from musicscore.musicxml.types.complextypes.notations import Dynamics


class Test(TestCase):

    def test_1(self):
        chord = TreeChord()
        notations = chord.add_child(Notations())
        dynamics = notations.add_child(Dynamics())
        dynamics.add_child(FF())
        note = chord._notes[0]
        note.add_child(Duration(1))
        result = '''<note>
  <pitch>
    <step>B</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <notations>
    <dynamics placement="below">
      <ff/>
    </dynamics>
  </notations>
</note>
'''
        self.assertEqual(note.to_string(), result)

    def test_2(self):
        chord = TreeChord()
        chord.add_dynamics('fp')
        chord.add_dynamics('pp')
        note = chord._notes[0]
        note.add_child(Duration(1))
        result = '''<note>
  <pitch>
    <step>B</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <notations>
    <dynamics placement="below">
      <fp/>
    </dynamics>
    <dynamics placement="below">
      <pp/>
    </dynamics>
  </notations>
</note>
'''
        self.assertEqual(note.to_string(), result)

        with self.assertRaises(ValueError):
            chord.add_dynamics('mmf')

    def test_3(self):
        chord = TreeChord()
        d = chord.add_dynamics('pp')
        d.relative_x = 10
        d.valign = 'middle'
        d.halign = 'center'
        note = chord._notes[0]
        note.add_child(Duration(1))

        result = '''<note>
  <pitch>
    <step>B</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <notations>
    <dynamics relative-x="10" halign="center" valign="middle" placement="below">
      <pp/>
    </dynamics>
  </notations>
</note>
'''
        self.assertEqual(note.to_string(), result)
