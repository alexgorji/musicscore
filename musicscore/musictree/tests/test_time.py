from unittest import TestCase

from musicscore.musictree.exceptions import MusicTreeError
from musicscore.musictree.timewise import TreeTime


class TestTreeTime(TestCase):

    def test_tree_time(self):
        time = TreeTime(3, 4)
        result = '''<time>
  <beats>3</beats>
  <beat-type>4</beat-type>
</time>
'''
        self.assertEqual(time.to_string(), result)

        with self.assertRaises(MusicTreeError):
            TreeTime(4, 3)

