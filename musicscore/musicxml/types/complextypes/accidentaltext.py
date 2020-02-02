from musicscore.musicxml.attributes.textformatting import TextFormatting
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeAccidentalValue

"""
<xs:attribute name="smufl" type="smufl-accidental-glyph-name"/>
"""


class ComplexTypeAccidentalText(ComplexType, TypeAccidentalValue, TextFormatting):
    """ The accidental-text type represents an element with an accidental value and text-formatting attributes."""

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
