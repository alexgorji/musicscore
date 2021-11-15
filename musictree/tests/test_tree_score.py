from unittest import TestCase

from musictree.treepart import TreePart
from musictree.treescore import TreeScore


class TestTreeScore(TestCase):
    def test_add_part(self):
        score = TreeScore()
        assert len(score.parts) == 0
        self.assertEqual(0, len(score.parts))
        part = score.add_part()
        assert isinstance(part, TreePart)
        assert score.parts[-1] == part
