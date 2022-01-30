from unittest import TestCase

from musicxml.exceptions import XMLElementChildrenRequired
from musicxml.xmlelement.xmlelement import *
from fractions import Fraction

from musictree.midi import Midi
from musictree.note import Note


class TestNote(TestCase):
    def test_note_init(self):
        n = Note()
        n.quarter_duration = 2
        n.midi = Midi(71)
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
        n = Note(Midi(61), quarter_duration=2, voice=2, default_x=10)
        n.xml_notehead = XMLNotehead('square')
        n.set_divisions(2)
        assert n.midi.value == 61
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
        n = Note(Midi(61), quarter_duration=Fraction(1, 3))
        assert n.get_divisions() == 3
        assert n.xml_duration.value == 1
        n.set_divisions(6)
        assert n.xml_duration.value == 2
        with self.assertRaises(ValueError):
            n.set_divisions(4)
        assert n.get_divisions() == 6

    def test_note_type(self):
        n = Note(quarter_duration=2)
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
        n.set_type('whole')
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
        n.set_type()
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
            n.type = n.set_type('bla')

    def test_note_dots(self):
        n = Note(quarter_duration=1.5)
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
        n.set_dots(0)
        assert len(n.xml_object.find_children('XMLDot')) == 0
        n.set_dots(3)
        assert len(n.xml_object.find_children('XMLDot')) == 3
        n.set_dots()
        assert len(n.xml_object.find_children('XMLDot')) == 1
        n = Note(quarter_duration=1.75)
        assert len(n.xml_object.find_children('XMLDot')) == 2

    def test_change_midi_or_duration(self):
        n = Note(Midi(61), quarter_duration=2, voice=2, default_x=10)
        n.xml_notehead = 'square'
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
        assert n.midi.parent_note == n
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
        n = Note(Midi(61), quarter_duration=0, default_x=10)
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
        n = Note(Midi(61), quarter_duration=2)
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
        n = Note()
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
