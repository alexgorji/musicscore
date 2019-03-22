from unittest import TestCase

from musicscore.musictree.exceptions import MusicTreeError
from musicscore.musictree.treetimewise import TreeTime, TreeScoreTimewise


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

        self.assertEqual(time.quarter_duration, 3.5)

        with self.assertRaises(MusicTreeError):
            TreeTime(4, 3)

    def test_score_time(self):
        score = TreeScoreTimewise()
        score.add_measure()
        score.add_part('one')
        score.finish()
        result = '''<score-timewise version="3.0">
  <part-list>
    <score-part id="p1">
      <part-name print-object="no">one</part-name>
    </score-part>
  </part-list>
  <measure number="1">
    <part id="p1">
      <attributes>
        <divisions>1</divisions>
      </attributes>
    </part>
  </measure>
</score-timewise>
'''
        self.assertEqual(score.to_string(), result)

