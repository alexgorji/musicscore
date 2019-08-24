from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.textformatting import TextFormatting
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import String


class ComplexTypeFormattedTextId(ComplexType, String, TextFormatting, OptionalUniqueId):
    """
    The formatted-text-id type represents a text element with text-formatting and id attributes.

    """

    def __init__(self, tag, value, *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)
