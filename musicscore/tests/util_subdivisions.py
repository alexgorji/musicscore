import itertools
import math

from quicktions import Fraction


def _permute(l):
    return list(dict.fromkeys(itertools.permutations(l)))


def generate_all_triplets_manually():
    output = [tuple(3 * [Fraction(1, 3)])]
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 3), Fraction(2, 3)]))))
    return output


def generate_all_16ths_manually():
    output = [tuple(4 * [Fraction(1, 4)])]
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 4), Fraction(3, 4)]))))
    return output


def generate_all_quintuplets_manually():
    output = [tuple(5 * [Fraction(1, 5)])]
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 5), Fraction(1, 5), Fraction(1, 5), Fraction(2, 5)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 5), Fraction(2, 5), Fraction(2, 5)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(2, 5), Fraction(3, 5)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 5), Fraction(4, 5)]))))
    return output


def generate_all_sextuplets_manually():
    output = [tuple(6 * [Fraction(1, 6)])]
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(1, 6),
                                                   Fraction(2, 6)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 6), Fraction(1, 6), Fraction(2, 6),
                                                             Fraction(2, 6)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(3, 6)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 6), Fraction(2, 6), Fraction(3, 6)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 6), Fraction(1, 6), Fraction(4, 6)]))))
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 6), Fraction(5, 6)]))))
    return output


def generate_all_septuplets_manually():
    output = [tuple(7 * [Fraction(1, 7)])]
    output.extend(list(dict.fromkeys(
        itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(1, 7),
                                Fraction(2, 7)]))))
    output.extend(
        list(dict.fromkeys(
            itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(2, 7), Fraction(2, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(2, 7), Fraction(2, 7), Fraction(2, 7)]))))
    output.extend(
        list(dict.fromkeys(
            itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(3, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(2, 7), Fraction(3, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(3, 7), Fraction(3, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(4, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(3, 7), Fraction(4, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(3, 7), Fraction(2, 7), Fraction(2, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(5, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(2, 7), Fraction(5, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(6, 7)]))))
    return output


def generate_all_32nds_manually():
    output = [tuple(8 * [Fraction(1, 8)])]
    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(2, 8)] + 6 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(2 * [Fraction(2, 8)] + 4 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(3 * [Fraction(2, 8)] + 2 * [Fraction(1, 8)]))))

    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(3, 8)] + 5 * [Fraction(1, 8)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations(1 * [Fraction(3, 8)] + 1 * [Fraction(2, 8)] + 3 * [Fraction(1, 8)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations(1 * [Fraction(3, 8)] + 2 * [Fraction(2, 8)] + 1 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(2 * [Fraction(3, 8)] + 2 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(2 * [Fraction(3, 8)] + 1 * [Fraction(2, 8)]))))

    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(4, 8)] + 4 * [Fraction(1, 8)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations(1 * [Fraction(4, 8)] + 1 * [Fraction(2, 8)] + 2 * [Fraction(1, 8)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations(1 * [Fraction(4, 8)] + 1 * [Fraction(3, 8)] + 1 * [Fraction(1, 8)]))))

    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(5, 8)] + 3 * [Fraction(1, 8)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations(1 * [Fraction(5, 8)] + 1 * [Fraction(2, 8)] + 1 * [Fraction(1, 8)]))))
    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(5, 8)] + 1 * [Fraction(3, 8)]))))

    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(6, 8)] + 2 * [Fraction(1, 8)]))))

    output.extend(list(dict.fromkeys(itertools.permutations(1 * [Fraction(7, 8)] + 1 * [Fraction(1, 8)]))))
    return output


def generate_all_nonuplets():
    output = [tuple(9 * [Fraction(1, 9)])]
    proportions = [
        1 * [2] + 7 * [1],
        2 * [2] + 5 * [1],
        3 * [1] + 3 * [2],
        1 * [1] + 4 * [2],
        6 * [1] + [3],
        3 * [1] + 2 * [3],
        3 * [3],
        5 * [1] + [4],
        4 * [1] + [5],
        3 * [1] + [6],
        2 * [1] + [7],
        1 * [1] + [8],

    ]
    output.extend(list(dict.fromkeys(
        itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(1, 7),
                                Fraction(2, 7)]))))
    output.extend(
        list(dict.fromkeys(
            itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(2, 7), Fraction(2, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(2, 7), Fraction(2, 7), Fraction(2, 7)]))))
    output.extend(
        list(dict.fromkeys(
            itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(3, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(2, 7), Fraction(3, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(3, 7), Fraction(3, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(1, 7), Fraction(4, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(3, 7), Fraction(4, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(5, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(2, 7), Fraction(5, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(6, 7)]))))
    return output


def get_first_pattern(first_element, sum_):
    output = (sum_ // first_element) * [first_element]
    if sum(output) != sum_:
        output += [sum_ - sum(output)]
    return output


def get_next_pattern(current_pattern):
    if set(current_pattern) == {1}:
        return None
    subdivision = sum(current_pattern)
    first_element = current_pattern[0]
    if len(current_pattern) > 1:
        other_elements = current_pattern[1:]
    else:
        other_elements = None
    if not other_elements or set(other_elements) == {1}:
        return get_first_pattern(first_element - 1, subdivision)
    else:
        output = [first_element] + get_next_pattern(other_elements)
        return output


def subdivision_patterns_generator(subdivision):
    current = [subdivision]
    current = get_next_pattern(current)
    while current:
        yield current
        current = get_next_pattern(current)


def generate_all_subdivision_patterns(subdivision, remove_larger_subdivisions=False):
    output = []
    patterns = subdivision_patterns_generator(subdivision)
    if remove_larger_subdivisions:
        patterns = [pat for pat in patterns if not (min(pat) != 1 and math.gcd(*pat) != 1)]
    for pattern in patterns:
        output.extend(_permute(pattern))
    return output



def generate_all_subdivisions(subdivision, remove_larger_subdivisions=False):
    return [tuple([Fraction(x, subdivision) for x in pat]) for pat in
            generate_all_subdivision_patterns(subdivision, remove_larger_subdivisions)]


def generate_subdivsion_test_patterns(subdivision, remove_larger_subdivision=False):
    def get_last_element():
        return subdivision - x - offset

    offset = 0
    while offset < subdivision:
        x = 1
        while get_last_element():
            if offset:
                pattern = (offset, x, get_last_element())
            else:
                pattern = (x, get_last_element())
            x += 1
            if remove_larger_subdivision and (min(pattern) != 1 and math.gcd(*pattern) != 1):
                continue
            yield pattern
        offset += 1