from musictree import Part
from musictree.chord import GraceChord
from musictree.exceptions import ChordException
from musictree.tests.util import IdTestCase
from musicxml.xmlelement.xmlelement import XMLType


class TestGraceChord(IdTestCase):
    def test_grace_chord_init(self):
        gch = GraceChord()
        assert gch.quarter_duration == 0
        gch.quarter_duration = 0
        with self.assertRaises(ChordException):
            gch.quarter_duration = 2

    def test_grace_chord_type(self):
        p = Part('p1')
        gch = GraceChord(60)

        gch.type_ = '16th'
        assert isinstance(gch.type_, XMLType)
        gch.type_ = XMLType('eighth')
        assert isinstance(gch.type_, XMLType)
        gch.type_ = None
        assert gch.type_ is None

        gch.type_ = '16th'
        p.add_chord(gch)
        p.finalize()
        assert p.get_chords()[0].notes[0].xml_type.value_ == '16th'
