from musicscore.fractaltree.fractaltree import FractalMusic
from musicscore.fractaltree.square import Square


class Module(FractalMusic):
    def __init__(self, square_number=None, row_number=None, column_number=None, *args, **kargs):
        super(Module, self).__init__(*args, **kargs)
        self.square_number = square_number
        self.square_number = square_number
        self.column_number = column_number
        self.row_number = row_number


class Cube(object):
    def __init__(self, duration, proportions, tree_permutation_order):
        self._side_size = None
        self._duration = None
        self._proportions = None
        self._modules = {}
        self._squares = []
        self._tree_permutation_order = None
        self._first_multi = (1, 1)

        self.duration = duration
        self.proportions = proportions
        self.tree_permutation_order = tree_permutation_order

    @property
    def side_size(self):
        return self._side_size

    @property
    def duration(self):
        if self.squares:
            durations = map(lambda squares: squares.duration, self.squares)
            self._duration = sum(durations)
        return self._duration

    @duration.setter
    def duration(self, value):
        if value is None:
            raise ValueError('duration cannot be None')
        self._duration = value
        self._calculate_squares()

    @property
    def proportions(self):
        return self._proportions

    @proportions.setter
    def proportions(self, values):
        if values is None:
            raise ValueError('proportions cannot be None')
        if self.side_size is not None:
            if len(values) != self.side_size:
                raise ValueError('wrong proportions length')
        else:
            self._side_size = len(values)
        self._proportions = values
        self._calculate_squares()

    @property
    def tree_permutation_order(self):
        return self._tree_permutation_order

    @tree_permutation_order.setter
    def tree_permutation_order(self, values):
        if values is None:
            raise ValueError('tree_permutation_order cannot be None')
        if self.side_size is not None:
            if len(values) != self.side_size:
                raise ValueError('wrong tree_permutation_order length')
        else:
            self._side_size = len(values)
        self._tree_permutation_order = values
        self._calculate_squares()

    @property
    def squares(self):
        return self._squares

    @property
    def modules(self):
        for indexed_square in enumerate(self.squares):
            square_index = indexed_square[0]
            square = indexed_square[1]
            for key in square.modules.keys():
                new_key = (square_index + 1, key[0], key[1])
                self._modules[new_key] = square.modules[key]
                self._modules[new_key].square_number = square_index + 1

        return self._modules

    @property
    def first_multi(self):
        return self._first_multi

    @first_multi.setter
    def first_multi(self, value):
        raise Exception('setting first_multi is not yet implemented')

    def get_square(self, number):
        return self.squares[number - 1]

    def get_module(self, *args):
        args = tuple(args)
        return self.modules[args]

    @property
    def duration(self):
        if self.squares:
            self._duration = sum([square.duration for square in self.squares])
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value
        if self.duration is not None and self.proportions is not None:
            self._calculate_squares()

    def _index_to_multi(self, index):
        row = int(index / self.side_size) % self.side_size + 1
        column = index % self.side_size + 1
        return row, column

    def _multi_to_index(self, multi):
        row = multi[0]
        column = multi[1]
        index = ((row - 1) * self.side_size) + (column - 1)
        return index

    def _calculate_squares(self):
        if self.duration is not None and self.proportions is not None and self.tree_permutation_order is not None:
            square_durations = [self.duration * prop / float(sum(self.proportions)) for prop in self.proportions]
            for indexed_duration in enumerate(square_durations):
                index = indexed_duration[0]
                duration = indexed_duration[1]
                first_multi = self._index_to_multi(self._multi_to_index(self.first_multi) + index * self.side_size)
                self._squares.append(Square(duration=duration, tree_permutation_order=self.tree_permutation_order,
                                            proportions=self.proportions, first_multi=first_multi))

    def change_module_duration(self, category, row, column, new_duration):
        factor = float(new_duration) / self.get_module(category, row, column).duration
        for square in self.squares:
            for key in square.modules.keys():
                square.modules[key].duration = square.modules[key].duration * factor
