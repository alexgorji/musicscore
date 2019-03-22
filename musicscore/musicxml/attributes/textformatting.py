from musicscore.musicxml.attributes.enclosure import Enclosure
from musicscore.musicxml.attributes.justify import Justify
from musicscore.musicxml.attributes.letterspacing import LetterSpacing
from musicscore.musicxml.attributes.lineheight import LineHeight
from musicscore.musicxml.attributes.printstyle import PrintStyleAlign
from musicscore.musicxml.attributes.textdecoration import TextDecoration
from musicscore.musicxml.attributes.text_direction import TextDirection
from musicscore.musicxml.attributes.textrotation import TextRotation


# todo: XMLLang, XMLSpace
class TextFormatting(Justify, PrintStyleAlign, TextDecoration, TextRotation, LetterSpacing, LineHeight, TextDirection,
                     Enclosure):
    """
    The text-formatting attribute group collects the common formatting attributes for text elements. Default values may
    differ across the elements that use this group.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
