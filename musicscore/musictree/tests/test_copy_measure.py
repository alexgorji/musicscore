from unittest import TestCase

from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musicxml.types.complextypes.attributes import Beats


class TestCopyMeasure(TestCase):
    def setUp(self):
        self.measure = TreeMeasure()

    def test_copy_measure(self):
        new_measure = self.measure.__copy__()
        new_measure.time.get_children_by_type(Beats)[0].value = 8

        result = '''<time>
  <beats>8</beats>
  <beat-type>4</beat-type>
</time>
'''
        self.assertEqual(new_measure.time.to_string(), result)

        result = '''<time>
  <beats>4</beats>
  <beat-type>4</beat-type>
</time>
'''
        self.assertEqual(self.measure.time.to_string(), result)

