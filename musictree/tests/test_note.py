from unittest import TestCase

from musictree.midi import Midi, Accidental
from musictree.musictree import Note, Chord
from musicxml.xmlelement.xmlelement import *
from musicxml.exceptions import XMLElementChildrenRequired


class TestNote(TestCase):
    def test_not_init(self):
        n = Note()
        with self.assertRaises(XMLElementChildrenRequired):
            n.to_string()
        n.duration = 2
        with self.assertRaises(XMLElementChildrenRequired):
            n.to_string()
        n.midi = Midi(71)
        expected = """<note>
    <pitch>
        <step>B</step>
        <octave>4</octave>
    </pitch>
    <duration>2</duration>
    <voice>1</voice>
</note>
"""
        assert n.to_string() == expected
        n = Note(Midi(61), duration=2, voice=2, default_x=10)
        n.xml_notehead = XMLNotehead('square')
        assert n.midi.value == 61
        expected = """<note default-x="10">
    <pitch>
        <step>C</step>
        <alter>1</alter>
        <octave>4</octave>
    </pitch>
    <duration>2</duration>
    <voice>2</voice>
    <notehead>square</notehead>
</note>
"""
        assert n.to_string() == expected

    def test_note_type(self):
        n = Note(Midi(61), duration=2)
        expected = """<note default-x="10">
    <pitch>
        <step>C</step>
        <alter>1</alter>
        <octave>4</octave>
    </pitch>
    <duration>2</duration>
    <type>half</type>
</note>
"""
        assert n.to_string() == expected
        n.type = 'whole'
        expected = """<note default-x="10">
    <pitch>
        <step>C</step>
        <alter>1</alter>
        <octave>4</octave>
    </pitch>
    <duration>2</duration>
    <type>whole</type>
</note>
"""
        assert n.to_string() == expected
        n.type = 'auto'
        expected = """<note default-x="10">
    <pitch>
        <step>C</step>
        <alter>1</alter>
        <octave>4</octave>
    </pitch>
    <duration>2</duration>
    <type>half</type>
</note>
"""
        assert n.to_string() == expected
        n.type = None
        expected = """<note default-x="10">
    <pitch>
        <step>C</step>
        <alter>1</alter>
        <octave>4</octave>
    </pitch>
    <duration>2</duration>
</note>
"""
        assert n.to_string() == expected
        with self.assertRaises(ValueError):
            n.type = 'bla'

    def test_note_dots(self):
        n = Note(Midi(61), duration=2)

    def test_change_midi_or_duration(self):
        n = Note(Midi(61), duration=2, voice=2, default_x=10)
        n.xml_notehead = 'square'
        expected = """<note default-x="10">
    <pitch>
        <step>C</step>
        <alter>1</alter>
        <octave>4</octave>
    </pitch>
    <duration>2</duration>
    <voice>2</voice>
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
    <notehead>diamond</notehead>
</note>
"""
        assert n.to_string() == expected
        n.midi.value = 0
        expected = """<note default-x="10">
    <rest />
    <duration>2</duration>
    <voice>2</voice>
</note>
"""
        assert n.to_string() == expected
        n.midi = None
        with self.assertRaises(XMLElementChildrenRequired):
            n.to_string()
        n.midi = Midi(80)
        n.duration = 0
        expected = """<note default-x="10">
    <grace />
    <pitch>
        <step>A</step>
        <alter>-1</alter>
        <octave>5</octave>
    </pitch>
    <voice>2</voice>
</note>
"""
        assert n.to_string() == expected
        with self.assertRaises(ValueError):
            n.midi = 0

    def test_note_init(self):
        n = Note(Midi(61), duration=2, voice=2, default_x=10)
        n.xml_notehead = XMLNotehead('square')
        assert n.midi.value == 61
        expected = """<note default-x="10">
    <pitch>
        <step>C</step>
        <alter>1</alter>
        <octave>4</octave>
    </pitch>
    <duration>2</duration>
    <voice>2</voice>
    <notehead>square</notehead>
</note>
"""
        assert n.xml_object.to_string() == expected

    def test_grace_note(self):
        n = Note(Midi(61), duration=0, default_x=10)
        n.xml_notehead = XMLNotehead('square')
        expected = """<note default-x="10">
    <grace />
    <pitch>
        <step>C</step>
        <alter>1</alter>
        <octave>4</octave>
    </pitch>
    <voice>1</voice>
    <notehead>square</notehead>
</note>
"""
        assert n.xml_object.to_string() == expected

    def test_cue_note(self):
        n = Note(Midi(61), duration=2)
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
</note>
"""
        assert n.xml_object.to_string() == expected
