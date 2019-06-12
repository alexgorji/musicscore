from unittest import TestCase
from musicscore.musictree.treenote import TreeNote
from musicscore.musicxml.elements.fullnote import Pitch
from musicscore.musicxml.elements.note import Duration


class TestTreeNote(TestCase):
    def setUp(self):
        self.note = TreeNote()

    def test_quarter_duration(self):
        self.note.add_child(Duration(int(self.note.quarter_duration)))
        result = ['Rest', 'Duration']
        self.assertEqual([type(child).__name__ for child in self.note.get_children()], result)
        self.note.quarter_duration = 0
        # result = ['Grace', 'Rest']
        # self.assertEqual([type(child).__name__ for child in self.note.get_children()], result)

    def test_duration(self):
        self.note.quarter_duration = 2
        self.note.update_duration(4)

        self.assertEqual(self.note.duration.value, 8)

    def test_accidental(self):
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
  <duration>1</duration>
  <accidental>three-quarters-flat</accidental>
</note>
'''
        self.assertEqual(self.note.to_string(), result)


