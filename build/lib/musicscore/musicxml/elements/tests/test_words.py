from unittest import TestCase

from musicscore.musicxml.elements.fullnote import Rest
from musicscore.musicxml.groups.musicdata import Direction, Attributes
from musicscore.musicxml.elements.note import Note, Duration
from musicscore.musicxml.elements.timewise import Part
from musicscore.musicxml.types.complextypes.attributes import Divisions
from musicscore.musicxml.types.complextypes.direction import DirectionType
from musicscore.musicxml.types.complextypes.directiontype import Words

# todo: Symbol in DTD

class Test(TestCase):
    def test_1(self):
        part = Part(id='P1')
        attributes = part.add_child(Attributes())
        attributes.add_child(Divisions(2))
        d = part.add_child(Direction())
        dt = d.add_child(DirectionType())
        dt.add_child(Words(value='bla'))
        note = part.add_child(Note())
        note.add_child(Rest())
        note.add_child(Duration(8))

        result = '''<part id="P1">
  <attributes>
    <divisions>2</divisions>
  </attributes>
  <direction>
    <direction-type>
      <words>bla</words>
    </direction-type>
  </direction>
  <note>
    <rest/>
    <duration>8</duration>
  </note>
</part>
'''
        self.assertEqual(part.to_string(), result)
