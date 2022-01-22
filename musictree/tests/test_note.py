from unittest import TestCase

from musictree.midi import Midi
from musictree.musictree import Note
from musicxml.xmlelement.xmlelement import *


class TestNote(TestCase):
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

    def test_changing_duration(self):
        n = Note()
