from musicscore import Part, QuarterDuration
from musicscore.chord import GraceChord
from musicscore.exceptions import ChordException
from musicscore.tests.util import IdTestCase
from musicxml.xmlelement.xmlelement import XMLType


class TestGraceChord(IdTestCase):
    def test_grace_chord_init(self):
        gch = GraceChord(60)
        assert gch.quarter_duration == 0
        assert isinstance(gch.quarter_duration, QuarterDuration)
        gch.quarter_duration = 0
        with self.assertRaises(ChordException):
            gch.quarter_duration = 2

    def test_grace_chord_type(self):
        p = Part('p1')
        gch = GraceChord(60)

        gch.type = '16th'
        p.add_chord(gch)
        p.finalize()
        assert p.get_chords()[0].notes[0].xml_type.value_ == '16th'
