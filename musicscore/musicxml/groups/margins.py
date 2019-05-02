from musicscore.dtd.dtd import GroupReference, Element, Sequence

from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.simple_type import TypeTenths


class LeftMargin(XMLElement, TypeTenths):
    _TAG = 'left-margin'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class RightMargin(XMLElement, TypeTenths):
    _TAG = 'right-margin'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class TopMargin(XMLElement, TypeTenths):
    _TAG = 'top-margin'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class BottomMargin(XMLElement, TypeTenths):
    _TAG = 'bottom-margin'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


"""
The left-right-margins group specifies horizontal margins in tenths.
"""

LeftRightMargins = Sequence(
    Element(LeftMargin),
    Element(RightMargin)
)

"""
The all-margins group specifies both horizontal and vertical margins in tenths.
"""
AllMargins = Sequence(
    GroupReference(LeftRightMargins),
    Element(TopMargin),
    Element(BottomMargin)
)
