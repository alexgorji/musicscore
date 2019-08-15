from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.holeclosed import ComplexTypeHoleClosed
from musicscore.musicxml.types.simple_type import String


class HoleType(String):
    """The content of the optional hole-type element indicates what the hole symbol represents in terms of instrument
    fingering or other techniques."""

    _TAG = 'hole-type'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class HoleClosed(ComplexTypeHoleClosed):
    """"""

    _TAG = 'hole-closed'

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class HoleShape(String):
    """The optional hole-shape element indicates the shape of the hole symbol; the default is a circle."""

    _TAG = 'hole-shape'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypeHole(ComplexType, PrintStyle, Placement):
    """The hole type represents the symbols used for woodwind and brass fingerings as well as other notations."""
    _DTD = Sequence(
        Element(HoleType, min_occurrence=0),
        Element(HoleClosed),
        Element(HoleShape, min_occurrence=0)
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
