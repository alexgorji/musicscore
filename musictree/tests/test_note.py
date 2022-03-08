from unittest import TestCase
from unittest.mock import patch, Mock

from musictree.chord import Chord
from musictree.part import Part
from musicxml.exceptions import XMLElementChildrenRequired
from musicxml.xmlelement.xmlelement import *
from quicktions import Fraction

from musictree.midi import Midi
from musictree.note import Note, tie, untie


class NoteTestCase(TestCase):
    def setUp(self) -> None:
        self.mock_chord = Mock()
        self.mock_chord.get_voice_number.return_value = 1
        self.mock_chord.get_staff_number.return_value = None
        self.mock_measure = Mock()
        self.mock_measure.get_divisions.return_value = 1
        self.mock_chord.get_parent_measure.return_value = self.mock_measure

    def tearDown(self):
        patch.stopall()


class TestNote(NoteTestCase):

    def test_mock_chord(self):
        assert self.mock_chord.get_voice_number() == 1
        assert self.mock_chord.get_staff_number() is None
        assert self.mock_chord.get_parent_measure().get_divisions() == 1

    def test_note_init(self):
        n = Note(parent_chord=self.mock_chord)
        n.quarter_duration = 2
        n.midi = Midi(71)
        n.midi.accidental.show = False
        expected = """<note>
  <pitch>
    <step>B</step>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
  <voice>1</voice>
  <type>half</type>
</note>
"""
        assert n.to_string() == expected
        self.mock_chord.get_voice_number.return_value = 2
        n = Note(parent_chord=self.mock_chord, midi=Midi(61), default_x=10)
        self.mock_measure.get_divisions.return_value = 2
        n.quarter_duration = 2
        n.xml_notehead = XMLNotehead('square')
        assert n.midi.value == 61
        n.midi.accidental.show = True
        expected = """<note default-x="10">
  <pitch>
    <step>C</step>
    <alter>1</alter>
    <octave>4</octave>
  </pitch>
  <duration>4</duration>
  <voice>2</voice>
  <type>half</type>
  <accidental>sharp</accidental>
  <notehead>square</notehead>
</note>
"""
        assert n.to_string() == expected

    def test_note_set_divisions(self):
        self.mock_measure.get_divisions.return_value = 3
        n = Note(parent_chord=self.mock_chord, midi=Midi(61), quarter_duration=Fraction(1, 3))
        assert n.xml_duration.value_ == 1
        self.mock_measure.get_divisions.return_value = 6
        n._update_xml_duration()
        assert n.xml_duration.value_ == 2

    def test_note_type(self):
        n = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=2)
        n.midi.accidental.show = False
        expected = """<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
  <voice>1</voice>
  <type>half</type>
</note>
"""
        assert n.to_string() == expected
        n.update_type('whole')
        expected = """<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
  <voice>1</voice>
  <type>whole</type>
</note>
"""
        assert n.to_string() == expected
        n.update_type()
        expected = """<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
  <voice>1</voice>
  <type>half</type>
</note>
"""
        assert n.to_string() == expected
        with self.assertRaises(ValueError):
            n.type = n.update_type('bla')

    def test_note_dots(self):
        self.mock_measure.get_divisions.return_value = 2
        n = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1.5)
        n.update_dots(1)
        n.midi.accidental.show = False
        expected = """<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>3</duration>
  <voice>1</voice>
  <type>quarter</type>
  <dot />
</note>
"""
        assert n.to_string() == expected
        assert len(n.xml_object.find_children('XMLDot')) == 1
        n.update_dots(0)
        assert len(n.xml_object.find_children('XMLDot')) == 0
        n.update_dots(3)
        assert len(n.xml_object.find_children('XMLDot')) == 3
        n.update_dots(1)
        assert len(n.xml_object.find_children('XMLDot')) == 1
        self.mock_measure.get_divisions.return_value = 4
        n.quarter_duration = 1.75
        n.update_dots(2)
        assert len(n.xml_object.find_children('XMLDot')) == 2

    def test_change_midi_or_duration(self):
        self.mock_chord.get_voice_number.return_value = 2
        n = Note(parent_chord=self.mock_chord, midi=Midi(61), quarter_duration=2, default_x=10)
        n.midi.accidental.show = True
        n.xml_notehead = 'square'
        n.midi.accidental.show = True
        expected = """<note default-x="10">
  <pitch>
    <step>C</step>
    <alter>1</alter>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
  <voice>2</voice>
  <type>half</type>
  <accidental>sharp</accidental>
  <notehead>square</notehead>
</note>
"""
        assert n.to_string() == expected
        n.midi.value = 62
        n.midi.accidental.show = False
        expected = """<note default-x="10">
  <pitch>
    <step>D</step>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
  <voice>2</voice>
  <type>half</type>
  <notehead>square</notehead>
</note>
"""
        assert n.midi.up == n
        assert n.to_string() == expected
        n.midi.value = 0
        expected = """<note default-x="10">
  <rest />
  <duration>2</duration>
  <voice>2</voice>
  <type>half</type>
</note>
"""
        assert n.to_string() == expected
        n.midi.value = 72
        n.xml_notehead = XMLNotehead('diamond')
        expected = """<note default-x="10">
  <pitch>
    <step>C</step>
    <octave>5</octave>
  </pitch>
  <duration>2</duration>
  <voice>2</voice>
  <type>half</type>
  <notehead>diamond</notehead>
</note>
"""
        assert n.to_string() == expected
        n.midi.value = 0
        expected = """<note default-x="10">
  <rest />
  <duration>2</duration>
  <voice>2</voice>
  <type>half</type>
</note>
"""
        assert n.to_string() == expected
        n.midi = None
        with self.assertRaises(XMLElementChildrenRequired):
            n.to_string()
        n.midi = Midi(80)
        n.midi.accidental.show = True
        n.quarter_duration = 0
        expected = """<note default-x="10">
  <grace />
  <pitch>
    <step>A</step>
    <alter>-1</alter>
    <octave>5</octave>
  </pitch>
  <voice>2</voice>
  <accidental>flat</accidental>
</note>
"""
        assert n.to_string() == expected
        with self.assertRaises(ValueError):
            n.midi = 0

    def test_grace_note(self):
        n = Note(parent_chord=self.mock_chord, midi=Midi(61), quarter_duration=0, default_x=10)
        n.midi.accidental.show = True
        n.xml_notehead = XMLNotehead('square')
        expected = """<note default-x="10">
  <grace />
  <pitch>
    <step>C</step>
    <alter>1</alter>
    <octave>4</octave>
  </pitch>
  <voice>1</voice>
  <accidental>sharp</accidental>
  <notehead>square</notehead>
</note>
"""
        assert n.xml_object.to_string() == expected

    def test_cue_note(self):
        n = Note(parent_chord=self.mock_chord, midi=Midi(61), quarter_duration=2)
        n.midi.accidental.show = True
        n.xml_cue = XMLCue()
        expected = """<note>
  <cue />
  <pitch>
    <step>C</step>
    <alter>1</alter>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
  <voice>1</voice>
  <type>half</type>
  <accidental>sharp</accidental>
</note>
"""
        assert n.xml_object.to_string() == expected

    def test_note_stem(self):
        n = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)
        n.midi.accidental.show = False
        n.xml_stem = 'up'
        expected = """<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <voice>1</voice>
  <type>quarter</type>
  <stem>up</stem>
</note>
"""
        assert n.to_string() == expected

    def test_note_hide_show_accidental(self):
        n = Note(parent_chord=self.mock_chord, midi=Midi(60))
        n.midi.accidental.show = True
        assert n.xml_accidental.value_ == 'natural'
        n.midi.accidental.show = False
        assert n.midi.accidental.xml_object is None
        assert n.xml_object.xml_accidental is None

    def test_note_up_chord(self):
        self.mock_chord.get_voice_number.return_value = 1
        n = Note(parent_chord=self.mock_chord, midi=Midi(61), quarter_duration=1)
        assert n.up == self.mock_chord

    def test_note_midi_change_accidental_show(self):
        self.mock_chord.get_voice_number.return_value = 1
        n = Note(parent_chord=self.mock_chord, midi=Midi(61), quarter_duration=2, default_x=10)
        n.midi.accidental.show = True
        assert n.xml_object.xml_accidental == n.midi.accidental.xml_object
        assert n.xml_object.xml_accidental.value_ == n.midi.accidental.xml_object.value_ == 'sharp'
        n.midi.value = 62
        assert n.xml_object.xml_accidental.value_ == n.midi.accidental.xml_object.value_ == 'natural'
        n.midi.accidental.show = False
        assert n.xml_object.xml_accidental == n.midi.accidental.xml_object

    def test_note_update_xml_notations(self):
        n = Note(parent_chord=self.mock_chord)
        n.get_or_create_xml_notations()
        n.xml_notations.xml_articulations = XMLArticulations()
        accent = n.xml_notations.xml_articulations.add_child(XMLAccent())
        staccato = n.xml_notations.xml_articulations.add_child(XMLStaccato())
        n.xml_notations.xml_technical = XMLTechnical()
        string = n.xml_notations.xml_technical.add_child(XMLString(1))
        assert len(n.xml_notations.get_children()) == 2
        assert len(n.xml_notations.xml_articulations.get_children()) == 2
        assert len(n.xml_notations.xml_technical.get_children()) == 1

        n.xml_notations.xml_articulations.remove(accent)
        assert len(n.xml_notations.get_children()) == 2
        assert len(n.xml_notations.xml_articulations.get_children()) == 1
        assert len(n.xml_notations.xml_technical.get_children()) == 1

        n.xml_notations.xml_articulations.remove(staccato)

        assert len(n.xml_notations.get_children()) == 2
        assert len(n.xml_notations.xml_articulations.get_children()) == 0
        assert len(n.xml_notations.xml_technical.get_children()) == 1

        n.update_xml_notations()
        assert len(n.xml_notations.get_children()) == 1
        assert n.xml_notations.xml_articulations is None
        assert len(n.xml_notations.xml_technical.get_children()) == 1

        n.xml_notations.xml_technical.remove(string)
        assert len(n.xml_notations.get_children()) == 1
        assert n.xml_notations.xml_articulations is None
        assert len(n.xml_notations.xml_technical.get_children()) == 0

        n.update_xml_notations()
        assert n.xml_notations is None


standard_note_xml = """<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <voice>1</voice>
  <type>quarter</type>
</note>
"""
standard_note_xml_start_tie = """<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <tie type="start" />
  <voice>1</voice>
  <type>quarter</type>
  <notations>
    <tied type="start" />
  </notations>
</note>
"""

standard_note_xml_stop_tie = """<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <tie type="stop" />
  <voice>1</voice>
  <type>quarter</type>
  <notations>
    <tied type="stop" />
  </notations>
</note>
"""
standard_note_xml_stop_start_tie = """<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <tie type="stop" />
  <tie type="start" />
  <voice>1</voice>
  <type>quarter</type>
  <notations>
    <tied type="stop" />
    <tied type="start" />
  </notations>
</note>
"""


class TestNoteTie(NoteTestCase):
    def test_tie_manually(self):
        n = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)
        n.xml_object.add_child(XMLTie(type='start'))
        n.xml_notations = XMLNotations()
        n.xml_notations.add_child(XMLTied(type='start'))
        assert n.is_tied
        assert not n.is_tied_to_previous
        assert n.to_string() == standard_note_xml_start_tie

    def test_start_tie(self):
        n = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)
        n.start_tie()
        assert n.is_tied
        assert not n.is_tied_to_previous
        assert n.to_string() == standard_note_xml_start_tie
        n.remove_tie()
        assert not n.is_tied
        assert not n.is_tied_to_previous
        assert n.to_string() == standard_note_xml

    def test_stop_tie(self):
        n = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)
        n.stop_tie()
        assert not n.is_tied
        assert n.is_tied_to_previous
        assert n.to_string() == standard_note_xml_stop_tie
        n.remove_tie()
        assert not n.is_tied
        assert not n.is_tied_to_previous
        assert n.to_string() == standard_note_xml

    def test_start_stop_tie(self):
        n = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)
        n.start_tie()
        n.stop_tie()
        assert n.is_tied
        assert n.is_tied_to_previous
        assert n.to_string() == standard_note_xml_stop_start_tie

        n.remove_tie('start')
        assert not n.is_tied
        assert n.is_tied_to_previous
        assert n.to_string() == standard_note_xml_stop_tie
        n.remove_tie()
        assert not n.is_tied
        assert not n.is_tied_to_previous
        assert n.to_string() == standard_note_xml

    # def test_tie_accidentals(self):
    #     n = Note(parent_chord=self.mock_chord, midi=61, quarter_duration=1)
    #     n.stop_tie()
    #     n.start_tie()
    #     assert n.midi.accidental.show is False
    #     assert n.xml_object.xml_accidental is None
    #
    #     n.remove_tie('start')
    #     assert n.midi.accidental.show is False
    #     n.remove_tie()
    #     assert n.midi.accidental.show is None

    def test_tie_untie_one_note(self):
        n = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)
        tie(n)
        assert n.to_string() == standard_note_xml_start_tie
        untie(n)
        assert n.to_string() == standard_note_xml

    def test_tie_untie_two_notes(self):
        n1 = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)
        n2 = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)

        tie(n1, n2)
        assert n1.to_string() + n2.to_string() == standard_note_xml_start_tie + standard_note_xml_stop_tie
        untie(n1, n2)
        assert n1.to_string() + n2.to_string() == standard_note_xml + standard_note_xml

    def test_tie_untie_tree_or_more_notes(self):
        n1 = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)
        n2 = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)
        n3 = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)
        n4 = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)
        tie(n1, n2, n3, n4)
        assert n1.to_string() + n2.to_string() + n3.to_string() + n4.to_string() == standard_note_xml_start_tie + \
               standard_note_xml_stop_start_tie + standard_note_xml_stop_start_tie + standard_note_xml_stop_tie
        untie(n1, n2, n3, n4)
        assert n1.to_string() + n2.to_string() + n3.to_string() + n4.to_string() == standard_note_xml + standard_note_xml + \
               standard_note_xml + standard_note_xml

    def test_note_staff_number(self):
        n1 = Note(parent_chord=self.mock_chord, midi=60, quarter_duration=1)
        assert n1.get_staff_number() is None
        assert n1.xml_object.xml_staff is None
        self.mock_chord.get_staff_number.return_value = 1
        assert n1.get_staff_number() == 1
        n1._update_xml_staff()
        assert n1.xml_object.xml_staff.value_ == 1

    def test_note_parent_chord(self):
        """
        Test if parent chord of a note is its parent in the musictree
        """
        p = Part('p1')
        ch = Chord(60, 1)
        p.add_chord(ch)
        ch.final_updates()
        n = ch.notes[0]
        assert n.up == n.parent_chord
