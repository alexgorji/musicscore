from musicscore.musicxml.types.complextypes.partlist import PartGroup


class TreePartGroup(PartGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)