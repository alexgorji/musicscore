from musicscore.musicxml.attributes.attribute_abstract import String
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.font import Font
from musicscore.musicxml.attributes.letterspacing import LetterSpacing
from musicscore.musicxml.attributes.text_direction import TextDirection
from musicscore.musicxml.attributes.textdecoration import TextDecoration
from musicscore.musicxml.attributes.textrotation import TextRotation
from musicscore.musicxml.types.complextypes.complextype import ComplexType


# todo XMLLang
class ComplexTypeTextElementData(ComplexType, String, Font, Color, TextDecoration, TextRotation, LetterSpacing,
                                 TextDirection):
    """
    documentation>The text-element-data type represents a syllable or portion of a syllable for lyric text underlay. A
    hyphen in the string content should only be used for an actual hyphenated word. Language names for text elements
    come from ISO 639, with optional country subcodes from ISO 3166.
    """

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
