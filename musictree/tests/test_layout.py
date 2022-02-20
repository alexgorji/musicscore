from musictree.layout import PageLayout, SystemLayout, StaffLayout
from musictree.tests.util import IdTestCase


class TestPageLayout(IdTestCase):

    def test_page_layout_default(self):
        pl = PageLayout()
        assert pl.size == 'A4'
        assert pl.orientation == 'portrait'
        assert pl.xml_page_height.value_ == 1643
        assert pl.xml_page_width.value_ == 1161
        assert pl.xml_page_margins.type == 'both'
        assert pl.xml_page_margins.xml_left_margin.value_ == 140
        assert pl.xml_page_margins.xml_right_margin.value_ == 70
        assert pl.xml_page_margins.xml_top_margin.value_ == 70
        assert pl.xml_page_margins.xml_bottom_margin.value_ == 70

        pl.orientation = 'landscape'
        assert pl.xml_page_height.value_ == 1161
        assert pl.xml_page_width.value_ == 1643
        assert pl.xml_page_margins.type == 'both'
        assert pl.xml_page_margins.xml_left_margin.value_ == 111
        assert pl.xml_page_margins.xml_right_margin.value_ == 70
        assert pl.xml_page_margins.xml_top_margin.value_ == 70
        assert pl.xml_page_margins.xml_bottom_margin.value_ == 70

        pl.size = 'A3'
        pl.orientation = 'portrait'
        assert pl.xml_page_height.value_ == 2323
        assert pl.xml_page_width.value_ == 1643
        assert pl.xml_page_margins.type == 'both'
        assert pl.xml_page_margins.xml_left_margin.value_ == 111
        assert pl.xml_page_margins.xml_right_margin.value_ == 70
        assert pl.xml_page_margins.xml_top_margin.value_ == 70
        assert pl.xml_page_margins.xml_bottom_margin.value_ == 70

        pl.orientation = 'landscape'
        assert pl.xml_page_height.value_ == 1643
        assert pl.xml_page_width.value_ == 2323
        assert pl.xml_page_margins.type == 'both'
        assert pl.xml_page_margins.xml_left_margin.value_ == 111
        assert pl.xml_page_margins.xml_right_margin.value_ == 70
        assert pl.xml_page_margins.xml_top_margin.value_ == 70
        assert pl.xml_page_margins.xml_bottom_margin.value_ == 70


class TestSystemLayout(IdTestCase):
    def test_style_layout_default(self):
        sl = SystemLayout()
        assert sl.xml_system_distance.value_ == 117
        assert sl.xml_top_system_distance.value_ == 66
        assert sl.xml_system_margins.xml_left_margin.value_ == 0
        assert sl.xml_system_margins.xml_right_margin.value_ == 0
        assert sl.xml_system_margins.xml_top_margin is None
        assert sl.xml_system_margins.xml_bottom_margin is None


class TestStaffLayout(IdTestCase):
    def test_staff_layout_default(self):
        sl = StaffLayout()
        assert sl.xml_staff_distance.value_ == 80
