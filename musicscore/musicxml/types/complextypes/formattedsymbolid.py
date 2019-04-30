from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.symbolformatting import SymbolFormatting
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeSmulfGlyphName


class ComplexTypeFormattedSymbolId(ComplexType, TypeSmulfGlyphName, SymbolFormatting, OptionalUniqueId):
    """
    The formatted-symbol-id type represents a SMuFL musical symbol element with formatting and id attributes.

    """

    def __init__(self, tag, value=None, *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)
