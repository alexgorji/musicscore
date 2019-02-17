class Tree(object):
    """
    A simple Tree class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._children = [].copy()
        self._up = None

    @property
    def up(self):
        return self._up

    def is_root(self):
        if self._up is None:
            return True
        else:
            return False

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
