from musicscore.musicxml.attributes.groupnametext import GroupNameText
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import String


class ComplexTypeGroupName(ComplexType, String, GroupNameText):
    """
    The group-name type describes the name or abbreviation of a part-group element. Formatting attributes in the
    group-name type are deprecated in Version 2.0 in favor of the new group-name-display and group-abbreviation-display
    elements.
    """

    def __init__(self, tag, value='', *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)
