from unittest import TestCase
from musicscore.tree.tree import Tree


class TestTree(TestCase):
    def setUp(self):
        self.tree = Tree()

    def test_tree(self):
        child = self.tree.add_child(Tree())
        self.assertTrue(self.tree.is_root)
        self.assertEqual(child.up, self.tree)

    def test_get_leaves(self):
        child_1 = self.tree.add_child(Tree())
        child_2 = self.tree.add_child(Tree())
        child_3 = self.tree.add_child(Tree())
        child_4 = child_2.add_child(Tree())
        child_5 = child_2.add_child(Tree())
        self.assertFalse(child_2.is_leaf)
        self.assertTrue(child_4.is_leaf)
        result = [child_1, [child_4, child_5], child_3]
        self.assertEqual(self.tree.get_leaves(), result)

