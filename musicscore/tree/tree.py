from musicscore.basic_functions import flatten
import copy


class Tree(object):
    """
    A simple Tree class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._children = []
        self._up = None

    @property
    def up(self):
        return self._up

    @property
    def is_root(self):
        if self._up is None:
            return True
        else:
            return False

    @property
    def index(self):
        if self.is_root:
            _index = [0]
        elif self.get_distance() == 1:
            _index = [self.up.get_children().index(self) + 1]
        else:
            _index = self.up.index
            _index.append(self.up.get_children().index(self) + 1)
        return _index

    def get_root(self):
        if self.is_root:
            return self

        root = self.up
        while not root.is_root:
            root = root.get_root()
        return root

    def get_children(self):
        return self._children

    def add_child(self, child):
        if not isinstance(child, Tree):
            raise TypeError('child must be of type Tree and not {}'.format(type(child)))
        self._children.append(child)
        child._up = self
        return child

    def remove_child(self, child):
        try:
            self._children.remove(child)
        except ValueError:
            pass

    def clear_children(self):

        self._children.clear()

    def get_branch(self):
        output = [self]
        node = self
        while node.up is not None:
            output.append(node.up)
            node = node.up
        output.reverse()
        return output

    def get_common_ancestor(self, *other_nodes):
        for other_node in other_nodes:
            if self.get_root() != other_node.get_root():
                raise Exception('{} has not the same root'.format(other_node))

        me_branch = self.get_branch()[:]
        other_branches = [other_node.get_branch()[:] for other_node in other_nodes]

        for node in reversed(me_branch):
            node_in_all_branches = True
            for branch in other_branches:
                if node not in branch:
                    node_in_all_branches = False
                    break
            if node_in_all_branches:
                return node

        # intersection = list(set(a) - (set(a) - set(b)))
        # print(a)
        # print(b)
        # print(intersection)

    @property
    def is_leaf(self):
        if len(self.get_children()) == 0:
            return True
        else:
            return False

    def get_leaves(self, key=None):
        output = []
        for index, child in enumerate(self.get_children()):
            if not child.is_leaf:
                output.append(child.get_leaves(key=key))
            else:
                if key is not None:
                    output.append(key(child))
                else:
                    output.append(child)

        return output

    def traverse(self):
        yield self
        for child in self.get_children():
            for grand_child in child.traverse():
                yield grand_child

    def dump(self):
        output = []
        for node in self.traverse():
            output.append(node)
        return output

    def get_distance(self, reference=None):
        if reference is None:
            reference = self.get_root()

        if self.is_root:
            return 0
        parent = self.up
        count = 1
        while parent is not reference:
            parent = parent.up
            count += 1
            if parent.is_root and parent is not reference:
                return None
        return count

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

    def clone(self, except_nodes=[]):
        if self not in except_nodes:
            cloned = copy.copy(self)
            cloned._children = []
            for child in self.get_children():
                cloned.add_child(child.clone(except_nodes=except_nodes))
            return cloned
        else:
            return self

    def goto(self, index):

        if index == [0]:
            return self

        if len(index) == 1:
            return self.get_children()[index[0] - 1]

        return self.goto(index[:1]).goto(index[1:])

    def replace_node(self, new_node):
        if self.is_root:
            raise Exception('root cannot be replaced')
        else:
            index = self.up.get_children().index(self)
            new_node._up = self._up
            self.up.get_children()[index] = new_node
            self._up = None

    def traverse_leaves(self):
        for leaf in flatten(self.get_leaves()):
            yield leaf

    def find_leaf(self, condition):
        for leaf in self.traverse_leaves():
            if condition(leaf) is True:
                return leaf
        return False

    def repair_parenthood(self):
        for child in self.get_children():
            child._up = self

    def __deepcopy__(self):
        copied = self.__class__()
        for item in self.__dict__.items():
            key = item[0]
            value = item[1]

            if key not in ('_children', '_up'):
                try:
                    new_value = value.__deepcopy__()
                except (AttributeError, TypeError):
                    new_value = value

                copied.__dict__[key] = new_value

        for child in self.get_children():
            copied.add_child(child.__deepcopy__())

        return copied

    def no_child_copy(self, *arguments, **kwargs):
        copied = self.__class__(*arguments, **kwargs)
        for item in self.__dict__.items():
            key = item[0]
            value = item[1]

            if key not in ('_children', '_up'):
                try:
                    new_value = value.__copy__()
                except (AttributeError, TypeError):
                    new_value = value

                copied.__dict__[key] = new_value

        return copied


class TreeNode(Tree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
