from unittest import TestCase
import musicscore.musicxml.elements.timewise as timewise
from musicscore.musicxml.elements.fullnote import Rest
from musicscore.musicxml.elements.note import Note, Duration
from musicscore.musicxml.groups.musicdata import Attributes
from musicscore.musicxml.types.complextypes.attributes import Divisions


class TestAddNote(TestCase):
    def setUp(self):
        self.part = timewise.Part(id='p1')
        attributes = self.part.add_child(Attributes())
        attributes.add_child(Divisions(1))

    def test_add_note(self):
        note = Note()
        note.add_child(Rest())
        note.add_child(Duration(2))
        self.part.add_child(note)

        note = Note()
        note.add_child(Rest())
        note.add_child(Duration(2))
        result = '''<part id="p1">
  <attributes>
    <divisions>1</divisions>
  </attributes>
  <note>
    <rest/>
    <duration>2</duration>
  </note>
</part>
'''
        self.assertEqual(self.part.to_string(), result)
