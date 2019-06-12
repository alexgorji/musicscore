from unittest import TestCase

from musicscore.musictree.exceptions import MusicTreeError
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musictree.treetime import TreeTime


class TestTreeTime(TestCase):

    def test_tree_time(self):
        time = TreeTime(3, 4, 1, 8)
        result = '''<time>
  <beats>3</beats>
  <beat-type>4</beat-type>
  <beats>1</beats>
  <beat-type>8</beat-type>
</time>
'''
        self.assertEqual(time.to_string(), result)

        # self.assertEqual(time.quarter_duration, 3.5)

        with self.assertRaises(MusicTreeError):
            TreeTime(4, 3)

    def test_copy_time(self):
        time = TreeTime(3, 4, 1, 8)
        copy = time.__copy__()
        result = '''<time>
  <beats>3</beats>
  <beat-type>4</beat-type>
  <beats>1</beats>
  <beat-type>8</beat-type>
</time>
'''
        self.assertEqual(copy.to_string(), result)
