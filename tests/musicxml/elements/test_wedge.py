from unittest import TestCase

from musicscore.musicxml.groups.musicdata import Direction
from musicscore.musicxml.types.complextypes.direction import DirectionType
from musicscore.musicxml.types.complextypes.directiontype import Wedge


class Test(TestCase):
    def test_1(self):
        wedge_object = Wedge('crescendo')
        direction = Direction(placement='below')
        direction_type = direction.add_child(DirectionType())
        direction_type.add_child(wedge_object)

        result = """<direction placement="below">
  <direction-type>
    <wedge type="crescendo"/>
  </direction-type>
</direction>
"""
        self.assertEqual(direction.to_string(), result)
