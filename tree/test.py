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

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


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
        assert self.root.get_root() == self.root

    def test_is_leaf(self):
        assert self.greatgrandchild1.is_leaf is True
        assert self.child4.is_leaf is False
        assert self.child3.is_leaf is True

    def test_traverse(self):
        assert list(self.root.traverse()) == [self.root, self.child1, self.child2, self.grandchild1, self.grandchild2,
                                              self.greatgrandchild1, self.child3, self.child4, self.grandchild3]

    def test_traverse_breadth_first_search(self):
        expected = [self.root, self.child1, self.child2, self.child3, self.child4, self.grandchild1, self.grandchild2, self.grandchild3,
                    self.greatgrandchild1]
        assert list(self.root.traverse(mode='bfs')) == expected

    def test_iterate_leaves(self):
        assert list(self.root.iterate_leaves()) == [self.child1, self.grandchild1, self.greatgrandchild1,
                                                    self.child3, self.grandchild3]

    def test_level(self):
        assert [node.level for node in self.root.traverse()] == [0, 1, 1, 2, 2, 3, 1, 1, 2]
        assert self.greatgrandchild1.level == 3
        assert self.grandchild2.level == 2
        assert self.child4.level == 1
        assert self.root.level == 0

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

    def test_replace_child(self):
        self.child2.replace_child(self.grandchild1, A(name='new_grand_child'))
        assert [ch.name for ch in self.child2.get_children()] == ['new_grand_child', 'grandchild2']
        self.child1.add_child('grandchild')
        self.child1.add_child('grandchild')
        new = A(name='other_new_grand_child')
        self.child1.replace_child(lambda x: x.name == 'grandchild', new, 1)
        assert new.get_parent() == self.child1
        assert [ch.name for ch in self.child1.get_children()] == ['grandchild', 'other_new_grand_child']
        with self.assertRaises(ValueError):
            self.child2.replace_child(None, None)
        with self.assertRaises(TypeError):
            self.root.replace_child(self.child1, 34)

    def test_previous(self):
        assert self.child4.previous == self.child3
        assert self.child3.previous == self.child2
        assert self.child2.previous == self.child1
        assert self.child1.previous is None

    def test_next(self):
        assert self.child1.next == self.child2
        assert self.child2.next == self.child3
        assert self.child3.next == self.child4
        assert self.child4.next is None

    def test_get_leaves(self):
        assert self.root.get_leaves(key=lambda x: x.name) == ['child1', ['grandchild1', ['greatgrandchild1']], 'child3', ['grandchild3']]

    def test_get_layer(self):
        assert self.root.get_layer(0) == [self.root]
        assert self.root.get_layer(1) == [self.child1, self.child2, self.child3, self.child4]
        assert self.root.get_layer(2) == [self.child1, self.grandchild1, self.grandchild2, self.child3, self.grandchild3]
        assert self.root.get_layer(3) == [self.child1, self.grandchild1, self.greatgrandchild1, self.child3, self.grandchild3]
        assert self.root.get_layer(4) == [self.child1, self.grandchild1, self.greatgrandchild1, self.child3, self.grandchild3]

    def test_find_grandchild(self):
        assert [n for n in self.root.traverse() if n.level == 2] == [self.grandchild1, self.grandchild2, self.grandchild3]
        for n in self.root.traverse():
            if n.level == 2:
                print(n)
                break
