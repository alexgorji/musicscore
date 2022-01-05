from abc import ABC, abstractmethod


class Tree(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent = None
        self._children = []

    @property
    def is_leaf(self):
        if not self.get_children():
            return True
        else:
            return False

    @abstractmethod
    def _check_child(self, child):
        """
        """

    def add_child(self, child):
        self._check_child(child)
        child._parent = self
        self._children.append(child)
        return child

    def get_children(self):
        return self._children

    def get_parent(self):
        return self._parent

    @property
    def compact_repr(self):
        return self.__str__()

    @property
    def level(self):
        if self.get_parent() is None:
            return 0
        else:
            return self.get_parent().level + 1

    def get_root(self):
        node = self
        parent = node.get_parent()
        while parent is not None:
            node = parent
            parent = node.get_parent()
        return node

    def get_layer_number(self):
        output = 0
        node = self
        while node.get_parent() is not None:
            output += 1
            node = node.get_parent()
        return output

    def iterate_leaves(self):
        for node in self.traverse():
            if node.is_leaf:
                yield node

    def reversed_path_to_root(self):
        yield self
        if self.get_parent():
            for node in self.get_parent().reversed_path_to_root():
                yield node

    def traverse(self):
        if self is not None:
            yield self
            for child in self.get_children():
                for node in child.traverse():
                    yield node

    def get_indentation(self):
        indentation = ''
        for i in range(self.get_layer_number()):
            indentation += '    '
        return indentation

    def tree_representation(self, attr='compact_repr'):

        """
        A string representation of the tree structure
        """
        output = ''
        for node in self.traverse():
            output += node.get_indentation() + getattr(node, attr)
            output += '\n'

        return output
