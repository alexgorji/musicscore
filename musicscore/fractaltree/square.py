from musicscore.fractaltree.fractaltree import FractalMusic


class Module(FractalMusic):
    def __init__(self, row_number=None, column_number=None, *args, **kargs):
        super(Module, self).__init__(*args, **kargs)
        self.row_number = row_number
        self.column_number = column_number


class Square(object):
    def __init__(self, duration, proportions, tree_permutation_order, first_multi=(1, 1)):

        self._duration = None
        self._proportions = None
        self._modules = {}
        self._tree_permutation_order = None
        self._first_multi = (1, 1)
        self._side_size = None

        self.duration = duration
        self.proportions = proportions
        self.tree_permutation_order = tree_permutation_order
        self.first_multi = first_multi

    @property
    def side_size(self):
        return self._side_size

    @property
    def duration(self):
        if self.modules != {}:
            durations = map(lambda module: module.duration, self.modules.values())
            self._duration = sum(durations)
        return self._duration

    @duration.setter
    def duration(self, value):
        if value is None:
            raise ValueError('duration cannot be None')
        self._duration = value
        self._calculate_module_values()

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
        self._calculate_module_values()

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
        self._calculate_module_values()

    @property
    def modules(self):
        return self._modules

    @property
    def first_multi(self):
        return self._first_multi

    @first_multi.setter
    def first_multi(self, value):
        self._first_multi = value
        if self._modules != {}:
            for key in self._modules.keys():
                # print 'key', key
                module = self._modules[key]
                module.multi = self.index_to_r_c(
                    self.r_c_to_index(module.row_number, module.column_number) + self.r_c_to_index(self.first_multi[0],
                                                                                                   self.first_multi[1]))

    def get_module(self, *args):
        args = tuple(args)
        return self.modules[args]

    def get_row(self, row_number):
        if row_number < 1 or row_number > self.side_size:
            raise ValueError('row_number can be between 1 and {}'.format(self.side_size))

        return [self.get_module(row_number, i) for i in range(1, self.side_size + 1)]

    def get_row_durations(self, row_number):
        if row_number > self.side_size or row_number < 0 or isinstance(row_number, int) == False:
            raise ValueError('row_number')
        else:
            row_durations = []
            row_keys = [(row_number, i + 1) for i in range(self.side_size)]
            for key in row_keys:
                row_durations.append(self.modules[key].duration)
            return row_durations

    def index_to_r_c(self, index):
        row = int(index / self.side_size) % self.side_size + 1
        column = index % self.side_size + 1
        return row, column

    def r_c_to_index(self, row, column):
        index = ((row - 1) * self.side_size) + (column - 1)
        return index

    def _calculate_module_values(self):
        if self.duration is not None and self.proportions is not None and self.tree_permutation_order is not None:
            row_durations = [self.duration * prop / float(sum(self.proportions)) for prop in self.proportions]
            for (row, column) in [(i + 1, j + 1) for i in range(self.side_size) for j in range(self.side_size)]:
                module_durations = [row_durations[row - 1] * prop / float(sum(self.proportions)) for prop in
                                    self.proportions]
                multi = self.index_to_r_c(
                    self.r_c_to_index(row, column) + self.r_c_to_index(self.first_multi[0], self.first_multi[1]))
                module = Module(duration=module_durations[column - 1],
                                tree_permutation_order=self.tree_permutation_order, proportions=self.proportions,
                                multi=multi)
                (module.row_number, module.column_number) = (row, column)
                self._modules[(row, column)] = module
            # durations = map(lambda module: module.duration, self.modules.values())

    def change_module_duration(self, row_number, column_number, new_duration):
        factor = new_duration / self.get_module(row_number, column_number).duration
        for key in self.modules:
            self.modules[key].duration = self.modules[key].duration * factor
