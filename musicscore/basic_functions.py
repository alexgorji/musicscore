import re
import functools
from itertools import cycle, islice


def replace_dash(name):
    if '-' in name:
        return re.sub(r'-', '_', name)
    elif '_' in name:
        return re.sub(r'_', '-', name)
    else:
        return name


def is_empty(string):
    if re.sub(r'\s', '', string) == '':
        return True
    else:
        return False


def lcm(l):
    """least common multiple of numbers in a list"""

    def _lcm(a, b):
        if a > b:
            greater = a
        else:
            greater = b

        while True:
            if greater % a == 0 and greater % b == 0:
                lcm_ = greater
                break
            greater += 1

        return lcm_

    return functools.reduce(lambda x, y: _lcm(x, y), l)


def flatten(x):
    if hasattr(x, "__iter__"):
        result = []
        for el in x:
            if hasattr(el, "__iter__") and not isinstance(el, str):
                result.extend(flatten(el))
            else:
                result.append(el)
        return result
    else:
        return [x]


def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))


def substitute(input_list, old_element, new_elements):
    index = input_list.index(old_element)
    try:
        new_elements = list(new_elements)
    except TypeError:
        new_elements = [new_elements]

    output_list = input_list[:index] + new_elements + input_list[index + 1:]
    return output_list


def dToX(input_list, first_element=0):
    if isinstance(input_list, list) is False:
        raise TypeError('xToD(input_list)')
    else:
        output = [first_element]
        for i in range(len(input_list)):
            output.append(input_list[i] + output[i])
        return output


def xToD(input_list):
    result = []
    for i in range(1, len(input_list)):
        result.append(input_list[i] - input_list[i - 1])
    return result


def step_sums(input):
    # if input == {}:
    #     return {}
    if not input:
        return []

    # if isinstance(input, dict):
    #     input_items = zip(*input.items())[1]
    #     input_keys = zip(*input.items())[0]
    #     output_items = [input_items[0]]
    #     for i in range(1, len(input_items)):
    #         output_items.append(output_items[-1] + input_items[i])
    #
    #     return dict(zip(input_keys, output_items))

    result = [input[0]]
    for i in range(1, len(input)):
        result.append(result[-1] + input[i])
    return result


def one_dimensional(x):
    if hasattr(x, '__iter__'):
        result = []
        for list_el in x:
            if hasattr(list_el, "__iter__") and not hasattr(list_el[0], "__iter__"):
                result.append(list_el)
            else:
                result.extend(one_dimensional(list_el))
        return result
    else:
        return [x]

class Scale(object):
    def __init__(self, old_min, old_max, new_min, new_max, step=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_min = old_min
        self.old_max = old_max
        self.new_min = new_min
        self.new_max = new_max
        self._step = None
        self.step = step

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, val):
        if val is not None and val <= 0:
            raise TypeError('step.value must positive not {}'.format(type(val)))
        self._step = val

    def __call__(self, x):
        y = self.new_min + (self.new_max - self.new_min) * (x - self.old_min) / (self.old_max - self.old_min)
        if self.step:
            y = round(y / self.step) * self.step
        return y
