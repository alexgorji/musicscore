from musicscore.musictree.midi import Midi
from unittest import TestCase


class TestMidi(TestCase):
    def test_midi(self):
        midi = Midi(60)
        result = '''<pitch>
  <step>C</step>
  <octave>4</octave>
</pitch>
'''
        self.assertEqual(midi.get_pitch_rest().to_string(), result)
        midi = Midi(0)
        result = '''<rest/>
'''
        self.assertEqual(midi.get_pitch_rest().to_string(), result)
        midi = Midi(59, accidental_mode='enharmonic_1')
        result = '''<pitch>
  <step>C</step>
  <alter>-1</alter>
  <octave>4</octave>
</pitch>
'''
        self.assertEqual(midi.get_pitch_rest().to_string(), result)
        midi = Midi(59, accidental_mode='enharmonic_2')
        result = '''<pitch>
  <step>A</step>
  <alter>2</alter>
  <octave>3</octave>
</pitch>
'''
        self.assertEqual(midi.get_pitch_rest().to_string(), result)
        midi = Midi(58, accidental_mode='sharp')
        result = '''<pitch>
  <step>A</step>
  <alter>1</alter>
  <octave>3</octave>
</pitch>
'''
        self.assertEqual(midi.get_pitch_rest().to_string(), result)
