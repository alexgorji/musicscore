from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.justify import Justify


class TextFormatting(Justify, PrintStyleAlign, TextDecoration, TextRotation, LetterSpacing, LineHeight, XMLLang,
                     XMLSpace, TextDirection, Enclosure):
    """
    The text-formatting attribute group collects the common formatting attributes for text elements. Default values may
    differ across the elements that use this group.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

