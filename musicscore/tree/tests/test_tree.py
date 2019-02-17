from unittest import TestCase
from musicscore.tree.tree import Tree


class TestTree(TestCase):
    def setUp(self):
        self.tree = Tree()

    def test_tree(self):
        self.tree.add_child(Tree())
        print(self.tree.get_children())
