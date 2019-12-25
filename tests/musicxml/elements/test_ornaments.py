from unittest import TestCase

from musicscore.musicxml.elements.note import Notations
from musicscore.musicxml.types.complextypes.notations import Ornaments
from musicscore.musicxml.types.complextypes.ornaments import Tremolo, Turn


class Test(TestCase):
    def test_1(self):
        notations = Notations()
        ornaments = notations.add_child(Ornaments())
        ornaments.add_child(Tremolo(4))
        ornaments.add_child(Turn())
        result = '''<notations>
  <ornaments>
    <tremolo type="single">4</tremolo>
    <turn slash="no"/>
  </ornaments>
</notations>
'''
        self.assertEqual(notations.to_string(), result)
