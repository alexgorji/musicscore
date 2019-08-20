from musicscore.musicxml.attributes.align import Halign, Valign
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.font import Font
from musicscore.musicxml.attributes.position import Position


class PrintStyle(Position, Font, Color):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PrintStyleAlign(PrintStyle, Halign, Valign):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
