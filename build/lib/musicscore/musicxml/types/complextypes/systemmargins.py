from musicscore.dtd.dtd import GroupReference, Sequence
from musicscore.musicxml.groups.margins import LeftRightMargins
from musicscore.musicxml.types.complextypes.complextype import ComplexType


class ComplexTypeSystemMargins(ComplexType):
    """
    System margins are relative to the page margins. Positive values indent and negative values reduce the margin size.
    """

    _DTD = Sequence(
        GroupReference(LeftRightMargins)
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)