import inspect
from pathlib import Path
from unittest import skip

from musictree import Score, Chord, C, Time, generate_measures
from musictree.tests.util import IdTestCase


def generate_path(frame):
    f = str(inspect.getframeinfo(frame).function) + '.xml'
    path = Path(__file__).parent / f
    return path


class TestCautionaryAccidentalSigns(IdTestCase):
    def setUp(self):
        super().setUp()
        self.score = Score()
        self.part = self.score.add_part('p.')

    def generate_repetitions(self):
        for m in generate_measures([(3, 8), (3, 4)] + 2 * [(6, 4)] + 3 * [(4, 4)] + [(5, 4)]):
            self.part.add_child(m)

        for qd in 3 * [0.5] + 3 * [1] + 4 * [1.5] + 3 * [2] + [1, 1, 1, 2, 1, 1, 2, 2, 3, 3, 3, 4, 4, 2, 2, 1.5, 1.5,
                                                               1.5]:
            self.part.add_chord(Chord(C(5, '#'), qd))

    def test_cautionary_signs_repetition_traditional(self):
        self.generate_repetitions()
        path = generate_path(inspect.currentframe())
        self.score.export_xml(path)

    # self.fail()

    @skip
    def test_cautionary_signs_repetition_modern(self):
        path = generate_path(inspect.currentframe())
        print(path)
        # self.fail()

    @skip
    def test_cautionary_signs_traditional(self):
        path = generate_path(inspect.currentframe())
        print(path)
        # self.fail()

    @skip
    def test_cautionary_signs_modern(self):
        path = generate_path(inspect.currentframe())
        print(path)
        # self.fail()

    @skip
    def test_cautionary_signs_different_octaves_traditional(self):
        path = generate_path(inspect.currentframe())
        print(path)
        # self.fail()

    def test_cautionary_signs_different_octaves_modern(self):
        path = generate_path(inspect.currentframe())
        print(path)
        # self.fail()

    def test_cautionary_signs_different_voice_traditional(self):
        path = generate_path(inspect.currentframe())
        print(path)
        # self.fail()

    def test_cautionary_signs_different_voice_modern(self):
        path = generate_path(inspect.currentframe())
        print(path)
        # self.fail()

    def test_cautionary_signs_multi_staff_traditional(self):
        path = generate_path(inspect.currentframe())
        print(path)
        # self.fail()

    def test_cautionary_signs_multi_staff_modern(self):
        path = generate_path(inspect.currentframe())
        print(path)
        # self.fail()
