from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeBreathMarkValue


class ComplexTypeBreathMark(ComplexType, TypeBreathMarkValue, PrintStyle, Placement):
    """The breath-mark element indicates a place to take a breath."""

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
