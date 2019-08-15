from unittest import TestCase

from musicscore.musicxml.elements import timewise
from musicscore.musicxml.elements.scoreheader import PartList, Defaults
from musicscore.musicxml.types.complextypes.appearance import LineWidth
from musicscore.musicxml.types.complextypes.defaults import Appearance
from musicscore.musicxml.types.complextypes.partlist import ScorePart
from musicscore.musicxml.types.complextypes.scorepart import PartName


class Test(TestCase):
    def setUp(self) -> None:
        self.score = timewise.Score()
        pl = self.score.add_child(PartList())
        sp = pl.add_child(ScorePart(id='p1'))
        sp.add_child(PartName(name='none'))
        m = self.score.add_child(timewise.Measure(number=1))
        m.add_child(timewise.Part(id='p1'))

    def test_1(self):
        d = self.score.add_child(Defaults())
        a = d.add_child(Appearance())
        a.add_child(LineWidth(type='tuplet bracket', value=2.4))
        result = """<score-timewise version="1.0">
  <defaults>
    <appearance>
      <line-width type="tuplet bracket">2.4</line-width>
    </appearance>
  </defaults>
  <part-list>
    <score-part id="p1">
      <part-name>none</part-name>
    </score-part>
  </part-list>
  <measure number="1">
    <part id="p1"/>
  </measure>
</score-timewise>
"""
        self.assertEqual(self.score.to_string(), result)
