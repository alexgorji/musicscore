import inspect
from unittest import skip

from musicscore import Score
from musicscore.tests.util import IdTestCase, generate_repetitions, generate_path


class TestCautionaryAccidentalSigns(IdTestCase):
    def setUp(self):
        super().setUp()
        self.score = Score()
        self.part = self.score.add_part('p.')

    @skip
    def test_cautionary_signs_repetition_traditional(self):
        self.part.show_accidental_signs = 'traditional'
        generate_repetitions(self.part)
        path = generate_path(inspect.currentframe())
        self.score.export_xml(path)

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
