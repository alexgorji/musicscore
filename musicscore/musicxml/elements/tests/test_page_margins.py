from unittest import TestCase

from musicscore.dtd.dtd import ChildIsNotOptional
from musicscore.musicxml.groups.layout import PageLayout
from musicscore.musicxml.groups.margins import LeftMargin, RightMargin
from musicscore.musicxml.types.complextypes.pagelayout import PageMargins


class Test(TestCase):
    def test_1(self):
        page_margins = PageMargins()
        page_margins.add_child(LeftMargin(70))
        page_margins.add_child(RightMargin(70))
        with self.assertRaises(ChildIsNotOptional):
            page_margins.to_string()

    def test_2(self):
        page_layout = PageLayout()
        page_margins = page_layout.add_child(PageMargins())
        page_margins.add_child(LeftMargin(70))
        page_margins.add_child(RightMargin(70))
        with self.assertRaises(ChildIsNotOptional):
            page_layout.to_string()
