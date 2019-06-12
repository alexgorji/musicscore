from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.pagemargins import ComplexTypePageMargins
from musicscore.musicxml.types.simple_type import TypeTenths


class PageHeight(XMLElement, TypeTenths):
    _TAG = 'page-height'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class PageWidth(XMLElement, TypeTenths):
    _TAG = 'page-width'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class PageMargins(ComplexTypePageMargins):
    _TAG = 'page-margins'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypePageLayout(ComplexType):
    """Page layout can be defined both in score-wide defaults and in the print element. Page margins are specified
    either for both even and odd pages, or via separate odd and even page number values. The type is not needed when
    used as part of a print element. If omitted when used in the defaults element, "both" is the default."""

    _DTD = Sequence(
        Sequence(
            Element(PageHeight),
            Element(PageWidth),
            min_occurrence=0
        ),
        Element(PageMargins, min_occurrence=0, max_occurrence=2)
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
