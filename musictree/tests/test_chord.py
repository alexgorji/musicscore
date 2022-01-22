from unittest import TestCase

from quicktions import Fraction

from musictree.exceptions import MusicTreeDurationError
from musictree.midi import Midi, Accidental
from musictree.musictree import Chord, QuarterDuration, Measure
from musicxml.xmlelement.xmlelement import *


def get_chord_midi_values(chord):
    return [m.value for m in chord._midis]


class TestQuarterDuration(TestCase):
    def test_quarter_duration_comparisons(self):
        """
        Test all possible input types
        """
        qd = QuarterDuration(10)
        assert qd == 10
        qd = QuarterDuration(1.2)
        assert qd == 6 / 5
        assert qd <= 6 / 5
        assert qd >= 6 / 5
        with self.assertRaises(AssertionError):
            assert qd != 6 / 5
        with self.assertRaises(AssertionError):
            assert qd < 6 / 5
        with self.assertRaises(AssertionError):
            assert qd > 6 / 5

        qd = QuarterDuration(6 / 4)
        assert qd == 1.5
        qd = QuarterDuration(Fraction(5, 7))
        assert qd == 5 / 7
        assert QuarterDuration(1.2) < 1.3

    def test_quarter_duration_operators(self):
        assert QuarterDuration(1.2) * 5 == 6
        assert QuarterDuration(1.2) / 0.2 == 6
        assert QuarterDuration(1.2) // 0.2 == 6
        assert QuarterDuration(1.2) + 1.2 == 2.4
        assert QuarterDuration(1.2) - 0.2 == 1
        assert QuarterDuration(10) % 3 == 1
        assert QuarterDuration(10) ** 2 == 100


class TestTreeChord(TestCase):

    def test_chord_init_midis(self):
        """
        Test all possible types of input midis
        """
        ch = Chord(70, 1)
        assert get_chord_midi_values(ch) == [70]
        ch = Chord([70, 50], 1)
        assert get_chord_midi_values(ch) == [70, 50]
        ch = Chord(0, 1)
        assert get_chord_midi_values(ch) == [0]
        ch = Chord(Midi(90, accidental=Accidental(mode='enharmonic_1')), 1)
        assert get_chord_midi_values(ch) == [90]
        ch = Chord([Midi(90, accidental=Accidental(mode='enharmonic_1')), 70], 1)
        assert get_chord_midi_values(ch) == [90, 70]

        with self.assertRaises(ValueError):
            Chord([0, 60], 1)

        """
        A grace note cannot be a rest.
        """
        with self.assertRaises(ValueError):
            Chord(0, 0)

    def test_init_quarter_durations(self):
        """
        Test types and values of quarter_duration
        """
        ch = Chord(90, 1.25)
        assert ch.quarter_duration == 1.25
        ch = Chord(80, 1.2)
        assert ch.quarter_duration == 1.2
        assert ch.quarter_duration == 6 / 5
        ch = Chord(80, 8)
        assert ch.quarter_duration == 8
        with self.assertRaises(TypeError):
            ch = Chord(80, '1.2')

    def test_divisions_and_duration(self):
        """
        Each tree chord gets a parameter division to be able to determine the right value of duration of its notes ( divisions *
        quarter_duration).
        """
        ch = Chord(70, 2)
        with self.assertRaises(MusicTreeDurationError):
            ch._get_duration()
        m = Measure()
        m.add_child(ch)
        assert ch._get_duration() == 2
        m.xml_attributes.xml_divisions.value = 12
        assert ch._get_duration() == 24

    def test_is_rest(self):
        """
        Test is_rest property
        """
        assert Chord(0, 1).is_rest
        assert not Chord(50, 1).is_rest

    def test_chord_one_note(self):
        m = Measure(number='1')
        c = Chord(70, 4, relative_x=10)
        m.add_child(c)
        expected = """<measure number="1">
    <attributes>
        <divisions>1</divisions>
    </attributes>
    <note>
        <pitch>
            <step>B</step>
            <alter>-1</alter>
            <octave>4</octave>
        </pitch>
        <duration>4</duration>
        <voice>1</voice>
    </note>
</measure>
"""
        assert m.to_string() == expected
        # change quarter_duration
        xml_note = m.xml_object.find_children('XMLNote')[0]
        c.quarter_duration = 3
        assert xml_note.xml_duration.value == 3
        # change notes midi value
        c.get_notes()[0].midi.value = 72
        expected = """<pitch>
    <step>C</step>
    <alter>0</alter>
    <octave>5</octave>
</pitch>
"""
        assert c.to_string() == expected
        # change notes midi accidental mode
        c.get_notes()[0].midi.value = 73
        c.get_notes()[0].midi.accidental.mode = 'flat'
        expected = """<pitch>
            <step>D</step>
            <alter>-1</alter>
            <octave>5</octave>
        </pitch>
        """
        assert c.to_string() == expected

    def test_chord_one_note_rest(self):
        pass

    def test_chord_multiple_notes(self):
        pass

    def test_get_elements_single_non_rest(self):
        """
        Test get_elements of chord with a non rest single midi
        """
        c = Chord(72, 2)
        m = Measure()
        m.xml_attributes.xml_divisions.value = 12
        m.add_child(c)
        c.xml_voice = '1'
        c.xml_type = '16th'
        c.xml_stem = 'up'
        c.xml_staff = 1
        expected = """<note>
    <pitch>
        <step>F</step>
        <alter>1</alter>
        <octave>5</octave>
    </pitch>
    <duration>24</duration>
    <voice>1</voice>
    <type>16th</type>
    <stem>up</stem>
    <staff>1</staff>
</note>
"""
        assert c.get_xml_elements()[0].to_string() == expected

    def test_get_elements_single_non_rest_accidental(self):
        """
        Test get_elements of chord with a non rest single midi with accidental set.
        """
        chord = Chord(Midi(71, accidental=Accidental(mode='sharp')), 2)
        self.fail('Incomplete')

    def test_get_elements_rest(self):
        """
        Test get_elements of chord with a rest midi
        """
        chord = Chord(0, 2)
        self.fail('Incomplete')

    def test_get_elements_multiple_midis(self):
        """
        Test get_elements of chord with a list of midis
        """
        """<note default-x="372">
  <pitch>
    <step>D</step>
    <octave>5</octave>
  </pitch>
  <duration>24</duration>
  <voice>1</voice>
  <type>16th</type>
  <stem default-y="42">up</stem>
  <staff>1</staff>
  <beam number="1">continue</beam>
  <beam number="2">backward hook</beam>
</note>
<note default-x="372">
  <chord/>
  <pitch>
    <step>F</step>
    <alter>1</alter>
    <octave>5</octave>
  </pitch>
  <duration>24</duration>
  <voice>1</voice>
  <type>16th</type>
  <stem>up</stem>
  <staff>1</staff>
</note>
"""
        chord = Chord([60, 62, 63], 2)

        self.fail('Incomplete')
