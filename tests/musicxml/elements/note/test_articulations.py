from unittest import TestCase

from musicscore.musicxml.elements.fullnote import Pitch
from musicscore.musicxml.elements.note import Note, Duration, Notations
from musicscore.musicxml.groups.musicdata import Direction
from musicscore.musicxml.types.complextypes.articulations import Accent, Staccato
from musicscore.musicxml.types.complextypes.direction import DirectionType
from musicscore.musicxml.types.complextypes.directiontype import Dynamics
from musicscore.musicxml.types.complextypes.dynamics import P
from musicscore.musicxml.types.complextypes.notations import Articulations


class Test(TestCase):
    def setUp(self):
        self.note = Note()
        self.note.add_child(Duration())
        self.note.add_child(Pitch())

    def test_1(self):
        notations = self.note.add_child(Notations())
        articulations = notations.add_child(Articulations())
        articulations.add_child(Accent())
        articulations.add_child(Staccato(relative_y=20))

        result = """<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <notations>
    <articulations>
      <accent/>
      <staccato relative-y="20"/>
    </articulations>
  </notations>
</note>
"""
        self.assertEqual(self.note.to_string(), result)
