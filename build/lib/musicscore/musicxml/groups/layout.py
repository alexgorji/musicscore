from musicscore.dtd.dtd import Sequence, Element

from musicscore.musicxml.types.complextypes.pagelayout import ComplexTypePageLayout
from musicscore.musicxml.types.complextypes.stafflayout import ComplexTypeStaffLayout
from musicscore.musicxml.types.complextypes.systemlayout import ComplexTypeSystemLayout

from musicscore.dtd.dtd import GroupReference, Element, Sequence

from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.simple_type import TypeTenths


#
# class LeftMargin(XMLElement, TypeTenths):
#     _TAG = 'left-margin'
#
#     def __init__(self, value=None, *args, **kwargs):
#         super().__init__(tag=self._TAG, value=value, *args, **kwargs)
#
#
# class RightMargin(XMLElement, TypeTenths):
#     _TAG = 'right-margin'
#
#     def __init__(self, value=None, *args, **kwargs):
#         super().__init__(tag=self._TAG, value=value, *args, **kwargs)
#
#
# class TopMargin(XMLElement, TypeTenths):
#     _TAG = 'top-margin'
#
#     def __init__(self, value=None, *args, **kwargs):
#         super().__init__(tag=self._TAG, value=value, *args, **kwargs)
#
#
# class BottomMargin(XMLElement, TypeTenths):
#     _TAG = 'bottom-margin'
#
#     def __init__(self, value=None, *args, **kwargs):
#         super().__init__(tag=self._TAG, value=value, *args, **kwargs)
#
#
# """
# The left-right-margins group specifies horizontal margins in tenths.
# """
#
# LeftRightMargins = Sequence(
#     Element(LeftMargin),
#     Element(RightMargin)
# )
#
# """
# The all-margins group specifies both horizontal and vertical margins in tenths.
# """
# AllMargins = Sequence(
#     GroupReference(LeftRightMargins),
#     Element(TopMargin),
#     Element(BottomMargin)
#
# )


class PageLayout(ComplexTypePageLayout):
    _TAG = 'page-layout'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class SystemLayout(ComplexTypeSystemLayout):
    _TAG = 'system-layout'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class StaffLayout(ComplexTypeStaffLayout):
    _TAG = 'staff-layout'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


"""
The layout group specifies the sequence of page, system, and staff layout elements that is
                common to both the defaults and print elements.
"""
Layout = Sequence(
    Element(PageLayout, min_occurrence=0),
    Element(SystemLayout, min_occurrence=0),
    Element(StaffLayout, min_occurrence=0, max_occurrence=None)
)
