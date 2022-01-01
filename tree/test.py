from unittest import TestCase

from tree.tree import Tree


class A(Tree):
    def __init__(self, name, parent=None):
        self._children = []
        self._parent = parent
        self.name = name

    def add_child(self, name):
        child = type(self)(parent=self, name=name)
        self._children.append(child)
        return child

    def get_children(self):
        return self._children

    def get_parent(self):
        return self._parent


class TestTree(TestCase):
    def setUp(self) -> None:
        self.root = A(name='root')
        self.child1 = self.root.add_child('child1')
        self.child2 = self.root.add_child('child2')
        self.child3 = self.root.add_child('child3')
        self.child4 = self.root.add_child('child4')
        self.grandchild1 = self.child2.add_child('grandchild1')
        self.grandchild2 = self.child2.add_child('grandchild2')
        self.grandchild3 = self.child4.add_child('grandchild3')
        self.greatgrandchild1 = self.grandchild2.add_child('greatgrandchild1')

    def test_get_root(self):
        assert self.greatgrandchild1.get_root() == self.root
        assert self.child4.get_root() == self.root

    def test_is_leaf(self):
        assert self.greatgrandchild1.is_leaf is True
        assert self.child4.is_leaf is False
        assert self.child3.is_leaf is True

    def test_traverse(self):
        assert list(self.root.traverse()) == [self.root, self.child1, self.child2, self.grandchild1, self.grandchild2,
                                              self.greatgrandchild1, self.child3, self.child4, self.grandchild3]

    def test_iterate_leaves(self):
        assert list(self.root.iterate_leaves()) == [self.child1, self.grandchild1, self.greatgrandchild1,
                                                    self.child3, self.grandchild3]

    def test_get_layer_number(self):
        assert [node.get_layer_number() for node in self.root.traverse()] == [0, 1, 1, 2, 2, 3, 1, 1, 2]

    def test_tree_repr(self):
        expected = """root
    child1
    child2
        grandchild1
        grandchild2
            greatgrandchild1
    child3
    child4
        grandchild3
"""
        assert self.root.tree_repr('name') == expected