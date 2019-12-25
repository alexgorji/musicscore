from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeNumberLevel, TypeUpDown


class ComplexTypeArpeggiate(ComplexType, Position, Placement, Color, OptionalUniqueId):
    """The arpeggiate type indicates that this note is part of an arpeggiated chord. The number attribute can be used to
    distinguish between two simultaneous chords arpeggiated separately (different numbers) or together (same number).
    The up-down attribute is used if there is an arrow on the arpeggio sign. By default, arpeggios go from the lowest
    to highest note."""

    def __init__(self, tag, number=1, direction='up', *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.number = number
        self.direction = direction

    @property
    def number(self):
        return self.get_attribute('number')

    @number.setter
    def number(self, value):
        if value is None:
            self.remove_attribute('number')
        else:
            TypeNumberLevel(value)
            self._ATTRIBUTES.insert(0, 'number')
            self.set_attribute('number', value)

    @property
    def direction(self):
        return self.get_attribute('direction')

    @direction.setter
    def direction(self, value):
        if value is None:
            self.remove_attribute('direction')
        else:
            TypeUpDown(value)
            self._ATTRIBUTES.insert(0, 'direction')
            self.set_attribute('direction', value)
