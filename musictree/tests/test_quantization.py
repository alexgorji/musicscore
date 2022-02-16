from musictree.chord import Chord
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

    def test_simple_quantization(self):
        s = Score()
        p = s.add_child(Part('p1'))
        p.add_measure()
        p.add_chord(Chord(60, 0.2))
        p.add_chord(Chord(60, 3.8))
        assert [ch.quarter_duration for ch in p.get_chords()] == [0.2, 0.8, 3]
        p.get_measure(1).get_staff(1).add_voice()

        b = p.get_measure(1).get_staff(1).get_voice(2).get_beat(1)
        b.set_possible_subdivisions(subdivisions=[2, 3, 4])
        p.add_chord(Chord(60, 0.2), staff_number=1, voice_number=2)
        p.add_chord(Chord(60, 3.8), staff_number=1, voice_number=2)
        assert [ch.quarter_duration for ch in p.get_measure(1).get_staff(1).get_voice(2).get_chords()] == [0.25, 0.75, 3]

        # b = p.get_measure(1).get_staff(1).get_voice(1).get_beat(1)
        # b.set_possible_subdivisions(subdivisions=[2, 3, 4])
        # assert [ch.quarter_duration for ch in p.get_measure(1).get_staff(1).get_voice(1).get_chords()] == [0.25, 0.75, 3]

