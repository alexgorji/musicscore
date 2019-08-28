from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.dahsedformatting import DashedFormatting
from musicscore.musicxml.attributes.linetype import LineType
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeNumberLevel, TypeWedgeType


class Spread(AttributeAbstract):
    def __init__(self, spread=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('spread', spread, 'TypeTenths')


class Niente(AttributeAbstract):
    def __init__(self, niente=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('niente', niente, 'TypeYesNo')


class ComplexTypeWedge(ComplexType, Spread, Niente, LineType, DashedFormatting, Position, Color, OptionalUniqueId):
    """The wedge type represents crescendo and diminuendo wedge symbols. The type attribute is crescendo for the start
    of a wedge that is closed at the left side, and diminuendo for the start of a wedge that is closed on the right
    side. Spread values are measured in tenths; those at the start of a crescendo wedge or end of a diminuendo wedge are
    ignored. The niente attribute is yes if a circle appears at the point of the wedge, indicating a crescendo from
    nothing or diminuendo to nothing. It is no by default, and used only when the type is crescendo, or the type is
    stop for a wedge that began with a diminuendo type. The line-type is solid by default."""

    def __init__(self, tag, type, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.type = type

    @property
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            TypeWedgeType(value)
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
