from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeGroupBarlineValue


class ComplexTypeGroupBarline(ComplexType, TypeGroupBarlineValue, Color):
    """The group-barline type indicates if the group should have common barlines."""

    def __init__(self, tag, value=None, *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)
