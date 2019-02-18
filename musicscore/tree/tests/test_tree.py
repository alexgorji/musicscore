from unittest import TestCase
from musicscore.tree.tree import Tree


class TestTree(TestCase):
    def setUp(self):
        self.tree = Tree()

    def test_tree(self):
        child = self.tree.add_child(Tree())
        self.assertTrue(self.tree.is_root())
        self.assertEqual(child.up, self.tree)
