from unittest import TestCase

from musicscore.musicxml.types.complextypes.attributes import Clef
from musicscore.musicxml.types.complextypes.clef import Sign


class Test(TestCase):
    def setUp(self) -> None:
        self.clef = Clef()
        self.clef.add_child(Sign('F'))

    def test_1(self):
        clef = self.clef

        expected = '''<clef>
  <sign>F</sign>
</clef>
'''
        actual = clef.to_string()
        self.assertEqual(expected, actual)

    def test_2(self):
        clef = self.clef
        clef.number = 2
        expected = '''<clef number="2">
  <sign>F</sign>
</clef>
'''
        actual = clef.to_string()
        self.assertEqual(expected, actual)

    def test_3(self):
        clef = self.clef
        clef.after_barline = 'yes'
        expected = '''<clef after-barline="yes">
  <sign>F</sign>
</clef>
'''
        actual = clef.to_string()
        self.assertEqual(expected, actual)

    def test_4(self):
        clef = self.clef
        clef.size = 'large'
        expected = '''<clef size="large">
  <sign>F</sign>
</clef>
'''
        actual = clef.to_string()
        self.assertEqual(expected, actual)

    def test_5(self):
        clef = self.clef
        clef.additional = 'no'
        expected = '''<clef additional="no">
  <sign>F</sign>
</clef>
'''
        actual = clef.to_string()
        self.assertEqual(expected, actual)

    def test_6(self):
        clef = self.clef
        clef.number = 2
        clef.additional = 'no'
        clef.size = 'large'
        clef.after_barline = 'yes'
        expected = '''<clef number="2" additional="no" size="large" after-barline="yes">
  <sign>F</sign>
</clef>
'''
        actual = clef.to_string()
        self.assertEqual(expected, actual)

    # def test_7(self):
    #     clef = Clef(number=2)
