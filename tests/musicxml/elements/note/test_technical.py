from unittest import TestCase

from musicscore.musicxml.elements.fullnote import Pitch
from musicscore.musicxml.elements.note import Note, Duration, Notations
from musicscore.musicxml.types.complextypes.hole import HoleClosed

from musicscore.musicxml.types.complextypes.notations import Technical
from musicscore.musicxml.types.complextypes.technical import Hole, SnapPizzicato


class Test(TestCase):
    def setUp(self):
        self.note = Note()
        self.note.add_child(Duration())
        self.note.add_child(Pitch())

    def test_1(self):
        notations = self.note.add_child(Notations())
        technical = notations.add_child(Technical())
        hole = technical.add_child(Hole())
        hole.add_child(HoleClosed(value='no'))
        technical.add_child(SnapPizzicato(relative_y=20))

        result = """<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <notations>
    <technical>
      <hole>
        <hole-closed>no</hole-closed>
      </hole>
      <snap-pizzicato relative-y="20"/>
    </technical>
  </notations>
</note>
"""
        self.assertEqual(self.note.to_string(), result)
