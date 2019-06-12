from musicscore.musicxml.attributes.dahsedformatting import DashedFormatting
from musicscore.musicxml.attributes.linelength import LineLength
from musicscore.musicxml.attributes.lineshape import LineShape
from musicscore.musicxml.attributes.linetype import LineType
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.types.complextypes.complextype import Empty


class ComplexTypeEmptyLine(Empty, LineShape, LineType, LineLength, DashedFormatting, PrintStyle, Placement):
    """The empty-line type represents an empty element with line-shape, line-type, line-length, dashed-formatting,
    print-style and placement attributes."""

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
