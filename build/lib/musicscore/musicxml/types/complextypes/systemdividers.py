from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.types.complextypes.complextype import ComplexType, EmptyPrintObjectStyleAlign


class LeftDivider(EmptyPrintObjectStyleAlign):
    _TAG = 'left-divider'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class RightDivider(EmptyPrintObjectStyleAlign):
    _TAG = 'right-divider'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypeSystemDividers(ComplexType):
    """The system-dividers element indicates the presence or absence of system dividers (also known as system
    separation marks) between systems displayed on the same page. Dividers on the left and right side of the page are
    controlled by the left-divider and right-divider elements respectively. The default vertical position is half the
    system-distance value from the top of the system that is below the divider. The default horizontal position is the
    left and right system margin, respectively.

    When used in the print element, the system-dividers element affects the dividers that would appear between the
    current system and the previous system."""

    _DTD = Sequence(
        Element(LeftDivider),
        Element(RightDivider),
    ),

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
