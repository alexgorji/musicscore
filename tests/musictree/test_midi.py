from unittest import TestCase

from musicscore.musictree.midi import Midi, Accidental


class Test(TestCase):
    def test_1(self):
        midi = Midi(60)
        expected = '''<pitch>
  <step>C</step>
  <octave>4</octave>
</pitch>
'''
        self.assertEqual(expected, midi.get_pitch_rest().to_string())

    def test_2(self):
        midi = Midi(0)
        expected = '''<rest/>
'''
        self.assertEqual(expected, midi.get_pitch_rest().to_string())

    def test_3(self):
        midi = Midi(59, accidental=Accidental(mode='enharmonic_1'))
        expected = '''<pitch>
  <step>C</step>
  <alter>-1</alter>
  <octave>4</octave>
</pitch>
'''
        self.assertEqual(expected, midi.get_pitch_rest().to_string())

    def test_4(self):
        midi = Midi(59, accidental=Accidental(mode='enharmonic_2'))
        expected = '''<pitch>
  <step>A</step>
  <alter>2</alter>
  <octave>3</octave>
</pitch>
'''
        self.assertEqual(expected, midi.get_pitch_rest().to_string())

    def test_5(self):
        midi = Midi(58, accidental=Accidental(mode='sharp'))
        expected = '''<pitch>
  <step>A</step>
  <alter>1</alter>
  <octave>3</octave>
</pitch>
'''
        self.assertEqual(expected, midi.get_pitch_rest().to_string())

    def test_6(self):
        midi = Midi(59)
        expected = 'B3'
        self.assertEqual(expected, midi.__name__)

    def test_7(self):
        midi = Midi(58)
        expected = 'Bb3'
        self.assertEqual(expected, midi.__name__)

    def test_8(self):
        midi = Midi(61)
        expected = 'C#4'
        self.assertEqual(expected, midi.__name__)

    def test_9(self):
        midi = Midi(61.5)
        expected = 'D-4'
        self.assertEqual(expected, midi.__name__)

    def test_10(self):
        midi = Midi(61.5, accidental=Accidental(mode='sharp'))
        expected = 'C#+4'
        self.assertEqual(expected, midi.__name__)

    def test_11(self):
        midi = Midi(60.5, accidental=Accidental(mode='sharp'))
        expected = 'C+4'
        self.assertEqual(expected, midi.__name__)

    def test_12(self):
        midi = Midi(60.5, accidental=Accidental(mode='flat'))
        expected = 'Db-4'
        self.assertEqual(expected, midi.__name__)
