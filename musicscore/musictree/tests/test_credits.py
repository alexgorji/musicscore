import os
from unittest import TestCase

from musicscore.musictree.treescore_timewise import TreeScoreTimewise
from musicscore.musicxml.elements.scoreheader import Credit, Defaults
from musicscore.musicxml.groups.layout import PageLayout, SystemLayout
from musicscore.musicxml.groups.margins import LeftMargin, RightMargin, BottomMargin, TopMargin
from musicscore.musicxml.score_templates.xml_test_score import TestScore
from musicscore.musicxml.types.complextypes.credit import CreditType, CreditWords
from musicscore.musicxml.types.complextypes.defaults import Scaling
from musicscore.musicxml.types.complextypes.pagelayout import PageHeight, PageWidth, PageMargins
from musicscore.musicxml.types.complextypes.scaling import Millimeters, Tenths
from musicscore.musicxml.types.complextypes.systemlayout import SystemMargins, SystemDistance, TopSystemDistance

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.score.add_measure()
        self.score.add_part()

    def test_1(self):

        c = self.score.add_child(Credit(page=1))
        c.add_child(CreditType('title'))
        c.add_child(CreditWords('TEST', default_x=598, default_y=1600, font_size=24, justify='center', valign='top'))

        c = self.score.add_child(Credit(page=1))
        c.add_child(CreditType('composer'))
        c.add_child(CreditWords('me', default_x=1089, default_y=1550, font_size=12, justify='right', valign='top'))

        c = self.score.add_child(Credit(page=1))
        c.add_child(CreditType('arranger'))
        c.add_child(CreditWords('TEST', default_x=1089, default_y=1500, font_size=12, justify='right', valign='top'))

        c = self.score.add_child(Credit(page=1))
        c.add_child(CreditType('subtitle'))
        c.add_child(CreditWords('BLA', default_x=598, default_y=1550, font_size=18, justify='center', valign='top'))

        result_path = path + '_test_1'

        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)