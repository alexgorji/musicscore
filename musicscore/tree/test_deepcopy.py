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
        copied = self.parent.__deepcopy__()
        self.assertFalse([id(node) for node in self.parent.dump()] == [id(node) for node in copied.dump()])
        result = ['parent', 'sibling', 'nephew', 'me', 'child1', 'grand_child', 'child2']
        self.assertEqual([node.name for node in copied.dump()], result)

