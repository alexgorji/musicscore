from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import IdTestCase


class TestQuantization(IdTestCase):
    def test_get_and_set_possible_subdivisions(self):
        s = Score()
        p = s.add_child(Part('p1'))
        m = p.add_measure()
        s = m.get_children()[0]
        v = s.get_children()[0]
        beats = v.get_children()
        for beat in beats:
            assert beat.get_possible_subdivisions() == [2, 3, 4, 5, 6, 7, 8]
        beats[0].quarter_duration = 1 / 2
        assert beats[0].get_possible_subdivisions() == [2, 3, 4, 5]
        beats[0].quarter_duration = 1 / 4
        assert beats[0].get_possible_subdivisions() == [2, 3]
        beats[0].quarter_duration = 1 / 8
        assert beats[0].get_possible_subdivisions() is None
        v.set_possible_subdivisions([2, 3, 4, 6], beat_quarter_duration=1)
        beats[1].set_possible_subdivisions([2, 4])
        assert beats[0].get_possible_subdivisions() is None
        assert beats[1].get_possible_subdivisions() == [2, 4]
        for beat in beats[2:]:
            assert beat.get_possible_subdivisions() == [2, 3, 4, 6]

        with self.assertRaises(ValueError):
            beats[1].set_possible_subdivisions([2, 4], beat_quarter_duration=0.5)
