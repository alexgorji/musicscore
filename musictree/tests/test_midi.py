from unittest import TestCase

from musicxml.xmlelement.xmlelement import XMLPitch, XMLRest

from musictree.midi import Midi, C, B, G


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
        assert (m.accidental.mode, m.accidental.force_hide, m.accidental.force_show) == ('standard', False, False)
        assert not m.notehead
        assert m.name == 'Ab5'
        with self.assertRaises(AttributeError):
            m.value = 90

        assert m.get_pitch_parameters() == ('A', -1, 5)
        assert isinstance(m.get_pitch_or_rest(), XMLPitch)
        expected = """<pitch>
    <step>A</step>
    <alter>-1</alter>
    <octave>5</octave>
</pitch>
"""
        assert m.get_pitch_or_rest().to_string() == expected

    def test_midi_note(self):
        m = C(4, 's')
        assert m.get_pitch_parameters() == ('C', 1, 4)
        m = C(0)
        assert m.get_pitch_parameters() == ('C', 0, 0)
        with self.assertRaises(ValueError):
            B(-1)
        with self.assertRaises(ValueError):
            G(9, 's')

    def test_midi_rest(self):
        r = Midi(0)
        assert isinstance(r.get_pitch_or_rest(), XMLRest)
        assert r.get_pitch_parameters() is None
        assert r.get_pitch_or_rest().to_string() == '<rest />\n'
