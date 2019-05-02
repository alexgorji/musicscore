import os
from unittest import TestCase

from musicscore.musictree.treescore_timewise import TreeScoreTimewise
from musicscore.musicxml.elements.scoreheader import Credit
from musicscore.musicxml.types.complextypes.credit import CreditType, CreditWords

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.score.add_measure()
        self.score.add_part()

    def test_1(self):
        c = self.score.add_child(Credit(page=1))
        c.add_child(CreditType('title'))
        c.add_child(CreditWords('TEST', default_x=598, default_y=1573, font_size=24, justify='center', valign='top'))
        result_path = path + '_test_1'
        print(self.score.to_string())
        self.score.write(path=result_path)
        '''
          <credit page="1">
            <credit-type>title</credit-type>
            <credit-words default-x="598" default-y="1573" font-size="24" justify="center" valign="top">TEST</credit-words>
          </credit>
          <credit page="1">
            <credit-type>composer</credit-type>
            <credit-words default-x="1089" default-y="1504" font-size="12" justify="right" valign="top">me</credit-words>
          </credit>
          <credit page="1">
            <credit-type>arranger</credit-type>
            <credit-words default-x="1089" default-y="1469" font-size="12" justify="right" valign="top">me2</credit-words>
          </credit>
          <credit page="1">
            <credit-type>subtitle</credit-type>
            <credit-words default-x="598" default-y="1508" font-size="18" justify="center" valign="top">BLA</credit-words>
          </credit>
        '''
