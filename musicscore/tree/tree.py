from musicscore.basic_functions import flatten


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
    def id(self):
        if self.is_root:
            _id = [0]
        elif self.get_distance() == 1:
            _id = [self.up.get_children().index(self) + 1]
        else:
            _id = self.up.id
            _id.append(self.up.get_children().index(self) + 1)
        return _id

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
        self._children.remove(child)

    def clear_children(self):
        self._children.clear()

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

    # def get_number_of_layers(self):
    #     if self.is_leaf:
    #         return 0
    #     return max(flatten(self.get_leaves(key=lambda child: child.get_distance(self))))

    # def get_layer(self, layer=0, key=None):
    #
    #     if layer <= self.get_root().get_number_of_layers():
    #
    #         branch_distances = []
    #         for child in self.get_children():
    #             branch_distances.append(child.get_number_of_layers())
    #         print('layer', layer)
    #         print('branch_distances', branch_distances)
    #         if layer == 0:
    #             if key:
    #                 return key(self)
    #             else:
    #                 return self
    #
    #         if layer >= 1:
    #             if layer > max(branch_distances):
    #                 self.get_layer(layer=layer - 1, key=key)
    #
    #             output = []
    #             for i in range(len(self.get_children())):
    #                 child = self.get_children()[i]
    #                 if branch_distances[i] == 1:
    #                     if key:
    #                         output.append(key(child))
    #                     else:
    #                         output.append(child)
    #                 else:
    #                     output.append(child.get_layer(layer - 1, key))
    #
    #             return output
    #     else:
    #         err = 'max layer number=' + str(self.get_number_of_layers())
    #         raise ValueError(err)
