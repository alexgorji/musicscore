from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeGroupSymbolValue


class ComplexTypeGroupSymbol(ComplexType, TypeGroupSymbolValue, Position, Color):
    """The group-symbol type indicates how the symbol for a group is indicated in the score."""

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
