from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.types.complextypes.complextype import ComplexType


class Type(AttributeAbstract):
    def __init__(self, type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('type', type, 'TypeStartStopContinue')


class ComplexTypeExtend(ComplexType, Type, Position, Color):
    """
    The extend type represents lyric word extension / melisma lines as well as figured bass extensions. The optional
    type and position attributes are added in Version 3.0 to provide better formatting control.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
