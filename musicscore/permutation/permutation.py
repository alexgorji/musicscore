from itertools import cycle


def permute(input_list, permutation_order):
    if input_list is None:
        raise ValueError('input_list cannot be None')
    if permutation_order is None:
        raise ValueError('permutation_order cannot be None')
    if len(input_list) == len(permutation_order):
        return [input_list[m - 1] for m in permutation_order]
    else:
        raise ValueError('input_list = {} and permutation_order {} must have the same length'.format(str(input_list),
                                                                                                     str(
                                                                                                         permutation_order)))


def self_permute(permutation_order):
    output = [permutation_order]

    for i in range(1, len(permutation_order)):
        output.append(permute(output[i - 1], permutation_order))

    return output


def multiplied_permutation(permutation_order, multi):
    self_permuted = self_permute(permutation_order)
    multiplier = self_permuted[multi - 1]

    return [self_permuted[m - 1] for m in multiplier]


class Permutation(object):
    class Element(object):
        def __init__(self, value, order):
            self.value = value
            '''order is order of element in the original input_list'''
            self.order = order

    def __init__(self, input_list, main_permutation_order, multi=(1, 1)):

        self._iterator = None
        self._element_generator = None

        self.input_list = input_list
        self.main_permutation_order = list(main_permutation_order)
        self.multi = multi

    @property
    def multiplied_order(self):
        def reordered(multiplied):
            index_of_first_row = None
            for index_of_first_row in range(len(multiplied)):
                if multiplied[index_of_first_row][0] == self.main_permutation_order:
                    break
            output = []
            for i in range(index_of_first_row, index_of_first_row + len(multiplied)):
                output.append(multiplied[i % len(multiplied)])
            return output

        self_permuted_order = self_permute(self.main_permutation_order)
        multiplied = [permute(self_permuted_order, current_order) for current_order in self_permuted_order]
        multiplied = reordered(multiplied)
        return [order for orders in multiplied for order in orders]

    @property
    def iterator(self):
        if self._iterator is None:
            self._iterator = cycle(self.multiplied_order)
            if self.multi is None:
                raise Exception('multi must be set first')

            first_index = (self.multi[0] - 1) * len(self.main_permutation_order) + (self.multi[1] - 1)
            for i in range(first_index):
                self._iterator.__next__()

        return self._iterator

    def next(self):
        return self.iterator.__next__()

    @property
    def element_generator(self):
        if self._element_generator is None:
            def gen():
                next_permutations = self.next()
                while True:
                    for order in next_permutations:
                        yield self.Element(value=self.input_list[order - 1], order=order)

                    next_permutations = self.next()

            self._element_generator = gen()

        return self._element_generator

    def next_element(self):
        return self.element_generator.__next__()
