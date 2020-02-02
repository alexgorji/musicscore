from unittest import TestCase

from musicscore.musicxml.elements.scoreheader import PartList
from musicscore.musicxml.types.complextypes.partlist import ScorePart, PartGroup
from musicscore.musicxml.types.complextypes.scorepart import PartName


def generate_score_part(id):
    output = ScorePart(id=id)
    output.add_child(PartName(id))
    return output


class Test(TestCase):

    def test_1(self):
        pl = PartList()
        pl.add_child(generate_score_part('p1'))
        pl.add_child(generate_score_part('p2'))
        result = pl.to_string()
        expected = '''<part-list>
  <score-part id="p1">
    <part-name>p1</part-name>
  </score-part>
  <score-part id="p2">
    <part-name>p2</part-name>
  </score-part>
</part-list>
'''
        self.assertEqual(expected, result)

    def test_2(self):
        pl = PartList()
        pl.add_child(PartGroup(type='start'))
        pl.add_child(generate_score_part('p1'))
        pl.add_child(generate_score_part('p2'))
        result = pl.to_string()
        expected = '''<part-list>
  <part-group number="1" type="start"/>
  <score-part id="p1">
    <part-name>p1</part-name>
  </score-part>
  <score-part id="p2">
    <part-name>p2</part-name>
  </score-part>
</part-list>
'''
        self.assertEqual(expected, result)

    def test_3(self):
        pl = PartList()
        pl.add_child(PartGroup(type='start'))
        pl.add_child(generate_score_part('p1'))
        pl.goto_next_dtd_choice()
        pl.add_child(generate_score_part('p2'))
        pl.add_child(PartGroup(type='stop'))
        result = pl.to_string()

        expected = '''<part-list>
  <score-part id="p1">
    <part-name>p1</part-name>
  </score-part>
  <part-group number="1" type="start"/>
  <score-part id="p2">
    <part-name>p2</part-name>
  </score-part>
  <part-group number="1" type="stop"/>
</part-list>
'''
        self.assertEqual(expected, result)

    def test_4(self):
        pl = PartList()
        pl.add_child(generate_score_part('p1'))
        pl.goto_next_dtd_choice()
        pl.add_child(PartGroup(type='start'))
        pl.add_child(generate_score_part('p2'))
        pl.add_child(generate_score_part('p3'))
        pl.add_child(generate_score_part('p4'))
        pl.add_child(PartGroup(type='stop'))
        pl.add_child(generate_score_part('p5'))
        result = pl.to_string()
        expected = '''<part-list>
  <score-part id="p1">
    <part-name>p1</part-name>
  </score-part>
  <part-group number="1" type="start"/>
  <score-part id="p2">
    <part-name>p2</part-name>
  </score-part>
  <score-part id="p3">
    <part-name>p3</part-name>
  </score-part>
  <score-part id="p4">
    <part-name>p4</part-name>
  </score-part>
  <part-group number="1" type="stop"/>
  <score-part id="p5">
    <part-name>p5</part-name>
  </score-part>
</part-list>
'''
        self.assertEqual(expected, result)
