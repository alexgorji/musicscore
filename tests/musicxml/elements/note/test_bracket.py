from unittest import TestCase

from musicscore.musicxml.groups.musicdata import Direction
from musicscore.musicxml.types.complextypes.direction import DirectionType
from musicscore.musicxml.types.complextypes.directiontype import Bracket


class Test(TestCase):

    def test_1(self):
        direction = Direction()
        direction_type = direction.add_child(DirectionType())
        direction_type.add_child(Bracket(type='start', line_end='arrow'))

        result = """<direction>
  <direction-type>
    <bracket number="1" type="start" line-end="arrow"/>
  </direction-type>
</direction>
"""
        self.assertEqual(direction.to_string(), result)
