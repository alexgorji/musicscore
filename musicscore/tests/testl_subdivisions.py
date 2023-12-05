from pprint import pprint

from musicscore.tests.test_metronome import TestCase
from musicscore.tests.util_subdivisions import generate_all_subdivisions, \
    subdivision_patterns_generator, get_first_pattern, get_next_pattern, generate_all_triplets_manually, \
    generate_all_16ths_manually, generate_all_quintuplets_manually, generate_all_sextuplets_manually, \
    generate_all_septuplets_manually, generate_all_32nds_manually, generate_all_subdivision_patterns


def _test_list_of_patterns(patterns1, patterns2, show_diff=False):
    if len(patterns1) != len(patterns2):
        if show_diff:
            print(f'different lengths {len(patterns1)} != {len(patterns2)}')
        return False
    a = [sorted(x) for x in patterns1]
    b = [sorted(x) for x in patterns2]
    while a:
        popped = a.pop()
        if popped not in b:
            if show_diff:
                print(f'{popped} not in patterns2')
            return False
    return True


def get_diff(list1, list2):
    diff_1 = []
    diff_2 = []
    for x in list1:
        if x not in list2:
            diff_1.append(x)
    for x in list2:
        if x not in list1:
            diff_2.append(x)
    if not diff_1 and not diff_2:
        return None
    else:
        return {'list1': diff_1, 'list_2': diff_2}


class TestGeneratePatterns(TestCase):

    def test_get_first_pattern(self):
        assert get_first_pattern(2, 3) == [2, 1]
        assert get_first_pattern(1, 3) == [1, 1, 1]
        assert get_first_pattern(3, 4) == [3, 1]
        assert get_first_pattern(2, 4) == [2, 2]
        assert get_first_pattern(1, 4) == [1, 1, 1, 1]
        assert get_first_pattern(4, 5) == [4, 1]
        assert get_first_pattern(3, 5) == [3, 2]
        assert get_first_pattern(2, 5) == [2, 2, 1]
        assert get_first_pattern(1, 5) == [1, 1, 1, 1, 1]
        assert get_first_pattern(5, 6) == [5, 1]
        assert get_first_pattern(4, 6) == [4, 2]
        assert get_first_pattern(3, 6) == [3, 3]
        assert get_first_pattern(2, 6) == [2, 2, 2]
        assert get_first_pattern(1, 6) == [1, 1, 1, 1, 1, 1]

    def test_next_pattern_None(self):
        self.assertIsNone(get_next_pattern([1, 1, 1]))

    def test_next_pattern_is_a_first(self):
        assert get_next_pattern([5, 1]) == [4, 2]
        assert get_next_pattern([4, 1, 1]) == [3, 3]
        assert get_next_pattern([3, 1, 1, 1]) == [2, 2, 2]
        assert get_next_pattern([2, 1, 1, 1, 1]) == [1, 1, 1, 1, 1, 1]

    def test_next_pattern_of_first(self):
        assert get_next_pattern([4, 2]) == [4, 1, 1]
        assert get_next_pattern([3, 3]) == [3, 2, 1]
        assert get_next_pattern([2, 2, 2]) == [2, 2, 1, 1]

    def test_next_pattern_of_not_first(self):
        assert get_next_pattern([3, 2, 1]) == [3, 1, 1, 1]
        assert get_next_pattern([2, 2, 1, 1]) == [2, 1, 1, 1, 1]

    def test_all_next_patterns_until_10(self):
        expected = [
            [2, 1],
            [1, 1, 1]
        ]
        assert list(subdivision_patterns_generator(3)) == expected
        expected = [
            [3, 1],
            [2, 2], [2, 1, 1],
            [1, 1, 1, 1]
        ]
        assert list(subdivision_patterns_generator(4)) == expected
        expected = [
            [4, 1],
            [3, 2], [3, 1, 1],
            [2, 2, 1], [2, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ]
        assert list(subdivision_patterns_generator(5)) == expected
        expected = [
            [5, 1],
            [4, 2], [4, 1, 1],
            [3, 3], [3, 2, 1], [3, 1, 1, 1],
            [2, 2, 2], [2, 2, 1, 1], [2, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1]
        ]
        assert list(subdivision_patterns_generator(6)) == expected
        expected = [
            [6, 1],
            [5, 2], [5, 1, 1],
            [4, 3], [4, 2, 1], [4, 1, 1, 1],
            [3, 3, 1], [3, 2, 2], [3, 2, 1, 1], [3, 1, 1, 1, 1],
            [2, 2, 2, 1], [2, 2, 1, 1, 1], [2, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        assert list(subdivision_patterns_generator(7)) == expected
        expected = [
            [7, 1],
            [6, 2], [6, 1, 1],
            [5, 3], [5, 2, 1], [5, 1, 1, 1],
            [4, 4], [4, 3, 1], [4, 2, 2], [4, 2, 1, 1], [4, 1, 1, 1, 1],
            [3, 3, 2], [3, 3, 1, 1], [3, 2, 2, 1], [3, 2, 1, 1, 1], [3, 1, 1, 1, 1, 1],
            [2, 2, 2, 2], [2, 2, 2, 1, 1], [2, 2, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]
        assert list(subdivision_patterns_generator(8)) == expected
        expected = [
            [8, 1],
            [7, 2], [7, 1, 1],
            [6, 3], [6, 2, 1], [6, 1, 1, 1],
            [5, 4], [5, 3, 1], [5, 2, 2], [5, 2, 1, 1], [5, 1, 1, 1, 1],
            [4, 4, 1], [4, 3, 2], [4, 3, 1, 1], [4, 2, 2, 1], [4, 2, 1, 1, 1], [4, 1, 1, 1, 1, 1],
            [3, 3, 3], [3, 3, 2, 1], [3, 3, 1, 1, 1], [3, 2, 2, 2], [3, 2, 2, 1, 1], [3, 2, 1, 1, 1, 1],
            [3, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 1], [2, 2, 2, 1, 1, 1], [2, 2, 1, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]]
        assert list(subdivision_patterns_generator(9)) == expected
        expected = [[9, 1],
                    [8, 2], [8, 1, 1],
                    [7, 3], [7, 2, 1], [7, 1, 1, 1],
                    [6, 4], [6, 3, 1], [6, 2, 2], [6, 2, 1, 1], [6, 1, 1, 1, 1],
                    [5, 5], [5, 4, 1], [5, 3, 2], [5, 3, 1, 1], [5, 2, 2, 1], [5, 2, 1, 1, 1], [5, 1, 1, 1, 1, 1],
                    [4, 4, 2], [4, 4, 1, 1], [4, 3, 3], [4, 3, 2, 1], [4, 3, 1, 1, 1], [4, 2, 2, 2], [4, 2, 2, 1, 1],
                    [4, 2, 1, 1, 1, 1], [4, 1, 1, 1, 1, 1, 1],
                    [3, 3, 3, 1], [3, 3, 2, 2], [3, 3, 2, 1, 1], [3, 3, 1, 1, 1, 1], [3, 2, 2, 2, 1],
                    [3, 2, 2, 1, 1, 1], [3, 2, 1, 1, 1, 1, 1], [3, 1, 1, 1, 1, 1, 1, 1],
                    [2, 2, 2, 2, 2], [2, 2, 2, 2, 1, 1], [2, 2, 2, 1, 1, 1, 1], [2, 2, 1, 1, 1, 1, 1, 1],
                    [2, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        assert list(subdivision_patterns_generator(10)) == expected

    def test_test_list_patterns(self):
        expected = [[1, 1, 1], [1, 2]]
        a = expected
        b = [[1, 2], [1, 1, 1]]
        c = [[1, 1, 1], [2, 1]]
        d = [[2, 1], [1, 1, 1]]
        e = [[1, 1, 1]]
        f = expected + [[2, 2]]

        assert _test_list_of_patterns(expected, a)
        assert _test_list_of_patterns(expected, b)
        assert _test_list_of_patterns(expected, c, show_diff=True)
        assert _test_list_of_patterns(expected, d)
        assert not _test_list_of_patterns(expected, e)
        assert not _test_list_of_patterns(expected, f)


class TestGenerateAllSubdivisions(TestCase):
    def test_generate_all_triplets(self):
        self.assertIsNone(get_diff(generate_all_subdivisions(3), generate_all_triplets_manually()))

    def test_generate_all_16ths(self):
        self.assertIsNone(get_diff(generate_all_subdivisions(4, remove_larger_subdivisions=True),
                                   generate_all_16ths_manually()))

    def test_generate_all_quintuplets(self):
        self.assertIsNone(get_diff(generate_all_subdivisions(5), generate_all_quintuplets_manually()))

    def test_generate_all_sextuplets(self):
        self.assertIsNone(get_diff(generate_all_subdivisions(6, remove_larger_subdivisions=True),
                                   generate_all_sextuplets_manually()))

    def test_generate_all_septuplets(self):
        self.assertIsNone(get_diff(generate_all_subdivisions(7), generate_all_septuplets_manually()))

    def test_generate_all_32nds(self):
        self.assertIsNone(
            get_diff(generate_all_subdivisions(8, remove_larger_subdivisions=True), generate_all_32nds_manually()))

    def test_number_of_patterns(self):
        output = [len(list(subdivision_patterns_generator(x))) for x in range(2, 16)]
        expected = [1, 2, 4, 6, 10, 14, 21, 29, 41, 55, 76, 100, 134, 175]
        assert expected == output
