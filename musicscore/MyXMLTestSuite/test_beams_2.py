import inspect
from itertools import permutations

from musicscore import Score, Time, C, Chord
from musicscore.tests.util import IdTestCase, generate_path

patterns = [(1, 1), (1, 3), (1, 1, 2), (1, 7), (1, 1, 6), (1, 2, 5), (1, 3, 4), (1, 1, 1, 5), (1, 1, 2, 4),
            (1, 1, 3, 3), (1, 2, 2, 3), (1, 1, 1, 1, 4), (1, 1, 1, 2, 3), (1, 2, 2, 2, 1), (1, 1, 1, 1, 1, 3),
            (1, 1, 1, 1, 2, 2), (1, 1, 1, 1, 1, 1, 2)]
permuted_patterns = [list(set(list(permutations(pattern)))) for pattern in patterns]


class TestBeams(IdTestCase):
    def setUp(self):
        super().setUp()
        self.score = Score()
        self.part = self.score.add_part('p1')

    def test_beams_complicated_rhythm(self):
        self.part.add_measure(Time(1, 4))
        for list_of_patterns in permuted_patterns:
            for pattern in list_of_patterns:
                for index, qd in enumerate([x / sum(pattern) for x in pattern]):
                    ch = Chord(C(5), qd)
                    if index == 0:
                        ch.add_lyric(pattern, justify='left')
                    self.part.add_chord(ch)

        path = generate_path(inspect.currentframe())
        self.score.export_xml(path)

    def test_beams_arbitrary_groups(self):
        qds = None