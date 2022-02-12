from unittest import TestCase
from unittest.mock import patch

from musicxml.xmlelement.xmlelement import XMLPitch, XMLRest

from musictree.accidental import Accidental
from musictree.midi import Midi, C, B, G
from musictree.note import Note
from musictree.measure import Measure


class TestMidi(TestCase):
    def test_midi_init(self):
        """
        Test that midi initiation
        """
        with self.assertRaises(TypeError):
            Midi()
        with self.assertRaises(TypeError):
            Midi('80')
        with self.assertRaises(ValueError):
            Midi(11)
        with self.assertRaises(ValueError):
            Midi(128)

        m = Midi(80)
        assert m.accidental.mode == 'standard'
        assert m.name == 'Ab5'
        assert m.accidental.get_pitch_parameters() == ('A', -1, 5)
        assert isinstance(m.get_pitch_or_rest(), XMLPitch)
        expected = """<pitch>
  <step>A</step>
  <alter>-1</alter>
  <octave>5</octave>
</pitch>
"""

        assert m.get_pitch_or_rest().to_string() == expected
        m = Midi(60)
        expected = """<pitch>
  <step>C</step>
  <octave>4</octave>
</pitch>
"""

        assert m.get_pitch_or_rest().to_string() == expected

    def test_midi_accidental_modes(self):
        m = Midi(60)
        assert m.accidental.get_pitch_parameters() == ('C', 0, 4)
        m.accidental.mode = 'enharmonic_1'
        assert m.accidental.get_pitch_parameters() == ('B', 1, 3)
        m.accidental.mode = 'enharmonic_2'
        assert m.accidental.get_pitch_parameters() == ('D', -2, 4)

    def test_midi_note(self):
        m = C(4, 's')
        assert m.accidental.get_pitch_parameters() == ('C', 1, 4)
        m = C(0)
        assert m.accidental.get_pitch_parameters() == ('C', 0, 0)
        with self.assertRaises(ValueError):
            B(-1)
        with self.assertRaises(ValueError):
            G(9, 's')

    def test_midi_rest(self):
        r = Midi(0)
        assert isinstance(r.get_pitch_or_rest(), XMLRest)
        assert r.accidental.get_pitch_parameters() is None
        assert r.get_pitch_or_rest().to_string() == '<rest />\n'

    @patch('musictree.chord.Chord')
    def test_midi_parent_note(self, mock_chord):
        """
        Test if a midi object which is being contained in a note can access it via its parent_note attribute.
        """
        mock_chord.get_staff_number.return_value = None
        m = Midi(70)
        assert m.parent_note is None
        n = Note(parent_chord=mock_chord, midi=m)
        assert m.parent_note == n
        with self.assertRaises(TypeError):
            m.parent_note = Measure()

    def test_change_midi_value_or_accidental_mode(self):
        """
        Test if changing midi value changes its pitch or rest
        """
        m = Midi(70)
        expected = """<pitch>
  <step>B</step>
  <alter>-1</alter>
  <octave>4</octave>
</pitch>
"""
        assert m.get_pitch_or_rest().to_string() == expected
        m.value = 69
        expected = """<pitch>
  <step>A</step>
  <octave>4</octave>
</pitch>
"""
        assert m.get_pitch_or_rest().to_string() == expected
        m.accidental.mode = 'enharmonic_2'
        expected = """<pitch>
  <step>B</step>
  <alter>-2</alter>
  <octave>4</octave>
</pitch>
"""
        assert m.get_pitch_or_rest().to_string() == expected

        m.value = 0
        expected = """<rest />
"""
        assert m.get_pitch_or_rest().to_string() == expected
        m.value = 61
        m.accidental.mode = 'flat'
        expected = """<pitch>
  <step>D</step>
  <alter>-1</alter>
  <octave>4</octave>
</pitch>
"""
        assert m.get_pitch_or_rest().to_string() == expected

    def test_midi_copy(self):
        m = Midi(61, accidental=Accidental(mode='sharp', show=False))
        copied = m.__deepcopy__()
        assert m != copied
        assert m.value == copied.value
        assert m.accidental != copied.accidental
        assert m.accidental.mode == copied.accidental.mode
        assert m.accidental.show == copied.accidental.show

    @patch('musictree.chord.Chord')
    def test_midi_up_note(self, mock_chord):
        mock_chord.get_staff_number.return_value = None
        m = Midi(70)
        n = Note(parent_chord=mock_chord, midi=m)
        assert m.up == n
