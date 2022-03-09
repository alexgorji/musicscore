from musictree.chord import Chord
from musictree.part import Part
from musictree.quarterduration import QuarterDuration
from musictree.score import Score
from musictree.tests.util import IdTestCase
from musictree.util import lcm


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

    def test_quantize_attribute(self):
        s = Score()
        p = s.add_child(Part('p1'))
        m = p.add_measure()

        st = m.get_children()[0]

        v = st.get_children()[0]
        beats = v.get_children()

        assert s.quantize is False
        assert p.quantize is False
        assert m.quantize is False
        assert st.quantize is False
        assert v.quantize is False
        for b in beats:
            assert b.quantize is False

        s.quantize = True
        assert p.quantize is True
        assert m.quantize is True
        assert st.quantize is True
        assert v.quantize is True
        for b in beats:
            assert b.quantize is True

        st.quantize = False
        assert s.quantize is True
        assert p.quantize is True
        assert m.quantize is True
        assert st.quantize is False
        assert v.quantize is False
        for b in beats:
            assert b.quantize is False

        p.quantize = False
        m.quantize = True
        st.quantize = False
        v.quantize = True
        beats[0].quantize = False
        beats[1].quantize = True
        beats[2].quantize = False
        beats[3].quantize = True

        assert s.quantize is True
        assert p.quantize is False
        assert m.quantize is True
        assert st.quantize is False
        assert v.quantize is True
        beats[0].quantize is False
        beats[1].quantize is True
        beats[2].quantize is False
        beats[3].quantize is True

    def test_simple_quantization(self):
        s = Score()
        p = s.add_child(Part('p1'))
        p.add_measure()
        p.add_chord(Chord(60, 0.2))
        p.add_chord(Chord(60, 3.8))
        assert [ch.quarter_duration for ch in p.get_chords()] == [0.2, 0.8, 3]
        b = p.get_measure(1).get_staff(1).get_voice(1).get_beat(1)
        b.set_possible_subdivisions(subdivisions=[2, 3, 4])
        b.quantize_quarter_durations()
        assert [ch.quarter_duration for ch in p.get_measure(1).get_staff(1).get_voice(1).get_chords()] == [0.25, 0.75, 3]
        assert [ch.offset for ch in p.get_measure(1).get_staff(1).get_voice(1).get_chords()] == [0, 0.25, 0]

    def test_complex_quantization(self):
        s = Score()
        s.set_possible_subdivisions([2, 3, 4, 6, 8])
        p = s.add_child(Part('p1'))
        import random
        random.seed(11)
        quarter_durations = []
        while sum(quarter_durations) < 40:
            quarter_durations.append(QuarterDuration(random.random() + random.randint(0, 3)))
        quarter_durations.append(44 - sum(quarter_durations))

        for qd in quarter_durations:
            p.add_chord(Chord(midis=60, quarter_duration=qd))
        for beat in [b for m in p.get_children() for st in m.get_children() for v in st.get_children() for b in v.get_children()]:
            beat.quantize_quarter_durations()
        # p.quantize = True
        for measure in p.get_children():
            v = measure.get_staff(1).get_voice(1)
            for b in v.get_children():
                qds = [ch.quarter_duration for ch in b.get_children()]
                div = lcm([qd.denominator for qd in qds])
                if div != 1:
                    assert div in [2, 3, 4, 6, 8]

    def test_part_quantization(self):
        s = Score()
        s.set_possible_subdivisions([2, 3, 4, 6, 8])
        p = s.add_child(Part('p1'))
        for qd in [2, 2 / 7, 1, 5 / 7]:
            p.add_chord(Chord(60, qd))
        p.quantize = True
        p.final_updates()
        assert [ch.quarter_duration for ch in p.get_chords()] == [2, 1 / 4, 3 / 4, 1 / 4, 3 / 4]
        assert p.get_measure(1).get_divisions() == 4
        assert [ch.notes[0].xml_duration.value_ for ch in p.get_chords()] == [8, 1, 3, 1, 3]

    # def test_zero_not_as_tied_to(self):
    #     """
    #     Three cases where a zero quarter_duration appears during quantization. If a chord with zero qd is tied to previous,
    #     it must be omitted.
    #     """
    #     qds1 = [QuarterDuration(139, 171), QuarterDuration(134, 945), QuarterDuration(35, 772)]
    #     qds2 = [QuarterDuration(314, 487), QuarterDuration(18, 605), QuarterDuration(235, 722)]
    #     qds3 = [QuarterDuration(638, 643), QuarterDuration(3, 643), QuarterDuration(2, 643)]
    #     p = Part('p1')
    #     p.set_possible_subdivisions([2, 3, 4, 6, 8], 1)
    #     for index, qds in enumerate([qds1, qds2, qds3]):
    #         assert sum(qds) == 1
    #         for qd in qds:
    #             p.add_chord(Chord(midis=60, quarter_duration=qd))
    #         b = p.get_measure(1).get_staff(1).get_voice(1).get_beat(index + 1)
    #         b.quantize_quarter_durations()
    #         if index == 0:
    #             assert [ch.quarter_duration for ch in b.get_chords()] == [QuarterDuration(5, 6), QuarterDuration(1, 6)]
    #         elif index == 1:
    #             assert [ch.quarter_duration for ch in b.get_chords()] == [QuarterDuration(5, 6), QuarterDuration(1, 6)]
    #         else:
    #             assert [ch.quarter_duration for ch in b.get_chords()] == [QuarterDuration(5, 6), QuarterDuration(1, 6)]
