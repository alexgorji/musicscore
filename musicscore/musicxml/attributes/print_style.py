from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.font import Font
from musicscore.musicxml.attributes.position import Position


class PrintStyle(Position, Font, Color):
    def __init__(self, default_x=None, default_y=None, relative_x=None, relative_y=None, font_family=None,
                 font_style=None, font_size=None, font_weight=None, color=None, *args, **kwargs):
        super().__init__(default_x=default_x, default_y=default_y, relative_x=relative_x,
                         relative_y=relative_y, font_family=font_family, font_style=font_style, font_size=font_size,
                         font_weight=font_weight, color=color, *args, **kwargs)
