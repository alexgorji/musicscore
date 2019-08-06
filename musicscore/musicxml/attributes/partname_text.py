from musicscore.musicxml.attributes.justify import Justify
from musicscore.musicxml.attributes.printobject import PrintObject
from musicscore.musicxml.attributes.printstyle import PrintStyle


class PartNameText(PrintStyle, PrintObject, Justify):
    """
    The part-name-text attribute group is used by the part-name and part-abbreviation elements. The print-style and
    justify attribute groups are deprecated in MusicXML 2.0 in favor of the new part-name-display and
    part-abbreviation-display elements
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
