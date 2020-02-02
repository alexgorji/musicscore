from musicscore.musicxml.attributes.justify import Justify
from musicscore.musicxml.attributes.printstyle import PrintStyle


class GroupNameText(PrintStyle, Justify):
    """
    The group-name-text attribute group is used by the group-name and group-abbreviation elements. The print-style and
    justify attribute groups are deprecated in MusicXML 2.0 in favor of the new group-name-display and
    group-abbreviation-display elements.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
