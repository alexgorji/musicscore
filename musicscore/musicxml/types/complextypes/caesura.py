from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeCaesuraValue


# class ComplexTypeCaesura(ComplexType, TypeCaesuraValue, PrintStyle, Placement):
#     """The caesura element indicates a slight pause. It is notated using a "railroad tracks" symbol or other variations
#     specified in the element content."""
#
#     def __init__(self, tag, value, *args, **kwargs):
#         super().__init__(tag=tag, value=value, *args, **kwargs)

class ComplexTypeCaesura(ComplexType, PrintStyle, Placement):
    """The caesura element indicates a slight pause. It is notated using a "railroad tracks" symbol or other variations
    specified in the element content."""

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
