from unittest import TestCase

from quicktions import Fraction

from musicscore.musictree.midi import Midi, Accidental
from musicscore.musictree.treebeat import TreeBeat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart


class TestTreeChord(TestCase):
    def setUp(self):
        self.chord = TreeChord((60, 61), quarter_duration=2)

    def test_chord(self):
        for tree_note in self.chord.notes:
            tree_note.update_duration(divisions=1)
            # print(tree_note.to_string())

    def test_rest(self):
        with self.assertRaises(ValueError):
            TreeChord((0, 61), quarter_duration=2)

        chord = TreeChord(0, quarter_duration=2)
        tree_note = chord.notes[0]
        tree_note.update_duration(divisions=1)

        result = '''<note>
  <rest/>
  <duration>2</duration>
</note>
'''
        self.assertEqual(tree_note.to_string(), result)

    def test_chord_midi(self):
        chord = TreeChord(Midi(63, accidental = Accidental(mode='sharp')), quarter_duration=2)
        tree_note = chord.notes[0]
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

    def test_split_chord(self):
        b = TreeBeat()
        p = TreePart('one')
        chord = TreeChord((60, 62), quarter_duration=1)
        m = TreeMeasure()
        m.add_child(p)
        p.add_chord(chord)
        b.add_chord(chord)
        split = chord.split([1, 0.5, 3])

        result = [Fraction(2, 9), Fraction(1, 9), Fraction(2, 3)]
        self.assertEqual([chord.quarter_duration for chord in split], result)
