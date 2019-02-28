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
        print(child_2.is_leaf)
        print(child_4.is_leaf)
        print(self.tree.get_leaves())

