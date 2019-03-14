from musicscore.musicxml.attributes.justify import Justify
from musicscore.musicxml.attributes.print_object import PrintObject
from musicscore.musicxml.attributes.print_style import PrintStyle


class PartNameText(PrintStyle, PrintObject, Justify):
    """
    The part-name-text attribute group is used by the part-name and part-abbreviation elements. The print-style and
    justify attribute groups are deprecated in MusicXML 2.0 in favor of the new part-name-display and
    part-abbreviation-display elements
    """

    def __init__(self, default_x=None, default_y=None, relative_x=None, relative_y=None, font_family=None,
                 font_style=None, font_size=None, font_weight=None, color=None, print_object=None, *args, **kwargs):
        super().__init__(default_x=default_x, default_y=default_y, relative_x=relative_x,
                         relative_y=relative_y, font_family=font_family, font_style=font_style, font_size=font_size,
                         font_weight=font_weight, color=color, print_object=print_object, *args, **kwargs)