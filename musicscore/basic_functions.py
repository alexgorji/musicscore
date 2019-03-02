import re
import functools


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
