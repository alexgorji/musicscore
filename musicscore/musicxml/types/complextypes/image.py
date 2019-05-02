from musicscore.musicxml.attributes.image import ImageAttributes
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.types.complextypes.complextype import ComplexType


class ComplexTypeImage(ComplexType, ImageAttributes, OptionalUniqueId):
    """The image type is used to include graphical images in a score."""

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
