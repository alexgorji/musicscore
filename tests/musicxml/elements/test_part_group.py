from unittest import TestCase

from musicscore.musicxml.types.complextypes.namedisplay import DisplayText, AccidentalText
from musicscore.musicxml.types.complextypes.partgroup import GroupName, GroupNameDisplay, GroupSymbol, GroupBarline
from musicscore.musicxml.types.complextypes.partlist import PartGroup


class Test(TestCase):
    def test_1(self):
        obj = GroupName()
        expected = """<group-name></group-name>
"""
        result = obj.to_string()
        self.assertEqual(expected, result)

    def test_2(self):
        obj = GroupName('strings')
        expected = """<group-name>strings</group-name>
"""
        result = obj.to_string()
        self.assertEqual(expected, result)

    def test_3(self):
        obj = GroupNameDisplay()
        obj.add_child(DisplayText('strings'))
        obj.add_child(AccidentalText('natural'))
        expected = """<group-name-display>
  <display-text>strings</display-text>
  <accidental-text>natural</accidental-text>
</group-name-display>
"""
        result = obj.to_string()
        self.assertEqual(expected, result)

    def test_4(self):
        obj = GroupNameDisplay()
        obj.add_child(DisplayText('strings'))
        obj.add_child(AccidentalText('natural'))
        expected = """<group-name-display>
  <display-text>strings</display-text>
  <accidental-text>natural</accidental-text>
</group-name-display>
"""
        result = obj.to_string()
        self.assertEqual(expected, result)

    def test_5(self):
        pg = PartGroup(type='start', number='2')
        gnd = pg.add_child(GroupNameDisplay())
        gnd.add_child(DisplayText('strings'))
        pg.add_child(GroupSymbol('bracket'))
        pg.add_child(GroupBarline('yes'))
        expected = """<part-group number="2" type="start">
  <group-name-display>
    <display-text>strings</display-text>
  </group-name-display>
  <group-symbol>bracket</group-symbol>
  <group-barline>yes</group-barline>
</part-group>
"""
        result = pg.to_string()
        self.assertEqual(expected, result)


