import itertools
from fractions import Fraction


def _permute(l):
    return list(dict.fromkeys(itertools.permutations(l)))


def generate_all_sextuplets():
    output = [tuple(6 * [Fraction(1, 6)])]
    output.extend(
        _permute([Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(2, 6)]))
    output.extend(
        _permute([Fraction(1, 6), Fraction(1, 6), Fraction(2, 6), Fraction(2, 6)]))
    output.extend(
        _permute([Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(3, 6)]))
    output.extend(
        _permute([Fraction(1, 6), Fraction(2, 6), Fraction(3, 6)]))
    output.extend(
        _permute([Fraction(1, 6), Fraction(1, 6), Fraction(4, 6)])
    )
    output.extend(
        _permute([Fraction(1, 6), Fraction(5, 6)])
    )
    return output


def generate_all_septuplets():
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
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(1, 7), Fraction(5, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(2, 7), Fraction(5, 7)]))))
    output.extend(
        list(dict.fromkeys(itertools.permutations([Fraction(1, 7), Fraction(6, 7)]))))
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


def generate_all_triplets():
    output = [tuple(3 * [Fraction(1, 3)])]
    output.extend(list(dict.fromkeys(itertools.permutations([Fraction(1, 3), Fraction(2, 3)]))))
    return output
