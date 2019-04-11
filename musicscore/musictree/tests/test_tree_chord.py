from unittest import TestCase

from musicscore.musictree.midi import Midi
from musicscore.musictree.treechord import TreeChord


class TestTreeChord(TestCase):
    def setUp(self):
        self.chord = TreeChord(60, 61, quarter_duration=2)

    def test_chord(self):
        for tree_note in self.chord.tree_notes:
            tree_note.update_duration(divisions=1)
            # print(tree_note.to_string())

    def test_rest(self):
        with self.assertRaises(ValueError):
            TreeChord(0, 61, quarter_duration=2)

        chord = TreeChord(0, quarter_duration=2)
        tree_note = chord.tree_notes[0]
        tree_note.update_duration(divisions=1)

        result = '''<note>
  <rest/>
  <duration>2</duration>
</note>
'''
        self.assertEqual(tree_note.to_string(), result)

    def test_chor_midi(self):
        chord = TreeChord(Midi(63, accidental_mode='sharp'), quarter_duration=2)
        tree_note = chord.tree_notes[0]
        tree_note.update_duration(divisions=1)

        result = '''<note>
  <pitch>
    <step>D</step>
    <alter>1</alter>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
</note>
'''
        self.assertEqual(tree_note.to_string(), result)
