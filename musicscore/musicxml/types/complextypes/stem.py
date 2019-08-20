from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.position import YPosition
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeStemValue


class ComplexTypeStem(ComplexType, TypeStemValue, YPosition, Color):
    """Stems can be down, up, none, or double. For down and up stems, the position attributes can be used to specify
    stem length. The relative values specify the end of the stem relative to the program default. Default values specify
    an absolute end stem position. Negative values of relative-y that would flip a stem instead of shortening it are
    ignored. A stem element associated with a rest refers to a stemlet."""

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
