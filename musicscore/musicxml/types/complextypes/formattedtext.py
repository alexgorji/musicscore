from musicscore.musicxml.attributes.textformatting import TextFormatting
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import String


class ComplexTypeFormattedText(ComplexType, String, TextFormatting):
    """
    The formatted-text type represents a text element with text-formatting attributes.

    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
