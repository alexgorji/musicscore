from abc import ABC, abstractmethod
from typing import Optional, Callable, List, Iterator


class TreeException(Exception):
    pass


class ChildNotFoundError(TreeException):
    pass


class Tree(ABC):
    """
    An abstract lightweight tree class for managing tree structures in musicxml and musictree packages.
    """
    _TREE_ATTRIBUTES = {'compact_repr', 'is_leaf', 'level', '_parent', '_children', 'up'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent = None
        self._children = []

    @abstractmethod
    def _check_child_to_be_added(self, child):
        pass

    @property
    def compact_repr(self) -> str:
        """
        :return: as default the string representation. This property is used as default in the ``tree_representation`` method and can be
                 customized in subclasses to get the most appropriate representation.
        :rtype: str
        """
        return self.__str__()

    @property
    def is_leaf(self) -> bool:
        """
        :return: ``True`` if self has no children. ``False`` if self has one or more children.
        :rtype: bool
        """
        if not self.get_children():
            return True
        else:
            return False

    @property
    def is_root(self) -> bool:
        """
        :return: ``True`` if self has no parent, else ``False``.
        :rtype: bool
        """
        return True if self.get_parent() is None else False

    @property
    def level(self) -> int:
        """
        :return: ``0`` for ``root``, ``1, 2 etc.`` for each layer of children
        :rtype: nonnegative int

        >>> class TestTree(Tree):
        ...   def _check_child_to_be_added(self, child):
        ...      return True
        >>> root = TestTree()
        >>> root.level
        0
        >>> ch = root.add_child(TestTree()).add_child(TestTree()).add_child(TestTree())
        >>> ch.level
        3
        """
        if self.get_parent() is None:
            return 0
        else:
            return self.get_parent().level + 1

    @property
    def next(self) -> Optional['Tree']:
        """
        :return: next sibling. ``None`` if this is the last current child of the parent.
        :rtype: :obj:`~tree.tree.Tree`
        """
        if self.up and self != self.up.get_children()[-1]:
            return self.up.get_children()[self.up.get_children().index(self) + 1]
        else:
            return None

    @property
    def previous(self) -> Optional['Tree']:
        """
        :return: previous sibling. ``None`` if this is the first child of the parent.
        :rtype: :obj:`~tree.tree.Tree`
        """
        if self.up and self != self.up.get_children()[0]:
            return self.up.get_children()[self.up.get_children().index(self) - 1]
        else:
            return None

    @property
    def up(self) -> 'Tree':
        """
        :return: :obj:`get_parent()`
        :rtype: :obj:`~tree.tree.Tree`
        """
        return self.get_parent()

    def add_child(self, child: 'Tree') -> 'Tree':
        """
        Check and add child to list of children. Child's parent is set to self.

        :param child:
        :return: child
        :rtype: :obj:`~tree.tree.Tree`
        """
        self._check_child_to_be_added(child)
        child._parent = self
        self._children.append(child)
        return child

    def get_children(self) -> List['Tree']:
        """
        :return: list of added children.
        :rtype: List[:obj:`~tree.tree.Tree`]
        """
        return self._children

    def get_coordinates_in_tree(self) -> str:
        """
        :return: 0 for ``root``. 1, 2, ... for layer 1. Other layers: x.y.z.... Example: 3.2.2 => third child of secod child of second child
                 of the root.
        :rtype: str

        >>> class TestTree(Tree):
        ...   def _check_child_to_be_added(self, child):
        ...      return True
        >>> root = TestTree()
        >>> root.get_coordinates_in_tree()
        '0'
        >>> child1 = root.add_child(TestTree())
        >>> child2 = root.add_child(TestTree())
        >>> grandchild1 = child2.add_child(TestTree())
        >>> grandchild2 = child2.add_child(TestTree())
        >>> child1.get_coordinates_in_tree()
        '1'
        >>> child2.get_coordinates_in_tree()
        '2'
        >>> grandchild1.get_coordinates_in_tree()
        '2.1'
        >>> grandchild2.get_coordinates_in_tree()
        '2.2'
        """
        if self.level == 0:
            return '0'
        elif self.level == 1:
            return str(self.get_parent().get_children().index(self) + 1)
        else:
            return f"{self.get_parent().get_coordinates_in_tree()}.{self.get_parent().get_children().index(self) + 1}"

    def get_indentation(self) -> str:
        """
        :return: indentation according to ``level`` (layer number)
        :rtype: str
        """
        indentation = ''
        for i in range(self.level):
            indentation += '    '
        return indentation

    def get_parent(self) -> 'Tree':
        """
        :return: parent. ``None`` for ``root``.
        :rtype: :obj:`~tree.tree.Tree`
        """
        return self._parent

    def get_leaves(self, key: Optional[Callable] = None) -> list:
        """
        :param key: An optional callable to be called on each leaf.
        :return: nested list of leaves or values of key(leaf) for each leaf
        :rtype: nested list of :obj:`~tree.tree.Tree`
        """
        output = []
        for child in self.get_children():
            if not child.is_leaf:
                output.append(child.get_leaves(key=key))
            else:
                if key is not None:
                    output.append(key(child))
                else:
                    output.append(child)

        return output

    def get_root(self) -> 'Tree':
        """
        :return: ``root`` (upmost node of a tree which has no parent)
        :rtype: :obj:`~tree.tree.Tree`
        """
        node = self
        parent = node.get_parent()
        while parent is not None:
            node = parent
            parent = node.get_parent()
        return node

    def get_layer(self, level: int, key: Optional[Callable] = None) -> list:
        """
        :param level: layer number where 0 is the ``root``.
        :param key: An optional callable for each node in the layer.
        :return: All nodes on this level. The leaves of branches which are shorter than the given level will be repeated on this and all
                 following layers.
        :rtype: list
        """
        if level == 0:
            output = [self]
        elif level == 1:
            output = self.get_children()
        else:
            output = []
            for child in self.get_layer(level - 1):
                if child.is_leaf:
                    output.append(child)
                else:
                    output.extend(child.get_children())
        if key is None:
            return output
        else:
            return [key(child) for child in output]

    def iterate_leaves(self) -> Iterator['Tree']:
        """
        :return: A generator iterating over all leaves.
        """
        for node in self.traverse():
            if node.is_leaf:
                yield node

    def remove(self, child: 'Tree') -> None:
        """
        Child's parent will be set to ``None`` and child will be removed from list of children.

        :param child:
        :return: None
        """
        if child not in self.get_children():
            raise ChildNotFoundError
        child._parent = None
        self.get_children().remove(child)

    def remove_children(self) -> None:
        """
        Calls :obj:`remove()` on all children.

        :return: None
        """
        for child in self.get_children()[:]:
            child.up.remove(child)

    def replace_child(self, old, new, index: int = 0) -> None:
        """
        :param old: child or function
        :param new: child
        :param index: index of old in list of old appearances
        :return: None
        """
        if hasattr(old, '__call__'):
            list_of_olds = [ch for ch in self.get_children() if old(ch)]
        else:
            list_of_olds = [ch for ch in self.get_children() if ch == old]
        if not list_of_olds:
            raise ValueError(f"{old} not in list.")
        self._check_child_to_be_added(new)
        old_index = self.get_children().index(list_of_olds[index])
        old_child = self.get_children()[old_index]
        self.get_children().remove(old_child)
        self.get_children().insert(old_index, new)
        old_child._parent = None
        new._parent = self

    def reversed_path_to_root(self) -> Iterator['Tree']:
        """
        :return: path from self upwards through all ancestors up to the ``root``.
        """
        yield self
        if self.get_parent():
            for node in self.get_parent().reversed_path_to_root():
                yield node

    def traverse(self, mode: str = 'dfs') -> Iterator['Tree']:
        """
        Traverse all nodes tree nodes.

        :param str mode:  ``dfs``: depth first search; ``bfs``: breadth first search
        :return: generator
        """
        if mode == 'dfs':
            yield self
            for child in self.get_children():
                for node in child.traverse(mode=mode):
                    yield node
        elif mode == 'bfs':
            queue = [self]
            while queue:
                current = queue.pop()
                yield current
                for child in current.get_children():
                    queue.insert(0, child)
        else:
            raise NotImplementedError

    def tree_representation(self, key: Optional[Callable] = None, tab: Optional[Callable] = None) -> str:
        """
        :param key: An optional callable if ``None`` ``compact_repr`` property of each node is called.
        :param tab: An optional callable if ``None`` ``get_indentation()`` method of each node is called.
        :return: a representation of all nodes as string in tree form.
        :rtype: str
        """
        if not key:
            key = lambda x: x.compact_repr

        if not tab:
            tab = lambda x: x.get_indentation()

        output = ''
        for node in self.traverse():
            output += tab(node) + key(node)
            output += '\n'
        return output
