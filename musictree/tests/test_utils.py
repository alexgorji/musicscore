from unittest import TestCase

from musictree.score import Score
from musictree.util import isinstance_as_string


class TestUtils(TestCase):
    def test_isinstance_as_string(self):
        assert isinstance_as_string(Score, 'Score')
        assert isinstance_as_string(Score, 'MusicTree')
        assert not isinstance_as_string(Score, 'str')

        class Measure:
            pass

        assert not isinstance_as_string(Measure, 'MusicTree')
