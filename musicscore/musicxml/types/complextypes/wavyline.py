from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.attributes.trillsound import TrillSound
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeStartStopContinue, TypeNumberLevel


class ComplexTypeWavyLine(ComplexType, Position, Placement, Color, TrillSound):
    """
    Wavy lines are one way to indicate trills. When used with a barline element, they should always have
    type="continue" set.
    """

    def __init__(self, tag, type, number=1, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.type = type
        self.number = number

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
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            TypeStartStopContinue(value)
            self._ATTRIBUTES.insert(0, 'type')
            self.set_attribute('type', value)
