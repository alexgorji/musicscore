from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.attributes.trillsound import TrillSound
from musicscore.musicxml.types.complextypes.complextype import ComplexType


class ComplexTypeEmptyTrillSound(ComplexType, PrintStyle, Placement, TrillSound):
    """
    The empty-trill-sound type represents an empty element with print-style, placement, and trill-sound attributes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


