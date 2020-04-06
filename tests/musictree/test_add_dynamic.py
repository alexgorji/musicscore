import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.elements.note import Notations, Duration
from musicscore.musicxml.types.complextypes.dynamics import FF, Dynamics
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):

    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        chord = TreeChord()
        notations = chord.add_child(Notations())
        dynamics = notations.add_child(Dynamics())
        dynamics.add_child(FF())
        note = chord.notes[0]
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
        sf = SimpleFormat(quarter_durations=[1, 1])

        sf.chords[0].add_dynamics('fff')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

#         result = '''<note>
#   <pitch>
#     <step>B</step>
#     <octave>4</octave>
#   </pitch>
#   <duration>1</duration>
#   <notations>
#     <dynamics placement="below">
#       <ff/>
#     </dynamics>
#   </notations>
# </note>
# '''
#         self.assertEqual(note.to_string(), result)

#     def test_2(self):
#         chord = TreeChord()
#         chord.add_dynamics('fp')
#         chord.add_dynamics('pp')
#         note = chord._notes[0]
#         note.add_child(Duration(1))
#         result = '''<note>
#   <pitch>
#     <step>B</step>
#     <octave>4</octave>
#   </pitch>
#   <duration>1</duration>
#   <notations>
#     <dynamics placement="below">
#       <fp/>
#     </dynamics>
#     <dynamics placement="below">
#       <pp/>
#     </dynamics>
#   </notations>
# </note>
# '''
#         self.assertEqual(note.to_string(), result)
#
#         with self.assertRaises(ValueError):
#             chord.add_dynamics('mmf')
#
#     def test_3(self):
#         chord = TreeChord()
#         d = chord.add_dynamics('pp')
#         d.relative_x = 10
#         d.valign = 'middle'
#         d.halign = 'center'
#         note = chord._notes[0]
#         note.add_child(Duration(1))
#
#         result = '''<note>
#   <pitch>
#     <step>B</step>
#     <octave>4</octave>
#   </pitch>
#   <duration>1</duration>
#   <notations>
#     <dynamics relative-x="10" halign="center" valign="middle" placement="below">
#       <pp/>
#     </dynamics>
#   </notations>
# </note>
# '''
#         self.assertEqual(note.to_string(), result)
