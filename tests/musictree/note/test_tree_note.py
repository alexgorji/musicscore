from musicscore.musictree.treechord import TreeNote, TreeChord
from musicscore.musicxml.elements.fullnote import Pitch
from musicscore.musicxml.elements.note import Duration
from musicxmlunittest import XMLTestCase


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.chord = TreeChord(quarter_duration=2)
        self.note = TreeNote(parent_chord=self.chord)

    def test_1(self):
        expected = self.chord.quarter_duration
        actual = self.note.quarter_duration
        self.assertEqual(actual, expected)

    def test_2(self):
        # accidental
        self.note.accidental.show = False
        self.note.add_child(Duration(int(self.note.quarter_duration)))
        self.note.event = Pitch(step='A', alter=-1.5)
        self.note.accidental.show = True
        result = '''<note>
  <pitch>
    <step>A</step>
    <alter>-1.5</alter>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
  <accidental>three-quarters-flat</accidental>
</note>
'''
        self.assertEqual(self.note.to_string(), result)
