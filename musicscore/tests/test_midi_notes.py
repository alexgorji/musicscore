import inspect

from musicscore import C, B, G, Part, Chord, Score, Time
from musicscore.tests.util import TestCase, generate_path, IdTestCase
from musicxml.xmlelement.xmlelement import XMLNotehead


class TestMidiNotes(TestCase):
    def test_midi_note(self):
        m = C(4, 's')
        assert m.accidental.get_pitch_parameters() == ('C', 1, 4)
        m = C(0)
        assert m.accidental.get_pitch_parameters() == ('C', 0, 0)
        with self.assertRaises(ValueError):
            B(-1)
        with self.assertRaises(ValueError):
            G(9, 's')

    def test_midi_note_half_tone_accidentals(self):
        signs = ['double-flat', 'flat-flat', 'ff', 'bb', 'flat', 'f', 'b', 'sharp', 's', '#', 'double-sharp',
                 'sharp-sharp',
                 'ss', '##']
        for sign in signs:
            m = C(4, sign)
            if sign in ['double-flat', 'flat-flat', 'ff', 'bb']:
                assert m.value == 58
                assert m.accidental.get_pitch_parameters() == ('C', -2, 4)
                assert m.accidental.sign == 'flat-flat'

            elif sign in ['flat', 'f', 'b']:
                assert m.value == 59
                assert m.accidental.sign == 'flat'
                assert m.accidental.get_pitch_parameters() == ('C', -1, 4)
            elif sign in ['sharp', 's', '#']:
                assert m.value == 61
                assert m.accidental.sign == 'sharp'
                assert m.accidental.get_pitch_parameters() == ('C', 1, 4)
            elif sign in ['double-sharp', 'sharp-sharp', 'ss', '##']:
                assert m.value == 62
                assert m.accidental.sign == 'double-sharp'
                assert m.accidental.get_pitch_parameters() == ('C', 2, 4)

    def test_midi_note_quarter_tones(self):
        m1 = C(4, 'three-quarters-flat')
        assert m1.value == 60 - 3 / 2
        assert m1.accidental.sign == 'three-quarters-flat'
        assert m1.accidental.get_pitch_parameters() == ('C', -1.5, 4)
        m2 = C(4, 'quarter-flat')
        m3 = C(4, 'quarter-sharp')
        m4 = C(4, 'three-quarters-sharp')

    def test_midi_note_copy(self):
        m = C(4, '#')
        m.add_tie('start')
        copied = m.__copy__()
        assert m != copied
        assert m.value == copied.value
        assert id(m.accidental) == id(copied.accidental)
        assert id(m._ties) == id(copied._ties)

        copied = m.__deepcopy__()
        assert m != copied
        assert m.value == copied.value
        assert m.accidental != copied.accidental
        assert m.accidental.mode == copied.accidental.mode
        assert m.accidental.show == copied.accidental.show
        assert id(m._ties) != id(copied._ties)
        assert m._ties == copied._ties

        copied = m._copy_for_split()
        assert m != copied
        assert m.value == copied.value
        assert m.accidental != copied.accidental
        assert m.accidental.mode == copied.accidental.mode
        assert m.accidental.show == copied.accidental.show
        assert id(m._ties) != id(copied._ties)
        assert m._ties != copied._ties

        #
        # copied = m.__deepcopy__()
        # assert m != copied
        # assert m.value == copied.value
        # assert m.accidental != copied.accidental
        # assert m.accidental.mode == copied.accidental.mode
        # assert m.accidental.show == copied.accidental.show





class TestMidiNoteNoteHead(IdTestCase):
    def test_notehead_property(self):
        m = C(4)
        m.notehead = 'square'
        assert isinstance(m.notehead, XMLNotehead)
        assert m.notehead.value_ == 'square'

    def test_notehead_after_finalize(self):
        p = Part('p1')
        ch = Chord(C(4), 1)
        ch.midis[0].notehead = 'square'
        p.add_chord(ch)
        p.finalize()
        assert ch.midis[0].parent_note.xml_notehead.value_ == 'square'

    def test_notehead_copy_for_split(self):
        midi = C(4)
        midi.notehead = 'square'
        copied = midi._copy_for_split()
        assert copied.notehead.value_ == 'square'

    def test_midi_note_notehead_after_split(self):
        s = Score()
        p = s.add_part('p1')
        ch = Chord(C(4), 3)
        ch.midis[0].notehead = 'square'
        p.add_measure(Time(2, 4))
        p.add_chord(ch)
        path = generate_path(inspect.currentframe())
        s.export_xml(path)
        assert p.get_chords()[1].midis[0].notehead.value_ == 'square'
        assert p.get_chords()[1].midis[0].parent_note.xml_notehead.value_ == 'square'