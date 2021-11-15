from unittest import TestCase

from musictree.treemeasure import TreeMeasure
from musictree.treepart import TreePart


class TestTreePart(TestCase):
    def test_add_measure(self):
        part = TreePart()
        assert len(part.measures) == 0
        measure = part.add_measure()
        assert isinstance(measure, TreeMeasure)
        assert len(part.measures) == 1
        assert part.measures[-1] == measure
