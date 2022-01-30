from abc import ABC, abstractmethod


class TreeException(Exception):
    pass


class ChildNotFoundError(TreeException):
    pass


class Tree(ABC):
    TREE_ATTRIBUTES = {'compact_repr', 'is_leaf', 'level', '_parent', '_children', 'up'}

    def __init__(self, *args: object, **kwargs: object) -> object:
        super().__init__(*args, **kwargs)
        self._parent = None
        self._children = []

    @abstractmethod
    def _check_child_to_be_added(self, child):
        """
        """

    @property
    def compact_repr(self):
        return self.__str__()

    @property
    def is_leaf(self):
        if not self.get_children():
            return True
        else:
            return False

    @property
    def is_root(self):
        return True if self.get_parent() is None else False

    @property
    def level(self):
        if self.get_parent() is None:
            return 0
        else:
            return self.get_parent().level + 1

    @property
    def next(self):
        if self.up and self != self.up.get_children()[-1]:
            return self.up.get_children()[self.up.get_children().index(self) + 1]
        else:
            return None

    @property
    def previous(self):
        if self.up and self != self.up.get_children()[0]:
            return self.up.get_children()[self.up.get_children().index(self) - 1]
        else:
            return None

    @property
    def up(self):
        return self.get_parent()

    def add_child(self, child):
        self._check_child_to_be_added(child)
        child._parent = self
        self._children.append(child)
        return child

    def get_children(self):
        return self._children

    def get_coordinates_in_tree(self):
        if self.level == 0:
            return '0'
        elif self.level == 1:
            return str(self.get_parent().get_children().index(self) + 1)
        else:
            return f"{self.get_parent().get_coordinates_in_tree()}.{self.get_parent().get_children().index(self) + 1}"

    def get_indentation(self):
        indentation = ''
        for i in range(self.get_layer_number()):
            indentation += '    '
        return indentation

    def get_parent(self):
        return self._parent

    def get_leaves(self, key=None):
        output = []
        # for node in self.traverse():
        #     if not node.is_leaf:
        #         output.append(node.get_leaves(key=key))
        #     else:
        #         if key is not None:
        #             output.append(key(node))
        #         else:
        #             output.append(node)
        # return output
        for child in self.get_children():
            if not child.is_leaf:
                output.append(child.get_leaves(key=key))
            else:
                if key is not None:
                    output.append(key(child))
                else:
                    output.append(child)

        return output

    def get_root(self):
        node = self
        parent = node.get_parent()
        while parent is not None:
            node = parent
            parent = node.get_parent()
        return node

    def get_layer(self, layer, key=None):
        if layer == 0:
            output = [self]
        elif layer == 1:
            output = self.get_children()
        else:
            output = []
            for child in self.get_layer(layer - 1):
                if child.is_leaf:
                    output.append(child)
                else:
                    output.extend(child.get_children())
        if key is None:
            return output
        else:
            return [key(child) for child in output]

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

    def remove(self, child) -> None:
        if child not in self.get_children():
            raise ChildNotFoundError
        child._parent = None
        self.get_children().remove(child)

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

    def reversed_path_to_root(self):
        yield self
        if self.get_parent():
            for node in self.get_parent().reversed_path_to_root():
                yield node

    def traverse(self, mode='dfs'):
        """
        :param str mode:  dfs: depth first search; bfs: breadth first search
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

    def tree_representation(self, function=None):
        if not function:
            function = lambda x: x.compact_repr

        """
        A string representation of the tree structure
        """
        output = ''
        for node in self.traverse():
            output += node.get_indentation() + function(node)
            output += '\n'

        return output
