from musicscore.musicxml.attributes.bezier import Bezier
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.dahsedformatting import DashedFormatting
from musicscore.musicxml.attributes.linetype import LineType
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.orientation import Orientation
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.types.complextypes.complextype import Empty
from musicscore.musicxml.types.simple_type import TypeStartStopContinue, TypeNumberLevel


class ComplexTypeSlur(Empty, LineType, DashedFormatting, Position, Placement, Orientation, Bezier, Color,
                      OptionalUniqueId):
    """
    Slur types are empty. Most slurs are represented with two elements: one with a start type, and one with a stop type.
    Slurs can add more elements using a continue type. This is typically used to specify the formatting of cross-system
    slurs, or to specify the shape of very complex slurs.
    """

    def __init__(self, tag, type, number=1, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.type = type
        self.number = number

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
