from unittest import TestCase

from musicscore.tree.tree import TreeNode


class Test(TestCase):
    def setUp(self):
        self.me = TreeNode()
        self.me.name = 'me'
        self.child1 = self.me.add_child(TreeNode())
        self.child1.name = 'child1'
        self.grandchild = self.child1.add_child(TreeNode())
        self.grandchild.name = 'grandchild'
        self.child2 = self.me.add_child(TreeNode())
        self.child2.name = 'child2'
        self.parent = TreeNode()
        self.parent.name = 'parent'
        self.sibling = self.parent.add_child(TreeNode())
        self.sibling.name = 'sibling'
        self.nephew = self.sibling.add_child(TreeNode())
        self.nephew.name = 'nephew'
        self.parent.add_child(self.me)

    def test_remove(self):
        self.me.remove()
        result = ['parent', 'sibling', 'nephew', 'child1', 'grandchild', 'child2']
        self.assertEqual([node.name for node in self.parent.dump()], result)
