from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, TypeLineEnd
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.dahsedformatting import DashedFormatting
from musicscore.musicxml.attributes.linetype import LineType
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeNumberLevel, TypeStartStopContinue


class LineEnd(AttributeAbstract):
    """"""

    def __init__(self, line_end, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('line-end', line_end, 'TypeLineEnd')
        TypeLineEnd


class EndLength(AttributeAbstract):
    """"""

    def __init__(self, end_length=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('end-length', end_length, 'TypeTenth')


class ComplexTypeBracket(ComplexType, LineEnd, EndLength, LineType, DashedFormatting, Position, Color,
                         OptionalUniqueId):

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
