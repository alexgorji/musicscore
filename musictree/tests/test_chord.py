from unittest import TestCase

from fractions import Fraction

from musictree.midi import Midi
from musictree.accidental import Accidental
from musictree.chord import Chord


def get_chord_midi_values(chord):
    return [m.value for m in chord._midis]


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

    def test_chord_update_notes_duration(self):
        ch = Chord(70, 1)
        ch.quarter_duration = 1.5
        # assert ch.notes[0].xml_duration.value == 1

    def test_init_quarter_durations(self):
        """
        Test values of quarter_duration
        """
        ch = Chord(90, 1.25)
        assert ch.quarter_duration == 1.25
        assert ch.notes[0].quarter_duration == 1
        ch = Chord(80, 1.2)
        assert ch.quarter_duration == Fraction(1.2).limit_denominator(1000)
        assert ch.quarter_duration == Fraction(6 / 5).limit_denominator(1000)
        ch = Chord(80, 8)
        assert ch.quarter_duration == 8
        with self.assertRaises(TypeError):
            ch = Chord(80, '1.2')

    def test_is_rest(self):
        """
        Test is_rest property
        """
        assert Chord(0, 1).is_rest
        assert not Chord(50, 1).is_rest

    def test_chord_attributes(self):
        """
        Test that a dot operator can set and get note attributes
        """
        c = Chord([60, 61, 62], 2)
        c.relative_x = 10
        assert c.relative_x == [10, 10, 10]
        c.relative_y = [None, 20, 10]
        assert c.relative_y == [None, 20, 10]
        c.relative_y = [10]
        assert c.relative_y == [10, 20, 10]
        c.default_y = [10]
        assert c.default_y == [10, None, None]

    def test_chord_one_note(self):
        c = Chord(70, 4, relative_x=10)
        expected = """<note relative-x="10">
    <pitch>
        <step>B</step>
        <alter>-1</alter>
        <octave>4</octave>
    </pitch>
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
    <accidental>flat</accidental>
</note>
"""
        assert c.notes[0].to_string() == expected
        # change measures divisions
        c.notes[0].set_divisions(4)
        assert c.notes[0].xml_duration.value == 16
        # change chord's midi (non-zero)
        c.midis[0].value = 72
        expected = """<note relative-x="10">
    <pitch>
        <step>C</step>
        <octave>5</octave>
    </pitch>
    <duration>16</duration>
    <voice>1</voice>
    <type>whole</type>
</note>
"""
        assert c.notes[0].to_string() == expected
        # change chord's midi (zero)
        c.midis[0].value = 0

        expected = """<note relative-x="10">
    <rest />
    <duration>16</duration>
    <voice>1</voice>
    <type>whole</type>
</note>
"""
        assert c.notes[0].to_string() == expected
        # change chord's duration (not zero)
        c.quarter_duration = 1
        expected = """<note relative-x="10">
    <rest />
    <duration>4</duration>
    <voice>1</voice>
    <type>quarter</type>
</note>
"""
        assert c.notes[0].to_string() == expected
        # change chord's duration (zero)
        with self.assertRaises(ValueError):
            c.quarter_duration = 0
        c.midis[0].value = 60
        c.quarter_duration = 0
        expected = """<note relative-x="10">
    <grace />
    <pitch>
        <step>C</step>
        <octave>4</octave>
    </pitch>
    <voice>1</voice>
</note>
"""
        assert c.notes[0].to_string() == expected
        # change chord's attributes?
        c.notes[0].relative_x = 20
        c.notes[0].relative_y = 15
        expected = """<note relative-x="20" relative-y="15">
    <grace />
    <pitch>
        <step>C</step>
        <octave>4</octave>
    </pitch>
    <voice>1</voice>
</note>
"""
        assert c.notes[0].to_string() == expected

    def test_chord_single_non_rest(self):
        """
        Test a chord with a non rest single midi
        """
        c = Chord(72, 2)
        c.xml_voice = '1'
        c.xml_type = '16th'
        c.xml_stem = 'up'
        c.xml_staff = 1
        expected = """<note>
    <pitch>
        <step>C</step>
        <octave>5</octave>
    </pitch>
    <duration>2</duration>
    <voice>1</voice>
    <type>16th</type>
    <stem>up</stem>
    <staff>1</staff>
</note>
"""
        assert c.notes[0].to_string() == expected
        c.midis[0].value = 61
        expected = """<pitch>
    <step>C</step>
    <alter>1</alter>
    <octave>4</octave>
</pitch>
"""
        assert c.notes[0].xml_pitch.to_string() == expected
        c.midis[0].value = 0
        assert c.notes[0].xml_pitch is None
        assert c.notes[0].xml_rest is not None
        assert c.is_rest

    def test_chord_single_non_rest_midi_with_accidental(self):
        """
        Test chord with a non rest single midi with accidental set.
        """
        chord = Chord(Midi(70, accidental=Accidental(mode='sharp')), 1)
        expected = """<pitch>
        <step>A</step>
        <alter>1</alter>
        <octave>4</octave>
    </pitch>
"""
        assert chord.notes[0].xml_pitch.to_string() == expected

    def test_chord_as_rest(self):
        """
        Test chord with a rest midi
        """
        chord = Chord(0, 2)
        expected = """<note>
    <rest />
    <duration>2</duration>
    <voice>1</voice>
    <type>half</type>
</note>
"""
        assert chord.notes[0].to_string() == expected
        chord.midis = [60, 61]
        expected = """<pitch>
        <step>C</step>
        <octave>4</octave>
    </pitch>
"""
        assert chord.notes[0].xml_pitch.to_string() == expected
        expected = """<pitch>
        <step>C</step>
        <alter>1</alter>
        <octave>4</octave>
    </pitch>
"""
        assert chord.notes[1].xml_pitch.to_string() == expected
        chord.to_rest()
        expected = """<note>
    <rest />
    <duration>2</duration>
    <voice>1</voice>
    <type>half</type>
</note>
"""
        assert chord.notes[0].to_string() == expected
        assert len(chord.notes) == 1

    def test_chord_with_multiple_midis(self):
        """
        Test chord with a list of midis
        """

        chord = Chord([60, 62, 63], 2)
        chord.xml_stem = 'up'
        expected_1 = """<note>
    <pitch>
        <step>C</step>
        <octave>4</octave>
    </pitch>
    <duration>2</duration>
    <voice>1</voice>
    <type>half</type>
    <stem>up</stem>
</note>
"""
        expected_2 = """<note>
    <pitch>
        <step>D</step>
        <octave>4</octave>
    </pitch>
    <duration>2</duration>
    <voice>1</voice>
    <type>half</type>
    <stem>up</stem>
</note>
"""
        expected_3 = """<note>
    <pitch>
        <step>E</step>
        <alter>-1</alter>
        <octave>4</octave>
    </pitch>
    <duration>2</duration>
    <voice>1</voice>
    <type>half</type>
    <accidental>flat</accidental>
    <stem>up</stem>
</note>
"""
        for note, expected in zip(chord.notes, [expected_1, expected_2, expected_3]):
            assert note.to_string() == expected

    def test_chord_with_none_midis(self):
        ch = Chord(midis=None, quarter_duration=1)
        assert ch.notes == []
        ch.midis = 60
        assert len(ch.notes) == 1
        assert ch.notes[0].midi.value == 60
        ch.midis = None
        assert ch.notes == []

    def test_chord_with_none_quarter_duration(self):
        ch = Chord(midis=None, quarter_duration=None)
        assert ch.notes == []
        ch.midis = 60
        assert len(ch.notes) == 1
        assert ch.notes[0].midi.value == 60
        assert ch.notes[0].quarter_duration == Fraction(1, 1)
        ch.quarter_duration = 2
        assert len(ch.notes) == 1
        assert ch.notes[0].quarter_duration == Fraction(2, 1)
