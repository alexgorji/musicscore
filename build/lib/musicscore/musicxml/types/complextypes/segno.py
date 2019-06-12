from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.printstyle import PrintStyleAlign
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeTypeSmulfSegnoGlyphName


class Smulf(TypeTypeSmulfSegnoGlyphName):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class ComplexTypeSegno(ComplexType, PrintStyleAlign, OptionalUniqueId, Smulf):
    """The segno type is the visual indicator of a segno sign. The exact glyph can be specified with the smufl
    attribute. A sound element is also needed to guide playback applications reliably."""

    def __init__(self, tag, value=None, *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)
