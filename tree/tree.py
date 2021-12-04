from abc import ABC, abstractmethod, abstractproperty


class TreePresentation(ABC):
    @property
    def is_leaf(self):
        if not self.get_children():
            return True
        else:
            return False

    def iterate_leaves(self):
        for node in self.traverse():
            if node.is_leaf:
                yield node

    @abstractmethod
    def get_children(self):
        pass

    def traverse(self):
        if self is not None:
            yield self
            for child in self.get_children():
                for node in child.traverse():
                    yield node

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

    @abstractmethod
    def get_parent(self):
        pass

    def tree_repr(self, attr='compact_repr'):
        def _indentation(x):
            indentation = ''
            for i in range(x.get_layer_number()):
                indentation += '    '
            return indentation

        """
        A string representation of the tree structure
        """
        output = ''
        for node in self.traverse():
            output += _indentation(node) + getattr(node, attr)
            output += '\n'

        return output
