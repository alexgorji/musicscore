from unittest import TestCase

from tree.tree import Tree, ChildNotFoundError


class A(Tree):
    def __init__(self, name, parent=None, *args, **keyword):
        super().__init__(*args, **keyword)
        self._children = []
        self._parent = parent
        self.name = name

    def _check_child_to_be_added(self, child):
        if not isinstance(child, self.__class__):
            raise TypeError

    def add_child(self, name):
        child = type(self)(parent=self, name=name)
        return super().add_child(child)


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
        assert self.root.tree_representation(lambda x: x.name) == expected

    def test_level(self):
        assert self.greatgrandchild1.level == 3
        assert self.grandchild2.level == 2
        assert self.child4.level == 1
        assert self.root.level == 0

    def test_reversed_path_to_root(self):
        assert list(self.greatgrandchild1.reversed_path_to_root()) == [self.greatgrandchild1, self.grandchild2, self.child2, self.root]

    def test_remove_child(self):
        with self.assertRaises(ChildNotFoundError):
            self.child2.remove(self.child1)

        self.child2.remove(self.grandchild2)
        assert self.child2.get_children() == [self.grandchild1]
        assert self.grandchild2.get_parent() is None
        assert self.greatgrandchild1.get_parent() == self.grandchild2

    def test_get_coordinates(self):
        assert self.greatgrandchild1.get_coordinates_in_tree() == '2.2.1'
        assert self.child2.get_coordinates_in_tree() == '2'
        assert self.root.get_coordinates_in_tree() == '0'