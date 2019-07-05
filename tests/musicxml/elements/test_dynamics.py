from unittest import TestCase

from musicscore.musicxml.groups.musicdata import Direction
from musicscore.musicxml.types.complextypes.direction import DirectionType
from musicscore.musicxml.types.complextypes.directiontype import Dynamics
from musicscore.musicxml.types.complextypes.dynamics import P


class Test(TestCase):
    def test_1(self):
        direction = Direction()
        direction_type = direction.add_child(DirectionType())
        dynamics = direction_type.add_child(Dynamics())
        dynamics.add_child(P())
        print(direction.to_string())
