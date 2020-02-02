from musicscore.dtd.dtd import Sequence, Choice, Element
from musicscore.musicxml.attributes.printobject import PrintObject
from musicscore.musicxml.types.complextypes.accidentaltext import ComplexTypeAccidentalText
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.formattedtext import ComplexTypeFormattedText


class DisplayText(ComplexTypeFormattedText):
    _TAG = 'display-text'

    def __init__(self, value='', *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class AccidentalText(ComplexTypeAccidentalText):
    _TAG = 'accidental-text'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class ComplexTypeNameDisplay(ComplexType, PrintObject):
    """ The name-display type is used for exact formatting of multi-font text in part and group names to the left of
    the system. The print-object attribute can be used to determine what, if anything, is printed at the start of each
    system. Enclosure for the display-text element is none by default. Language for the display-text element is Italian
    ("it") by default.
    """
    _DTD = Sequence(
        Choice(
            Element(DisplayText),
            Element(AccidentalText),
            min_occurrence=0,
            max_occurrence=None
        )
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
