from musictree import Score, Chord, A
from musictree.tests.util import IdTestCase


class TestAddLyrics(IdTestCase):
    def setUp(self):
        super().setUp()
        self.score = Score()
        self.part = self.score.add_part('p1')

    def test_add_syllables(self):
        # chords = [Chord(A(4), 1) for _ in range(6)]
        # chords.append(Chord(A(4), 2))
        self.fail()


