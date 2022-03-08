from musicxml.xmlelement.xmlelement import XMLScaling

from musictree.layout import PageLayout, SystemLayout, StaffLayout, Scaling
from musictree.score import Score
from musictree.tests.util import IdTestCase


class TestScaling(IdTestCase):
    def test_scaling_init(self):
        sc = Scaling()
        assert sc.tenths == 40
        assert sc.millimeters == 7.2319
        assert isinstance(sc.xml_object, XMLScaling)
        assert sc.xml_object.xml_tenths.value_ == sc.tenths
        assert sc.xml_object.xml_millimeters.value_ == sc.millimeters

        sc.tenths = 50
        assert sc.xml_object.xml_tenths.value_ == sc.tenths


class TestPageLayout(IdTestCase):
    def setUp(self):
        self.score = Score()

    def test_page_layout_default(self):
        pl = PageLayout()
        self.score.page_layout = pl
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

        pl.scaling.tenths = 50
        assert self.score.page_layout == pl
        assert self.score.scaling.score == self.score
        assert self.score.scaling.tenths == 50
        assert pl.xml_page_height.value_ == round(1643 * 5 / 4)


class TestSystemLayout(IdTestCase):
    def test_style_layout_default(self):
        sl = SystemLayout()
        assert sl.xml_system_distance.value_ == 117
        assert sl.xml_top_system_distance.value_ == 117
        assert sl.xml_system_margins.xml_left_margin.value_ == 0
        assert sl.xml_system_margins.xml_right_margin.value_ == 0


class TestStaffLayout(IdTestCase):
    def test_staff_layout_default(self):
        sl = StaffLayout()
        assert sl.xml_staff_distance.value_ == 80
