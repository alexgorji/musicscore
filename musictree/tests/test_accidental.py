from unittest import TestCase

from musictree.midi import Midi
from musictree.accidental import Accidental


class TestAccidental(TestCase):
    def test_get_pitch_parameters(self):
        a = Accidental()
        assert a.get_pitch_parameters(midi_value=None) is None
        assert a.get_pitch_parameters(midi_value=0) is None
        assert a.get_pitch_parameters(midi_value=61) == ('C', 1, 4)
        a.mode = 'sharp'
        assert a.get_pitch_parameters(midi_value=61) == ('C', 1, 4)
        a.mode = 'flat'
        assert a.get_pitch_parameters(midi_value=61) == ('D', -1, 4)
        a.mode = 'enharmonic_1'
        assert a.get_pitch_parameters(midi_value=61) == ('D', -1, 4)
        a.mode = 'enharmonic_2'
        assert a.get_pitch_parameters(midi_value=61) == ('B', 2, 3)

        midi = Midi(61, accidental=a)
        assert a.get_pitch_parameters() == ('B', 2, 3)
        assert midi.accidental.get_pitch_parameters() == ('B', 2, 3)

    def test_accidental_sign(self):
        a = Accidental()
        assert a.sign is None
        midi = Midi(61)
        assert midi.accidental.sign == 'sharp'
        midi.accidental.mode = 'flat'
        assert midi.accidental.sign == 'flat'
        midi.accidental.mode = 'enharmonic_2'
        assert midi.accidental.sign == 'double-sharp'
        midi.value = 60
        assert midi.accidental.sign == 'flat-flat'
        midi.accidental.mode = 'flat'
        assert midi.accidental.sign == 'natural'

        midi = Midi(61)
        assert midi.accidental.sign == 'sharp'
        midi.value = 60
        assert midi.accidental.sign == 'natural'

    def test_get_xml_accidental(self):
        a = Accidental()
        assert a.xml_object is None
        midi = Midi(61)
        expected = """<accidental>sharp</accidental>
"""
        assert midi.accidental.xml_object.to_string() == expected
        midi.accidental.mode = 'flat'
        expected = """<accidental>flat</accidental>
"""
        assert midi.accidental.xml_object.to_string() == expected
        midi.accidental.mode = 'enharmonic_2'
        expected = """<accidental>double-sharp</accidental>
"""
        assert midi.accidental.xml_object.to_string() == expected
        midi.value = 60
        expected = """<accidental>flat-flat</accidental>
"""
        assert midi.accidental.xml_object.to_string() == expected
        midi.value = 0
        assert midi.accidental.xml_object is None
