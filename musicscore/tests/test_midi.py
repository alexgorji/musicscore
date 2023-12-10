import inspect
from unittest import TestCase
from unittest.mock import patch

from musicscore import Chord, Part, Time, Score
from musicscore.accidental import Accidental
from musicscore.measure import Measure
from musicscore.midi import Midi
from musicscore.note import Note
from musicscore.tests.util import generate_path, IdTestCase
from musicxml.xmlelement.xmlelement import XMLPitch, XMLRest, XMLNotehead


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
        m.accidental.mode = 'enharmonic'
        assert m.accidental.get_pitch_parameters() == ('C', 0, 4)
        m.accidental.mode = 'force-flat'
        assert m.accidental.get_pitch_parameters() == ('D', -2, 4)
        m.accidental.mode = 'force-sharp'
        assert m.accidental.get_pitch_parameters() == ('B', 1, 3)

    def test_midi_rest(self):
        r = Midi(0)
        assert isinstance(r.get_pitch_or_rest(), XMLRest)
        assert r.accidental.get_pitch_parameters() is None
        assert r.get_pitch_or_rest().to_string() == '<rest />\n'

    @patch('musicscore.chord.Chord', spec=Chord)
    def test_midi_parent_note(self, mock_chord):
        """
        Test if a midi object which is being contained in a note can access it via its parent_note attribute.
        """
        mock_chord.get_staff_number.return_value = None
        mock_chord.number_of_dots = 0
        m = Midi(70)
        m._set_parent_chord(mock_chord)
        assert m.parent_note is None
        n = Note(midi=m)
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
        m.accidental.mode = 'force-flat'
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

    @patch('musicscore.chord.Chord', spec=Chord)
    def test_midi_up_note(self, mock_chord):
        mock_chord.get_staff_number.return_value = None
        mock_chord.number_of_dots = 0
        m = Midi(70)
        m._set_parent_chord(mock_chord)
        n = Note(midi=m)
        assert m.up == n

    def test_midi_tie(self):
        m1 = Midi(60)
        m2 = Midi(60)
        m1.add_tie('start')
        m2.add_tie('stop')
        m2.add_tie('start')
        assert m1._ties == {'start'}
        assert m2._ties == {'start', 'stop'}
        m2.remove_tie('start')
        assert m2._ties == {'stop'}
        m2.remove_tie('start')
        m3 = m2.__deepcopy__()
        assert m3.value == m2.value
        assert m3._ties == m2._ties
        m3.add_tie('start')
        assert m3._ties != m2._ties

    def test_is_tied_to_next_and_previous(self):
        m1 = Midi(60)
        m2 = Midi(60)
        m1.add_tie('start')
        m2.add_tie('stop')
        m2.add_tie('start')
        assert not m1.is_tied_to_previous
        assert m1.is_tied_to_next
        assert m2.is_tied_to_previous
        assert m2.is_tied_to_next

    def test_set_staff_number(self):
        midi = Midi(60)
        assert not midi.get_staff_number()
        midi.set_staff_number(2)
        assert midi.get_staff_number() == 2

class TestMidiNoteHead(IdTestCase):
    def test_notehead_property(self):
        m = Midi(60)
        m.notehead = 'square'
        assert isinstance(m.notehead, XMLNotehead)
        assert m.notehead.value_ == 'square'

    def test_notehead_after_finalize(self):
        p = Part('p1')
        ch = Chord(60, 1)
        ch.midis[0].notehead = 'square'
        p.add_chord(ch)
        p.finalize()
        assert ch.midis[0].parent_note.xml_notehead.value_ == 'square'

    def test_notehead_copy_for_split(self):
        midi = Midi(60)
        midi.notehead = 'square'
        copied = midi._copy_for_split()
        assert copied.notehead.value_ == 'square'

    def test_midi_notehead_after_split(self):
        s = Score()
        p = s.add_part('p1')
        ch = Chord(60, 3)
        ch.midis[0].notehead = 'square'
        p.add_measure(Time(2, 4))
        p.add_chord(ch)
        path = generate_path(inspect.currentframe())
        s.export_xml(path)
        assert p.get_chords()[1].midis[0].notehead.value_ == 'square'
        assert p.get_chords()[1].midis[0].parent_note.xml_notehead.value_ == 'square'

