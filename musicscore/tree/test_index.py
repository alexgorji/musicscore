from unittest import TestCase

from musicscore.tree.tree import TreeNode


class Test(TestCase):
    def setUp(self):
        self.me = TreeNode()
        self.me.name = 'me'
        self.child1 = self.me.add_child(TreeNode())
        self.child1.name = 'child1'
        self.grandchild = self.child1.add_child(TreeNode())
        self.grandchild.name = 'grand_child'
        self.child2 = self.me.add_child(TreeNode())
        self.child2.name = 'child2'
        self.parent = TreeNode()
        self.parent.name = 'parent'
        self.sibling = self.parent.add_child(TreeNode())
        self.sibling.name = 'sibling'
        self.nephew = self.sibling.add_child(TreeNode())
        self.nephew.name = 'nephew'
        self.parent.add_child(self.me)

    def test_index(self):
        for node in self.parent.traverse():
            print(node.name)
            print(node.index)
            print(self.parent.goto(node.index).name)
        self.assertEqual(self.parent.goto(self.grandchild.index).name, 'grand_child')

