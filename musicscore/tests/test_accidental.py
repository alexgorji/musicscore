from unittest import TestCase

from musicscore.exceptions import MusicTreeTypeError
from musicscore.midi import Midi
from musicscore.accidental import Accidental


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
        a.mode = 'enharmonic'
        assert a.get_pitch_parameters(midi_value=61) == ('D', -1, 4)
        a.mode = 'force-flat'
        assert a.get_pitch_parameters(midi_value=61) == ('D', -1, 4)
        a.mode = 'force-sharp'
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
        midi.accidental.mode = 'force-sharp'
        assert midi.accidental.sign == 'double-sharp'
        midi.value = 60
        assert midi.accidental.sign == 'sharp'
        midi.accidental.mode = 'flat'
        assert midi.accidental.sign == 'natural'
        midi.accidental.mode = 'enharmonic'
        assert midi.accidental.sign == 'natural'
        midi.accidental.mode = 'force-flat'
        assert midi.accidental.sign == 'flat-flat'

        midi = Midi(61)
        assert midi.accidental.sign == 'sharp'
        midi.value = 60
        assert midi.accidental.sign == 'natural'

    def test_get_xml_accidental(self):
        a = Accidental()
        midi = Midi(61)
        midi.accidental.show = True
        expected = """<accidental>sharp</accidental>
"""
        assert midi.accidental.xml_object.to_string() == expected
        midi.accidental.mode = 'flat'
        expected = """<accidental>flat</accidental>
"""
        assert midi.accidental.xml_object.to_string() == expected
        midi.accidental.mode = 'force-sharp'
        expected = """<accidental>double-sharp</accidental>
"""
        assert midi.accidental.xml_object.to_string() == expected
        midi.value = 60
        expected = """<accidental>sharp</accidental>
"""
        assert midi.accidental.xml_object.to_string() == expected
        midi.value = 0
        assert midi.accidental.xml_object is None

    def test_accidental_show_mode(self):
        midi = Midi(60)
        assert midi.accidental.show is None
        assert midi.accidental.sign == 'natural'
        midi.accidental.show = True
        assert midi.accidental.xml_object.value_ == 'natural'
        midi.accidental.show = False
        assert midi.accidental.xml_object is None

        midi.accidental.show = True
        midi.value = 61
        assert midi.accidental.sign == 'sharp'
        assert midi.accidental.xml_object.value_ == 'sharp'
        midi.accidental.mode = 'flat'
        assert midi.accidental.xml_object.value_ == 'flat'
        midi.accidental.show = False
        assert midi.accidental.xml_object is None

    def test_accidental_midi(self):
        midi = Midi(61)
        assert midi.accidental.sign == 'sharp'
        midi.accidental.show = True
        assert midi.accidental.xml_object.value_ == 'sharp'

    def test_accidental_up_midi(self):
        m = Midi(70)
        assert m.accidental.up == m

    def test_accidental_copy(self):
        a = Accidental(mode='sharp', show=True)
        copied = a.__copy__()
        assert a != copied
        assert a.xml_object != copied.xml_object
        assert a.xml_object.value_ == copied.xml_object.value_
        assert a.mode == copied.mode
        assert a.show == copied.show

    def test_add_child(self):
        a = Accidental()
        with self.assertRaises(NotImplementedError):
            a.add_child(Accidental())

    def test_get_children(self):
        a = Accidental()
        assert a.get_children() == []

    def test_get_leaves(self):
        a = Accidental()
        assert a.get_leaves() == []

    def test_not_implemented_inherited_methods(self):
        a = Accidental()
        with self.assertRaises(MusicTreeTypeError):
            a.get_chord()
        with self.assertRaises(MusicTreeTypeError):
            a.get_beat()
        with self.assertRaises(MusicTreeTypeError):
            a.get_voice()
        with self.assertRaises(MusicTreeTypeError):
            a.get_staff()
        with self.assertRaises(MusicTreeTypeError):
            a.get_measure()
        with self.assertRaises(MusicTreeTypeError):
            a.get_part()
        with self.assertRaises(MusicTreeTypeError):
            a.get_beats()
        with self.assertRaises(MusicTreeTypeError):
            a.get_chords()
