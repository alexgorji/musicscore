from unittest import TestCase

from quicktions import Fraction

from musicscore.musictree.treebeat import TreeBeat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.elements.note import Lyric
from musicscore.musicxml.types.complextypes.lyric import Text

import os

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):

    def setUp(self):
        m = TreeMeasure(time=(4, 4))
        self.part = TreePart(id='one')
        self.part.max_division = 8
        self.part.forbidden_divisions = []
        m.add_child(self.part)
        # self.part.set_beats()

    # def test_add_chord1(self):
    #     self.part.add_chord(TreeChord((60, 61), quarter_duration=4))
    #     self.part.chord_to_notes()
    #     note_1 = self.part.notes[0]
    #     with self.assertRaises(AttributeError):
    #         print(note_1.chord)
    #     note_2 = self.part.notes[1]
    #     self.assertEqual(type(note_2.chord).__name__, 'Chord')
    #     self.assertEqual(note_1.quarter_duration, note_2.quarter_duration, 4)

    def test_previous_chord(self):
        p = self.part
        p.add_chord(TreeChord((60, 61), quarter_duration=1))
        p.add_chord(TreeChord(62, quarter_duration=2))
        p.add_chord(TreeChord(0, quarter_duration=1))

        self.assertEqual(p.chords[0].previous_in_part_voice, None)
        self.assertEqual(id(p.chords[1].previous_in_part_voice), id(p.chords[0]))
        self.assertEqual(id(p.chords[2].previous_in_part_voice), id(p.chords[1]))

    def test_offset(self):
        p = self.part
        p.add_chord(TreeChord((60, 61), quarter_duration=1))
        p.add_chord(TreeChord(62, quarter_duration=1.75))
        p.add_chord(TreeChord(0, quarter_duration=1.25))
        result = [0, 1, 2.75]
        self.assertEqual([chord.offset for chord in p.chords], result)

    def test_split_beats(self):
        p = self.part
        p.add_chord(TreeChord((60, 61), quarter_duration=1))
        p.add_chord(TreeChord(62, quarter_duration=1.75))
        p.add_chord(TreeChord(0, quarter_duration=1.25))
        p.finish()
        # p._add_chords_to_beats()
        # p._split_chords_beatwise()
        result = [0, Fraction(1, 1), Fraction(2, 1), Fraction(11, 4), Fraction(3, 1)]
        self.assertEqual([chord.offset for chord in p.chords], result)

    def test_split_beats_2(self):
        m = TreeMeasure(time=(3, 4))
        p = TreePart(id='one')
        p.max_division = 8
        p.forbidden_divisions = []
        m.add_child(p)
        # p.set_beats()

        p.add_chord(TreeChord(60, quarter_duration=1.4))
        p.add_chord(TreeChord(60, quarter_duration=1.6))
        # p._add_chords_to_beats()
        # p._split_chords_beatwise()
        p.finish()
        result = [Fraction(1, 1), Fraction(2, 5), Fraction(3, 5), Fraction(1, 1)]
        self.assertEqual([chord.quarter_duration for chord in p.chords], result)

    def test_quantize(self):
        m = TreeMeasure(time=(4, 4))
        p = TreePart(id='one')
        p.max_division = 8
        p.forbidden_divisions = []
        m.add_child(p)
        p.add_chord(TreeChord(60, quarter_duration=1))
        p.add_chord(TreeChord(60, quarter_duration=1.2))
        p.add_chord(TreeChord(60, quarter_duration=0.3))
        p.add_chord(TreeChord(60, quarter_duration=0.2))
        p.add_chord(TreeChord(60, quarter_duration=1.3))
        p.finish()

        result = [Fraction(1, 1), Fraction(1, 1), Fraction(1, 6), Fraction(1, 3), Fraction(1, 6), Fraction(1, 3),
                  Fraction(1, 1)]
        self.assertEqual([chord.quarter_duration for chord in p.chords], result)

    def test_beats(self):
        m = TreeMeasure(time=(3, 8, 2, 4))
        p = TreePart(id='one')
        m.add_child(p)
        tree_part_voice = p.get_staff(1).get_voice(1)
        tree_part_voice.set_beats()
        result = [0.5, 0.5, 0.5, 1.0, 1.0]
        self.assertEqual([beat.duration for beat in tree_part_voice.beats], result)
        result = [0, 0.5, 1.0, 1.5, 2.5]
        self.assertEqual([beat.offset for beat in tree_part_voice.beats], result)
        # result = [4, 4, 4, 8, 8]
        # self.assertEqual([beat.max_division for beat in tree_part_voice.beats], result)
        # tree_part_voice.beats[3].max_division = 5
        # result = [4, 4, 4, 5, 8]
        # self.assertEqual([beat.max_division for beat in tree_part_voice.beats], result)
        with self.assertRaises(ValueError):
            tree_part_voice.set_beats([TreeBeat(duration=0.5), TreeBeat(duration=0.5), TreeBeat(duration=0.5)])
        tree_part_voice.set_beats([TreeBeat(duration=1), TreeBeat(duration=0.5), TreeBeat(duration=2)])
        result = [0, 1, 1.5]
        self.assertEqual([beat.offset for beat in tree_part_voice.beats], result)

    def test_split_quantize(self):
        s = TreeScoreTimewise()
        m = TreeMeasure(time=(3, 4))
        s.add_measure(m)
        s.add_part()
        # m.add_child(p)

        chord1 = s.add_chord(1, 1, TreeChord((71, 72), quarter_duration=1.3))
        l1 = Lyric()
        l1.add_child(Text('bla'))
        chord1.add_child(l1)
        s.add_chord(1, 1, TreeChord((60, 63, 65), quarter_duration=0.6))
        s.add_chord(1, 1, TreeChord(60, quarter_duration=1.1))
        s.finish()

        # print(s.to_string())
        s.write(path=path)

        result = '''<part id="one">
  <attributes>
    <divisions>1</divisions>
  </attributes>
  <note>
    <pitch>
      <step>B</step>
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
      <octave>4</octave>
    </pitch>
    <tie/>
  </note>
  <note>
    <pitch>
      <step>B</step>
      <octave>4</octave>
    </pitch>
  </note>
  <note>
    <rest/>
  </note>
</part>
'''
        # self.assertEqual(p.to_string(), result)
