from unittest import TestCase

from musicscore.musicxml.groups.musicdata import Attributes
from musicscore.musicxml.types.complextypes.attributes import Clef
from musicscore.musicxml.types.complextypes.clef import Sign


class TestTime(TestCase):

    def setUp(self):
        self.attributes = Attributes()

    def test_1(self):
        clef_1 = Clef(number=1)
        clef_1.add_child(Sign('G'))
        self.attributes.add_child(clef_1)

        clef_2 = Clef(number=2)
        clef_2.add_child(Sign('F'))
        self.attributes.add_child(clef_2)
        expected ='''<attributes>
  <clef number="1">
    <sign>G</sign>
  </clef>
  <clef number="2">
    <sign>F</sign>
  </clef>
</attributes>
'''
        actual = self.attributes.to_string()
        self.assertEqual(expected, actual)
